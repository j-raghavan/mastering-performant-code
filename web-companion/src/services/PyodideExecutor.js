/**
 * Pyodide Executor Service
 * 
 * Handles Python code execution in the browser using Pyodide
 */

import { Logger } from '../utils/Logger.js';
import { PackageManager } from './PackageManager.js';
import { ImportPathResolver } from './ImportPathResolver.js';

// Import loadPyodide from the global scope (loaded via CDN)
const { loadPyodide } = globalThis;

class PyodideExecutor {
    constructor() {
        this.pyodide = null;
        this.isInitialized = false;
        this.isInitializing = false;
        this.packages = new Set();
        this.executionQueue = [];
        this.maxExecutionTime = 30000; // 30 seconds

        // Initialize new services
        this.packageManager = new PackageManager();
        this.importPathResolver = new ImportPathResolver();
        this.packageInstalled = false;
    }

    /**
     * Initialize Pyodide
     */
    async initialize() {
        if (this.isInitialized) {
            return;
        }

        if (this.isInitializing) {
            // Wait for initialization to complete
            while (this.isInitializing) {
                await new Promise(resolve => setTimeout(resolve, 100));
            }
            return;
        }

        this.isInitializing = true;

        try {
            Logger.info('🚀 Initializing Pyodide...');

            // Check if loadPyodide is available
            if (typeof loadPyodide === 'undefined') {
                throw new Error('loadPyodide function not available. Check if Pyodide script is loaded.');
            }

            Logger.info('Loading Pyodide from CDN...');

            // Use the same configuration as the working pyodide-demo
            this.pyodide = await loadPyodide({
                indexURL: "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/",
                fullStdLib: false  // Load minimal stdlib first
            });

            Logger.info('✅ Pyodide loaded successfully');

            // Expose globally for retry button
            window.pyodideExecutor = this;

            // Check Python version
            const pythonVersion = await this.pyodide.runPythonAsync(`
import sys
print(f"Python {sys.version}")
sys.version
            `);
            Logger.info(`🐍 Python version: ${pythonVersion}`);

            // Setup Python environment
            await this.setupPythonEnvironment();

            // Always install the mastering_performant_code package automatically
            await this.installMasteringPerformantCode();

            this.isInitialized = true;
            Logger.info('✅ Pyodide initialization completed');

        } catch (error) {
            Logger.error('❌ Failed to initialize Pyodide:', error);
            this.isInitializing = false;

            // Provide helpful error message
            if (error.message.includes('WASM')) {
                throw new Error(`WASM instantiation failed. This might be due to:
1. Browser compatibility issues (try Chrome/Edge)
2. Memory limitations (close other tabs)
3. Network issues (check internet connection)
4. Browser security settings (allow WASM execution)
                
Original error: ${error.message}`);
            }

            throw error;
        } finally {
            this.isInitializing = false;
        }
    }

    /**
     * Install the mastering_performant_code package
     */
    async installMasteringPerformantCode() {
        try {
            Logger.info('📦 Installing mastering_performant_code package...');

            // Set up progress callback
            this.packageManager.setProgressCallback((progress) => {
                Logger.info(`Package installation progress: ${progress.status} - ${progress.percentage}%`);
            });

            // Install the package
            const success = await this.packageManager.installPackage(this.pyodide);

            if (success) {
                this.packageInstalled = true;
                Logger.info('✅ mastering_performant_code package installed successfully');
            } else {
                Logger.warn('⚠️ mastering_performant_code package installation failed, but continuing...');
            }

        } catch (error) {
            Logger.error('❌ Failed to install mastering_performant_code package:', error);
            // Don't throw error - allow execution to continue without the package
        }
    }

    /**
     * Set up Python environment with custom modules
     */
    async setupPythonEnvironment() {
        try {
            Logger.info('Setting up Python environment...');

            // Simple setup - just verify Pyodide is working (same as pyodide-demo)
            const testResult = this.pyodide.runPython(`
import sys
import time
print("Python environment ready!")
"Environment setup complete"
            `);

            Logger.info('Python environment setup successful:', testResult);

        } catch (error) {
            Logger.error('Python environment setup failed:', error);
            throw new Error(`Python environment setup failed: ${error.message}`);
        }
    }

