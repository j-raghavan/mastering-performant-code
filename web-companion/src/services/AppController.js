/**
 * Application Controller
 * 
 * Main orchestrator for the Pyodide Interactive Companion application
 */

import { Logger } from '../utils/Logger.js';
import { FileLoader } from './FileLoader.js';
import { UIManager } from './UIManager.js';

class AppController {
    constructor(services) {
        this.services = services;
        this.stateManager = services.stateManager;
        this.storageService = services.storageService;
        this.contentSyncService = services.contentSyncService;
        this.pyodideExecutor = services.pyodideExecutor;
        this.chapterManager = services.chapterManager;
        this.errorHandler = services.errorHandler;
        this.testRunner = null; // Will be initialized later

        // Initialize FileLoader and UIManager
        this.fileLoader = new FileLoader(this.contentSyncService);
        this.uiManager = new UIManager();

        this.currentChapter = null;
        this.currentFile = null;
        this.eventSubscribers = new Map();
        this.uiComponents = new Map();
        this.isInitialized = false;
    }

    async initialize() {
        try {
            Logger.info('🚀 Initializing AppController...');

            // Initialize services
            await this.initializeServices();

            // Initialize FileLoader and UIManager
            await this.initializeInteractiveServices();

            // Set up event handling
            this.setupEventHandling();

            // Set up UI event handlers
            this.setupUIEventHandlers();

            this.isInitialized = true;
            Logger.info('✅ AppController initialized successfully');

        } catch (error) {
            Logger.error('❌ Failed to initialize AppController:', error);
            this.errorHandler.handleError(error);
            throw error;
        }
    }

    async initializeServices() {
        // Initialize content sync service first
        await this.contentSyncService.initialize();

        // Initialize Pyodide executor
        await this.pyodideExecutor.initialize();

        // Log Python version
        const pythonVersion = await this.pyodideExecutor.getPythonVersion();
        Logger.info(`🐍 Using Python: ${pythonVersion}`);

        // Initialize test runner
        this.testRunner = new (await import('./TestRunner.js')).TestRunner(this.pyodideExecutor);
        await this.testRunner.initialize();

        // Initialize chapter manager
        await this.chapterManager.initialize();

        // Initialize performance analyzer
        this.performanceAnalyzer = new (await import('./PerformanceAnalyzer.js')).PerformanceAnalyzer();
        await this.performanceAnalyzer.initialize();

        // Initialize state manager
        await this.stateManager.initialize();

        Logger.info('✅ All services initialized');
    }

    async initializeInteractiveServices() {
        try {
            Logger.info('Initializing interactive services...');

            // Initialize FileLoader
            const fileLoaderResult = await this.fileLoader.initialize();
            if (!fileLoaderResult.success) {
                throw new Error(`FileLoader initialization failed: ${fileLoaderResult.message}`);
            }

            // Initialize UIManager
            const uiManagerResult = await this.uiManager.initialize();
            if (!uiManagerResult.success) {
                throw new Error(`UIManager initialization failed: ${uiManagerResult.message}`);
            }

            // Set up UI event handlers
            this.uiManager.setEventHandlers({
                onFileSelected: (path) => this.handleFileSelection(path),
                onRunFile: () => this.handleRunCurrentFile(),
                onRunAllFiles: () => this.handleRunAllFiles(),
                onRunTests: () => this.handleRunAllTests()
            });

            Logger.info('✅ Interactive services initialized');

        } catch (error) {
            Logger.error('Failed to initialize interactive services:', error);
            throw error;
        }
    }

    setupEventHandling() {
        // Set up global error handling
        window.addEventListener('error', (event) => {
            this.errorHandler.handleError(event.error);
        });

        window.addEventListener('unhandledrejection', (event) => {
            this.errorHandler.handleError(event.reason);
        });
    }

    setupUIEventHandlers() {
        // Handle file selection
        this.uiManager.onFileSelected = (path) => this.handleFileSelection(path);

        // Handle code execution
        this.uiManager.onRunFile = () => this.handleRunCurrentFile();
        this.uiManager.onRunAllFiles = () => this.handleRunAllFiles();
        this.uiManager.onRunTests = () => this.handleRunAllTests();
    }

