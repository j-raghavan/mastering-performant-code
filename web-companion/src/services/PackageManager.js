/**
 * Package Manager Service
 * 
 * Handles installation and management of the mastering_performant_code wheel package
 */

import { Logger } from '../utils/Logger.js';

class PackageManager {
    constructor() {
        // Use wheel hosted directly on GitHub Pages to avoid CORS issues
        this.packageUrl = '/assets/mastering_performant_code-1.0.0-py3-none-any.whl';
        this.packageName = 'mastering_performant_code';
        this.packageVersion = '1.0.0';
        this.isInstalled = false;
        this.isInstalling = false;
        this.installationProgress = {
            status: 'idle',
            percentage: 0,
            message: ''
        };
        this.onProgressUpdate = null;
    }

    /**
     * Set progress update callback
     */
    setProgressCallback(callback) {
        this.onProgressUpdate = callback;
    }

    /**
     * Update installation progress
     */
    updateProgress(status, percentage, message) {
        this.installationProgress = { status, percentage, message };
        if (this.onProgressUpdate) {
            this.onProgressUpdate(this.installationProgress);
        }
        // Only log important status changes
        if (status === 'error' || status === 'complete' || percentage % 25 === 0) {
            Logger.info(`Package installation: ${status} - ${percentage}% - ${message}`);
        }
    }

    /**
     * Install the mastering_performant_code package
     */
    async installPackage(pyodide) {
        if (this.isInstalled) {
            Logger.info('Package already installed');
            return true;
        }

        if (this.isInstalling) {
            Logger.info('Package installation already in progress');
            return false;
        }

        this.isInstalling = true;
        this.updateProgress('starting', 0, 'Starting package installation...');

        try {
            // Step 1: Load micropip
            this.updateProgress('loading_micropip', 10, 'Loading micropip...');
            await pyodide.loadPackage(['micropip']);

            // Step 2: Download and install package
            this.updateProgress('downloading', 30, 'Downloading package from GitHub...');
            const micropip = pyodide.pyimport('micropip');
            await micropip.install(this.packageUrl);

            // Step 3: Verify installation
            this.updateProgress('verifying', 90, 'Verifying package installation...');
            const verified = await this.verifyInstallation(pyodide);

            if (verified) {
                this.isInstalled = true;
                this.updateProgress('complete', 100, 'Package installed successfully!');
                Logger.info('✅ Package installation completed successfully');
                return true;
            } else {
                throw new Error('Package verification failed');
            }

        } catch (error) {
            this.updateProgress('error', 0, `Installation failed: ${error.message}`);
            Logger.error('❌ Package installation failed:', error);
            throw error;
        } finally {
            this.isInstalling = false;
        }
    }

    /**
     * Verify that the package is installed and working correctly
     */
    async verifyInstallation(pyodide) {
        try {
            // Test basic import
            await pyodide.runPythonAsync(`
import mastering_performant_code
print(f"Package version: {mastering_performant_code.__version__}")
            `);

            // Test key chapter imports
            await pyodide.runPythonAsync(`
# Test Chapter 1 - Dynamic Array
from mastering_performant_code.chapter_01.dynamic_array import DynamicArray
arr = DynamicArray()
arr.append(1)
print(f"✓ Chapter 1: DynamicArray working (size: {len(arr)})")

# Test Chapter 2 - Algorithms
from mastering_performant_code.chapter_02.algorithms import bubble_sort
result = bubble_sort([3, 1, 4, 1, 5])
print(f"✓ Chapter 2: bubble_sort working (result: {result})")

# Test Chapter 3 - Applications (just import, don't call specific functions)
from mastering_performant_code.chapter_03 import applications
print(f"✓ Chapter 3: applications module imported successfully")

print("Package verification successful!")
            `);

            Logger.info('✅ Package verification completed successfully');
            return true;

        } catch (error) {
            Logger.error('❌ Package verification failed:', error);
            return false;
        }
    }

    /**
     * Check if package is installed
     */
    isPackageInstalled() {
        return this.isInstalled;
    }

    /**
     * Get package information
     */
    getPackageInfo() {
        return {
            name: this.packageName,
            version: this.packageVersion,
            url: this.packageUrl,
            isInstalled: this.isInstalled,
            isInstalling: this.isInstalling
        };
    }

    /**
     * Get installation progress
     */
    getInstallationProgress() {
        return { ...this.installationProgress };
    }

    /**
     * Reset installation state (for testing)
     */
    reset() {
        this.isInstalled = false;
        this.isInstalling = false;
        this.installationProgress = {
            status: 'idle',
            percentage: 0,
            message: ''
        };
        Logger.info('Package manager reset');
    }
}

export { PackageManager }; 