    /**
     * Execute Python code with import transformation
     */
    async execute(code, options = {}) {
        if (!this.isInitialized) {
            throw new Error('PyodideExecutor not initialized');
        }

        let transformedCode = code;
        let transformationInfo = null;

        // Apply import transformation if package is installed
        if (this.packageInstalled) {
            const transformation = this.importPathResolver.transformCode(code);
            transformedCode = transformation.transformedCode;
            transformationInfo = transformation;

            // Check if there were any transformations
            if (transformation.diagnostics && transformation.diagnostics.transformations.length > 0) {
                const transformationCount = transformation.diagnostics.transformations.reduce((sum, t) => sum + t.count, 0);
                Logger.info(`Applied ${transformationCount} import transformations`);
            }
        }

        // Patch to define __file__ if not present
        const filePatch = `\ntry:\n    __file__\nexcept NameError:\n    __file__ = '<pyodide>'\n`;
        const patchedCode = filePatch + '\n' + transformedCode;

        const executionOptions = {
            timeout: this.maxExecutionTime,
            captureOutput: true,
            measurePerformance: true,
            ...options
        };

        const startTime = performance.now();
        const executionResult = {
            success: false,
            output: '',
            error: null,
            executionTime: 0,
            memoryUsage: null,
            warnings: [],
            transformationInfo: transformationInfo
        };

        try {
            Logger.info('🐍 Executing Python code...');

            // Capture Python output using the working approach from pyodide-demo
            this.pyodide.runPython(`
import sys
import os
print(f"Current working directory: {os.getcwd()}")
from io import StringIO
sys.stdout = StringIO()
sys.stderr = StringIO()
            `);

            // Measure execution time
            const executionStartTime = performance.now();

            // Run the user code (with __file__ patch)
            const result = this.pyodide.runPython(patchedCode);

            const executionEndTime = performance.now();
            const executionTime = executionEndTime - executionStartTime;

            // Get captured output
            const stdout = this.pyodide.runPython("sys.stdout.getvalue()");
            const stderr = this.pyodide.runPython("sys.stderr.getvalue()");

            // Reset stdout/stderr
            this.pyodide.runPython(`
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__
            `);

            executionResult.success = true;
            executionResult.output = stdout || '';
            executionResult.error = stderr || null;
            executionResult.executionTime = executionTime;

            Logger.info(`✅ Code executed successfully in ${executionResult.executionTime.toFixed(2)}ms`);

        } catch (error) {
            executionResult.success = false;
            executionResult.error = error.message;
            executionResult.executionTime = performance.now() - startTime;

            Logger.error('❌ Code execution failed:', error);
        }

        // Get memory usage
        if (executionOptions.measurePerformance) {
            executionResult.memoryUsage = await this.getMemoryUsage();
        }

        return executionResult;
    }

    /**
     * Transform imports and execute code
     */
    async transformAndExecute(code, options = {}) {
        try {
            // Transform import statements
            const transformationResult = this.importPathResolver.transformCode(code);
            const { transformedCode, diagnostics } = transformationResult;

            // Only log if there were actual transformations
            if (diagnostics.transformations.length > 0) {
                Logger.debug(`[PyodideExecutor] Applied ${diagnostics.transformations.length} import transformations`);
            }

            // Execute the transformed code
            const result = await this.execute(transformedCode, options);

            // Add import diagnostics to result
            return {
                ...result,
                importDiagnostics: diagnostics
            };

        } catch (error) {
            Logger.error('Transform and execute failed:', error);
            throw error;
        }
    }

    /**
     * Get import diagnostics for code without executing
     */
    getImportDiagnostics(code) {
        if (!this.packageInstalled) {
            return {
                transformations: [],
                warnings: ['Package not installed - no transformations applied'],
                errors: []
            };
        }

        const transformation = this.importPathResolver.transformCode(code);
        const validation = this.importPathResolver.validateTransformation(code, transformation.transformedCode);

        return {
            transformations: transformation.diagnostics.transformations || [],
            warnings: [...(transformation.diagnostics.warnings || []), ...(validation.warnings || [])],
            errors: [...(transformation.diagnostics.errors || []), ...(validation.errors || [])],
            originalCode: code,
            transformedCode: transformation.transformedCode
        };
    }