    async loadChapter(chapterId) {
        try {
            Logger.info(`📖 Loading chapter: ${chapterId}`);

            // Load chapter data
            const chapter = await this.chapterManager.getChapter(chapterId);
            if (!chapter) {
                throw new Error(`Chapter not found: ${chapterId}`);
            }

            // Load chapter content
            const chapterContent = await this.contentSyncService.loadChapterContent(chapterId);

            this.currentChapter = {
                ...chapter,
                ...chapterContent
            };

            // Load files for the chapter
            const fileLoaderResult = await this.fileLoader.loadChapterFiles(chapterId);
            if (!fileLoaderResult.success) {
                throw new Error(`Failed to load chapter files: ${fileLoaderResult.error}`);
            }

            // Update UI with files
            this.updateUIWithFiles();

            // Update state
            this.stateManager.setState({
                currentChapter: this.currentChapter,
                currentFile: null
            });

            // Emit chapter loaded event
            this.emit('chapter:loaded', this.currentChapter);

            Logger.info(`✅ Chapter loaded successfully: ${chapter.title}`);

            return this.currentChapter;

        } catch (error) {
            Logger.error(`❌ Failed to load chapter ${chapterId}:`, error);
            this.errorHandler.handleError(error);
            throw error;
        }
    }

    updateUIWithFiles() {
        try {
            // Get files organized for display
            const files = this.fileLoader.getFilesForDisplay();

            // Update UI manager with files
            this.uiManager.displayFileExplorer(files);
            this.uiManager.populateFileSelector(files);

            // Enable buttons
            this.uiManager.setButtonsEnabled(true);

            // Update metrics
            const stats = this.fileLoader.getStats();
            this.uiManager.updateMetrics({
                filesLoaded: stats.totalFiles,
                loadTime: Date.now() - this.startTime,
                memoryUsage: this.pyodideExecutor.getMemoryUsage()
            });

            // Select first demo file if available
            const demoFiles = this.fileLoader.getDemoFiles();
            if (demoFiles.length > 0) {
                this.handleFileSelection(demoFiles[0].path);
            } else {
                // Select first available file
                const allFiles = this.fileLoader.getAllFiles();
                if (allFiles.length > 0) {
                    this.handleFileSelection(allFiles[0].path);
                }
            }

            Logger.info(`UI updated with ${stats.totalFiles} files`);

        } catch (error) {
            Logger.error('Failed to update UI with files:', error);
        }
    }

    async handleFileSelection(path) {
        try {
            Logger.info(`📁 File selected: ${path}`);

            const content = this.fileLoader.getFileContent(path);
            if (!content) {
                throw new Error(`File content not found: ${path}`);
            }

            // Display file content in UI
            this.uiManager.displayFileContent(path, content);

            // Update current file
            this.currentFile = path;

            // Update state
            this.stateManager.setState({
                currentFile: path
            });

            Logger.info(`✅ File loaded: ${path}`);

        } catch (error) {
            Logger.error(`Failed to handle file selection: ${path}`, error);
            this.uiManager.showNotification(`Failed to load file: ${error.message}`, 'error');
        }
    }

    async handleRunCurrentFile() {
        if (!this.isInitialized) {
            this.uiManager.showNotification('Application not ready', 'warning');
            return;
        }

        const currentFile = this.uiManager.getCurrentFile();
        if (!currentFile) {
            this.uiManager.showNotification('No file selected', 'warning');
            return;
        }

        try {
            this.uiManager.log(`Executing: ${currentFile}`, 'info');
            this.uiManager.updateStatus('Executing Python code...', 'loading');

            const content = this.fileLoader.getFileContent(currentFile);
            if (!content) {
                throw new Error(`File content not found: ${currentFile}`);
            }

            // Execute the code
            const result = await this.pyodideExecutor.execute(content, {
                timeout: 30000,
                captureOutput: true,
                measurePerformance: true
            });

            // Display result
            this.uiManager.displayExecutionResult(result);

            // Update status
            if (result.success) {
                this.uiManager.updateStatus('Execution completed successfully!', 'ready');
                this.uiManager.log(`✅ Execution completed in ${result.executionTime.toFixed(2)}ms`, 'success');
            } else {
                this.uiManager.updateStatus('Execution failed', 'error');
                this.uiManager.log(`❌ Execution failed: ${result.error}`, 'error');
            }

            // Emit execution result
            this.emit('code:executed', {
                fileId: currentFile,
                code: content,
                ...result,
                timestamp: Date.now()
            });

        } catch (error) {
            Logger.error('Failed to execute current file:', error);
            this.uiManager.updateStatus('Execution failed', 'error');
            this.uiManager.showNotification(`Execution failed: ${error.message}`, 'error');
        }
    }

    async handleRunAllFiles() {
        if (!this.isInitialized) {
            this.uiManager.showNotification('Application not ready', 'warning');
            return;
        }

        try {
            this.uiManager.log('Running all demo files...', 'info');
            this.uiManager.updateStatus('Running all examples...', 'loading');

            const demoFiles = this.fileLoader.getDemoFiles();
            if (demoFiles.length === 0) {
                this.uiManager.showNotification('No demo files found', 'warning');
                return;
            }

            let successCount = 0;
            let totalTime = 0;

            for (const file of demoFiles) {
                try {
                    this.uiManager.log(`Running: ${file.name}`, 'info');

                    const result = await this.pyodideExecutor.execute(file.content, {
                        timeout: 30000,
                        captureOutput: true,
                        measurePerformance: true
                    });

                    if (result.success) {
                        successCount++;
                        totalTime += result.executionTime;
                        this.uiManager.log(`✅ ${file.name}: ${result.executionTime.toFixed(2)}ms`, 'success');
                    } else {
                        this.uiManager.log(`❌ ${file.name}: ${result.error}`, 'error');
                    }

                } catch (error) {
                    this.uiManager.log(`❌ ${file.name}: ${error.message}`, 'error');
                }
            }

            const summary = `Completed ${successCount}/${demoFiles.length} files in ${totalTime.toFixed(2)}ms`;
            this.uiManager.updateStatus(summary, successCount === demoFiles.length ? 'ready' : 'warning');
            this.uiManager.log(summary, 'info');

        } catch (error) {
            Logger.error('Failed to run all files:', error);
            this.uiManager.updateStatus('Failed to run all files', 'error');
            this.uiManager.showNotification(`Failed to run all files: ${error.message}`, 'error');
        }
    }

    async handleRunAllTests() {
        if (!this.isInitialized) {
            this.uiManager.showNotification('Application not ready', 'warning');
            return;
        }

        try {
            this.uiManager.log('Running all tests...', 'info');
            this.uiManager.updateStatus('Running tests...', 'loading');

            const testFiles = this.fileLoader.getTestFiles();
            if (testFiles.length === 0) {
                this.uiManager.showNotification('No test files found', 'warning');
                return;
            }

            let successCount = 0;
            let totalTime = 0;

            for (const file of testFiles) {
                try {
                    this.uiManager.log(`Running tests: ${file.name}`, 'info');

                    const result = await this.testRunner.runTests(file.content, {
                        timeout: 30000,
                        captureOutput: true
                    });

                    if (result.success) {
                        successCount++;
                        totalTime += result.executionTime;
                        this.uiManager.log(`✅ ${file.name}: ${result.passedTests}/${result.totalTests} passed`, 'success');
                    } else {
                        this.uiManager.log(`❌ ${file.name}: ${result.error}`, 'error');
                    }

                } catch (error) {
                    this.uiManager.log(`❌ ${file.name}: ${error.message}`, 'error');
                }
            }

            const summary = `Tests completed: ${successCount}/${testFiles.length} files`;
            this.uiManager.updateStatus(summary, successCount === testFiles.length ? 'ready' : 'warning');
            this.uiManager.log(summary, 'info');

        } catch (error) {
            Logger.error('Failed to run tests:', error);
            this.uiManager.updateStatus('Failed to run tests', 'error');
            this.uiManager.showNotification(`Failed to run tests: ${error.message}`, 'error');
        }
    }

    async handleChapterSelection(chapter) {
        try {
            Logger.info(`🎯 Handling chapter selection: ${chapter.id}`);

            // Load the selected chapter
            await this.loadChapter(chapter.id);

            // Update UI components
            this.updateUIForChapter(chapter);

        } catch (error) {
            Logger.error('Failed to handle chapter selection:', error);
            this.errorHandler.handleError(error);
        }
    }

    updateUIForChapter(chapter) {
        // Update navigation
        const navigation = this.uiComponents.get('navigation');
        if (navigation) {
            navigation.setCurrentChapter(chapter);
        }

        // Update code panel with chapter files
        const codePanel = this.uiComponents.get('codePanel');
        if (codePanel && chapter.sourceFiles) {
            codePanel.setFiles(chapter.sourceFiles);
        }

        Logger.info(`UI updated for chapter: ${chapter.title}`);
    }

    async handleCodeExecution(fileId, code) {
        try {
            Logger.info(`🐍 Executing code for file: ${fileId}`);

            // Execute code
            const result = await this.pyodideExecutor.execute(code, {
                timeout: 30000,
                captureOutput: true,
                measurePerformance: true
            });

            // Update current file
            this.currentFile = fileId;

            // Store result
            const executionResult = {
                fileId,
                code,
                ...result,
                timestamp: Date.now()
            };

            // Update state
            this.stateManager.setState({
                lastExecution: executionResult
            });

            // Emit execution result
            this.emit('code:executed', executionResult);

            // Analyze performance if execution was successful
            if (result.success && this.performanceAnalyzer) {
                try {
                    const performanceMetrics = await this.performanceAnalyzer.analyzeExecution(result);
                    this.emit('performance:analyzed', {
                        type: 'execution',
                        data: performanceMetrics
                    });
                } catch (error) {
                    Logger.warn('Failed to analyze performance:', error);
                }
            }

            Logger.info(`✅ Code execution completed for ${fileId}`);

            return executionResult;

        } catch (error) {
            Logger.error(`❌ Failed to execute code for ${fileId}:`, error);
            this.errorHandler.handleError(error);
            throw error;
        }
    }