    /**
     * Verify package installation
     */
    async verifyPackageInstallation() {
        if (!this.packageInstalled) {
            return false;
        }

        try {
            const result = await this.pyodide.runPythonAsync(`
import mastering_performant_code
print(f"Package version: {mastering_performant_code.__version__}")
True
            `);
            return result === true;
        } catch (error) {
            Logger.error('Package verification failed:', error);
            return false;
        }
    }

    /**
     * Install additional package
     */
    async installPackage(packageName) {
        if (!this.isInitialized) {
            await this.initialize();
        }

        if (this.packages.has(packageName)) {
            Logger.info(`Package ${packageName} already installed`);
            return;
        }

        try {
            Logger.info(`📦 Installing package: ${packageName}`);
            await this.pyodide.loadPackage(packageName);
            this.packages.add(packageName);
            Logger.info(`✅ Package ${packageName} installed successfully`);
        } catch (error) {
            Logger.error(`❌ Failed to install package ${packageName}:`, error);
            throw error;
        }
    }

    /**
     * Get memory usage information
     */
    async getMemoryUsage() {
        if (!this.pyodide || !this.isInitialized) {
            return {
                heapSize: 0,
                totalObjects: 0,
                garbageCount: 0,
                available: false
            };
        }

        try {
            const memoryInfo = await this.pyodide.runPythonAsync(`
import sys
import gc

# Force garbage collection
gc.collect()

# Get memory info
memory_info = {
    'heap_size': sys.getsizeof([]),
    'total_objects': len(gc.get_objects()),
    'garbage_count': len(gc.garbage)
}
memory_info
            `);

            return {
                heapSize: memoryInfo.heap_size,
                totalObjects: memoryInfo.total_objects,
                garbageCount: memoryInfo.garbage_count,
                available: true
            };
        } catch (error) {
            Logger.warn('Failed to get memory usage:', error);
            return {
                heapSize: 0,
                totalObjects: 0,
                garbageCount: 0,
                available: false,
                error: error.message
            };
        }
    }

    /**
     * Interrupt current execution
     */
    interrupt() {
        if (this.pyodide) {
            // Pyodide doesn't support direct interruption, but we can clear globals
            try {
                this.pyodide.runPython('import sys; sys.exit()');
            } catch (error) {
                Logger.warn('Interrupt failed:', error);
            }
        }
    }

    /**
     * Reset Pyodide environment
     */
    async reset() {
        try {
            Logger.info('🔄 Resetting Pyodide environment...');

            // Clear Python globals
            if (this.pyodide) {
                await this.pyodide.runPythonAsync(`
import sys
import gc

# Clear all modules except built-ins
for module_name in list(sys.modules.keys()):
    if not module_name.startswith('_') and module_name not in ['sys', 'builtins', 'gc']:
        del sys.modules[module_name]

# Force garbage collection
gc.collect()
                `);
            }

            // Reset services
            this.packageManager.reset();
            this.importPathResolver.resetStats();
            this.packageInstalled = false;

            Logger.info('✅ Pyodide environment reset completed');
        } catch (error) {
            Logger.error('❌ Failed to reset Pyodide environment:', error);
            throw error;
        }
    }

    /**
     * Check if Pyodide is ready
     */
    isReady() {
        return this.isInitialized && this.pyodide !== null;
    }

    /**
     * Get Python version
     */
    async getPythonVersion() {
        if (!this.isInitialized) {
            await this.initialize();
        }

        try {
            const version = await this.pyodide.runPythonAsync(`
import sys
sys.version
            `);
            return version;
        } catch (error) {
            Logger.error('Failed to get Python version:', error);
            return 'Unknown';
        }
    }

    /**
     * Get installed packages
     */
    getInstalledPackages() {
        const packages = Array.from(this.packages);
        if (this.packageInstalled) {
            packages.push('mastering_performant_code');
        }
        return packages;
    }

    /**
     * Get package manager instance
     */
    getPackageManager() {
        return this.packageManager;
    }

    /**
     * Get import resolver instance
     */
    getImportResolver() {
        return this.importPathResolver;
    }
}

export { PyodideExecutor }; 