    async handleTestExecution(chapterId) {
        try {
            Logger.info(`🧪 Running tests for chapter: ${chapterId}`);

            if (!this.testRunner) {
                throw new Error('Test runner not initialized');
            }

            // Run tests
            const results = await this.testRunner.runChapterTests(chapterId);

            // Update state
            this.stateManager.setState({
                testResults: results
            });

            // Emit test results
            this.emit('tests:completed', results);

            Logger.info(`✅ Tests completed for chapter ${chapterId}: ${results.length} tests`);

            return results;

        } catch (error) {
            Logger.error(`❌ Test execution failed for chapter ${chapterId}:`, error);
            this.errorHandler.handleError(error);
            throw error;
        }
    }

    async handleSearch(query) {
        try {
            Logger.info(`🔍 Handling search: ${query}`);

            if (!query || query.trim().length === 0) {
                return [];
            }

            // Search in current chapter
            const results = await this.searchInCurrentChapter(query);

            // Emit search results
            this.emit('search:results', results);

            return results;

        } catch (error) {
            Logger.error('Search failed:', error);
            this.errorHandler.handleError(error);
            return [];
        }
    }

    async searchInCurrentChapter(query) {
        if (!this.currentChapter || !this.currentChapter.sourceFiles) {
            return [];
        }

        const results = [];
        const searchTerm = query.toLowerCase();

        for (const file of this.currentChapter.sourceFiles) {
            if (file.content) {
                const lines = file.content.split('\n');
                const matches = [];

                lines.forEach((line, index) => {
                    if (line.toLowerCase().includes(searchTerm)) {
                        matches.push({
                            line: index + 1,
                            content: line.trim(),
                            context: lines.slice(Math.max(0, index - 2), index + 3).join('\n')
                        });
                    }
                });

                if (matches.length > 0) {
                    results.push({
                        file: file.name,
                        matches
                    });
                }
            }
        }

        return results;
    }

    registerUIComponent(name, component) {
        this.uiComponents.set(name, component);
        Logger.info(`UI component registered: ${name}`);
    }

    getUIComponent(name) {
        return this.uiComponents.get(name);
    }

    getCurrentState() {
        return this.stateManager.getState();
    }

    getCurrentChapter() {
        return this.currentChapter;
    }

    getCurrentFile() {
        return this.currentFile;
    }

    // Event system
    subscribe(event, callback) {
        if (!this.eventSubscribers.has(event)) {
            this.eventSubscribers.set(event, []);
        }
        this.eventSubscribers.get(event).push(callback);
    }

    unsubscribe(event, callback) {
        const subscribers = this.eventSubscribers.get(event);
        if (subscribers) {
            const index = subscribers.indexOf(callback);
            if (index > -1) {
                subscribers.splice(index, 1);
            }
        }
    }

    emit(event, data) {
        const subscribers = this.eventSubscribers.get(event) || [];
        subscribers.forEach(callback => {
            try {
                callback(data);
            } catch (error) {
                Logger.error(`Error in event subscriber for ${event}:`, error);
                this.errorHandler.handleError(error);
            }
        });
    }

    // Utility methods
    async saveUserProgress() {
        try {
            if (this.currentChapter) {
                await this.storageService.saveProgress(this.currentChapter.id, {
                    timestamp: Date.now(),
                    chapterId: this.currentChapter.id,
                    currentFile: this.currentFile
                });
            }
        } catch (error) {
            Logger.error('Failed to save user progress:', error);
        }
    }

    async loadUserProgress() {
        try {
            if (this.currentChapter) {
                const progress = await this.storageService.getProgress(this.currentChapter.id);
                if (progress) {
                    this.currentFile = progress.currentFile;
                    return progress;
                }
            }
        } catch (error) {
            Logger.error('Failed to load user progress:', error);
        }
        return null;
    }

    // Cleanup
    destroy() {
        Logger.info('🧹 Cleaning up AppController...');

        // Clear event subscribers
        this.eventSubscribers.clear();

        // Clear UI components
        this.uiComponents.clear();

        // Save progress before destroying
        this.saveUserProgress();

        Logger.info('✅ AppController cleanup completed');
    }
}

export { AppController }; 