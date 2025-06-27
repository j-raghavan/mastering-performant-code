/**
 * Application Controller
 * 
 * Main orchestrator for the Pyodide Interactive Companion application
 */

import { Logger } from '../utils/Logger.js';
import { FileLoader } from './FileLoader.js';
import { UIManager } from './UIManager.js';
import { PackageStatusPanel } from '../components/package/PackageStatusPanel.js';

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

        // Initialize package management components
        this.packageStatusPanel = new PackageStatusPanel();

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

            // Initialize package management UI
            await this.initializePackageManagement();

            // Set up event handling
            this.setupEventHandling();

            // Set up UI event handlers
            this.setupUIEventHandlers();

            // Load all chapters and set up chapter selector
            Logger.info('📚 About to load chapters from content service...');
            const chapters = this.contentSyncService.getAllChapters();
            Logger.info(`📚 Loaded ${chapters.length} chapters from content service`);

            // Debug: Log first few chapters
            if (chapters && chapters.length > 0) {
                Logger.info('First 3 chapters from AppController:');
                chapters.slice(0, 3).forEach((chapter, index) => {
                    let displayTitle = chapter.title;
                    if (chapter.description) {
                        displayTitle = `Chapter ${chapter.number}: ${chapter.description}`;
                    } else if (chapter.title && chapter.title !== `Chapter ${chapter.number}`) {
                        displayTitle = chapter.title;
                    } else {
                        displayTitle = `Chapter ${chapter.number}`;
                    }
                    Logger.info(`  Chapter ${index + 1}: id="${chapter.id}", title="${displayTitle}", order=${chapter.order}`);
                });
            } else {
                Logger.warn('⚠️ No chapters returned from content service');
            }

            // Populate the chapter selector in the HTML
            this.setupChapterSelector(chapters);

            // Try to set up navigation if available
            const navigation = this.uiComponents.get('navigation');
            if (navigation) {
                navigation.setChapters(chapters);
                Logger.info(`✅ Navigation component updated with ${chapters.length} chapters`);
            } else {
                Logger.warn('⚠️ Navigation component not found - using HTML chapter selector');
            }

            this.isInitialized = true;
            Logger.info('✅ AppController initialized successfully');

        } catch (error) {
            Logger.error('❌ Failed to initialize AppController:', error);
            this.errorHandler.handleError(error);
            throw error;
        }
    }

    async initializeServices() {
        try {
            Logger.info('🚀 Starting service initialization...');

            // Initialize content sync service first
            Logger.info('📚 Initializing ContentSyncService...');
            await this.contentSyncService.initialize();
            Logger.info('✅ ContentSyncService initialized successfully');

            // Initialize Pyodide executor (this will also install the package)
            Logger.info('🐍 Initializing PyodideExecutor...');
            await this.pyodideExecutor.initialize();
            Logger.info('✅ PyodideExecutor initialized successfully');

            // Log Python version
            const pythonVersion = await this.pyodideExecutor.getPythonVersion();
            Logger.info(`🐍 Using Python: ${pythonVersion}`);

            // Log package installation status
            const packageManager = this.pyodideExecutor.getPackageManager();
            const packageInfo = packageManager.getPackageInfo();
            Logger.info(`📦 Package status: ${packageInfo.isInstalled ? 'Installed' : 'Not installed'}`);

            // Initialize test runner
            Logger.info('🧪 Initializing TestRunner...');
            this.testRunner = new (await import('./TestRunner.js')).TestRunner(this.pyodideExecutor);
            await this.testRunner.initialize();
            Logger.info('✅ TestRunner initialized successfully');

            // Initialize chapter manager
            Logger.info('📖 Initializing ChapterManager...');
            await this.chapterManager.initialize();
            Logger.info('✅ ChapterManager initialized successfully');

            // Initialize performance analyzer
            Logger.info('⚡ Initializing PerformanceAnalyzer...');
            this.performanceAnalyzer = new (await import('./PerformanceAnalyzer.js')).PerformanceAnalyzer();
            await this.performanceAnalyzer.initialize();
            Logger.info('✅ PerformanceAnalyzer initialized successfully');

            // Initialize state manager
            Logger.info('💾 Initializing StateManager...');
            await this.stateManager.initialize();
            Logger.info('✅ StateManager initialized successfully');

            Logger.info('✅ All services initialized successfully');
        } catch (error) {
            Logger.error('❌ Failed to initialize services:', error);
            throw error;
        }
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

    async initializePackageManagement() {
        try {
            Logger.info('Initializing package management...');

            // Get package manager from PyodideExecutor
            const packageManager = this.pyodideExecutor.getPackageManager();

            // Initialize package status panel (but don't show it - installation is automatic)
            this.packageStatusPanel.init(packageManager);

            // Don't show the panel - package installation is automatic
            // this.packageStatusPanel.show();

            // Register the panel as a UI component
            this.registerUIComponent('packageStatusPanel', this.packageStatusPanel);

            Logger.info('✅ Package management initialized');

        } catch (error) {
            Logger.error('Failed to initialize package management:', error);
            // Don't throw error - package management is optional
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

            return this.currentChapter;

        } catch (error) {
            Logger.error(`❌ Failed to load chapter ${chapterId}:`, error);
            this.errorHandler.handleError(error);
            throw error;
        }
    }

    updateUIWithFiles() {
        try {
            // Get files organized for display, hiding test files by default
            const files = this.fileLoader.getFilesForDisplay({ includeTests: false });

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

        } catch (error) {
            Logger.error('Failed to update UI with files:', error);
        }
    }

    async handleFileSelection(path) {
        try {
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

            // Execute the code with import transformation
            const result = await this.pyodideExecutor.transformAndExecute(content, {
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

                    // Execute with import transformation
                    const result = await this.pyodideExecutor.transformAndExecute(file.content, {
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
            // Get import diagnostics before execution
            const importDiagnostics = this.pyodideExecutor.getImportDiagnostics(code);

            // Execute code with transformation
            const result = await this.pyodideExecutor.transformAndExecute(code, {
                timeout: 30000,
                captureOutput: true,
                measurePerformance: true
            });

            // Update current file
            this.currentFile = fileId;

            // Store result with import diagnostics
            const executionResult = {
                fileId,
                code,
                ...result,
                importDiagnostics,
                timestamp: Date.now()
            };

            // Update state
            this.stateManager.setState({
                lastExecution: executionResult
            });

            // Emit execution result
            this.emit('code:executed', executionResult);

            // Show import transformation notification if transformations were applied
            if (importDiagnostics.transformations.length > 0) {
                const transformationCount = importDiagnostics.transformations.reduce((sum, t) => sum + t.count, 0);
                this.uiManager.showNotification(
                    `Applied ${transformationCount} import transformation(s) automatically`,
                    'info'
                );
            }

            // Show warnings if any
            if (importDiagnostics.warnings.length > 0) {
                this.uiManager.showNotification(
                    `Import warnings: ${importDiagnostics.warnings.join(', ')}`,
                    'warning'
                );
            }

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

    /**
     * Set up the chapter selector in the HTML using MutationObserver for robustness
     */
    setupChapterSelector(chapters) {
        Logger.info(`Setting up chapter selector with ${chapters.length} chapters...`);

        // Try multiple ways to find the chapter selector
        let chapterSelector = document.getElementById('chapterSelector');

        if (!chapterSelector) {
            // Try alternative selectors
            chapterSelector = document.querySelector('select[id*="chapter"]');
        }

        if (!chapterSelector) {
            // Try finding any select element in the file explorer section
            const fileExplorerSection = document.querySelector('.file-explorer-section');
            if (fileExplorerSection) {
                chapterSelector = fileExplorerSection.querySelector('select');
            }
        }

        if (chapterSelector) {
            Logger.info('✅ Chapter selector found, setting up...');
            this.populateChapterSelector(chapterSelector, chapters);
            return;
        }

        // Element doesn't exist yet, use MutationObserver to wait for it
        Logger.info('⏳ Chapter selector not found, waiting for DOM with MutationObserver...');

        const observer = new MutationObserver((mutations, obs) => {
            // Try to find the element again after mutations
            let chapterSelector = document.getElementById('chapterSelector');

            if (!chapterSelector) {
                chapterSelector = document.querySelector('select[id*="chapter"]');
            }

            if (!chapterSelector) {
                const fileExplorerSection = document.querySelector('.file-explorer-section');
                if (fileExplorerSection) {
                    chapterSelector = fileExplorerSection.querySelector('select');
                }
            }

            if (chapterSelector) {
                Logger.info('✅ Chapter selector found via MutationObserver, setting up...');
                this.populateChapterSelector(chapterSelector, chapters);
                obs.disconnect(); // Stop observing once found
            }
        });

        // Start observing the document body for added nodes
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });

        // Set a timeout to prevent infinite waiting
        setTimeout(() => {
            observer.disconnect();

            // Final attempt to find the element
            let chapterSelector = document.getElementById('chapterSelector');
            if (!chapterSelector) {
                chapterSelector = document.querySelector('select[id*="chapter"]');
            }
            if (!chapterSelector) {
                const fileExplorerSection = document.querySelector('.file-explorer-section');
                if (fileExplorerSection) {
                    chapterSelector = fileExplorerSection.querySelector('select');
                }
            }

            if (!chapterSelector) {
                Logger.warn('⚠️ Chapter selector not found, creating it dynamically...');

                // Create the chapter selector dynamically as a fallback
                const fileExplorerSection = document.querySelector('.file-explorer-section');
                if (fileExplorerSection) {
                    Logger.info('Creating chapter selector dynamically...');

                    // Create the chapter selector container
                    const chapterSelectorContainer = document.createElement('div');
                    chapterSelectorContainer.style.marginBottom = '20px';

                    // Create the label
                    const label = document.createElement('label');
                    label.setAttribute('for', 'chapterSelector');
                    label.style.display = 'block';
                    label.style.marginBottom = '8px';
                    label.style.fontWeight = '500';
                    label.style.color = '#374151';
                    label.textContent = 'Select Chapter:';

                    // Create the select element
                    chapterSelector = document.createElement('select');
                    chapterSelector.id = 'chapterSelector';
                    chapterSelector.style.padding = '8px 12px';
                    chapterSelector.style.border = '1px solid #d1d5db';
                    chapterSelector.style.borderRadius = '6px';
                    chapterSelector.style.fontSize = '0.875rem';
                    chapterSelector.style.minWidth = '200px';

                    // Insert before the file explorer
                    const fileExplorer = fileExplorerSection.querySelector('#fileExplorer');
                    if (fileExplorer) {
                        fileExplorerSection.insertBefore(chapterSelectorContainer, fileExplorer);
                        chapterSelectorContainer.appendChild(label);
                        chapterSelectorContainer.appendChild(chapterSelector);

                        Logger.info('✅ Chapter selector created dynamically');
                        this.populateChapterSelector(chapterSelector, chapters);
                    } else {
                        Logger.error('❌ Could not find fileExplorer element to insert chapter selector');
                    }
                } else {
                    Logger.error('❌ Could not find file-explorer-section to create chapter selector');
                }
            } else {
                Logger.info('✅ Chapter selector found after timeout, setting up...');
                this.populateChapterSelector(chapterSelector, chapters);
            }
        }, 5000); // 5 second timeout
    }

    /**
     * Populate the chapter selector with options
     */
    populateChapterSelector(chapterSelector, chapters) {
        Logger.info(`Populating chapter selector with ${chapters.length} chapters...`);

        // Debug: Log chapters being populated
        if (chapters && chapters.length > 0) {
            Logger.info('Chapters to populate:');
            chapters.slice(0, 5).forEach((chapter, index) => {
                let displayTitle = chapter.title;
                if (chapter.description) {
                    displayTitle = `Chapter ${chapter.number}: ${chapter.description}`;
                } else if (chapter.title && chapter.title !== `Chapter ${chapter.number}`) {
                    displayTitle = chapter.title;
                } else {
                    displayTitle = `Chapter ${chapter.number}`;
                }
                Logger.info(`  ${index + 1}. ${chapter.order}. ${displayTitle} (${chapter.id})`);
            });
            if (chapters.length > 5) {
                Logger.info(`  ... and ${chapters.length - 5} more chapters`);
            }
        } else {
            Logger.warn('⚠️ No chapters provided to populateChapterSelector');
        }

        // Clear existing options
        chapterSelector.innerHTML = '<option value="">Select a chapter...</option>';

        // Add chapter options with descriptive titles
        chapters.forEach(chapter => {
            const option = document.createElement('option');
            option.value = chapter.id;

            // Create a more descriptive title by combining chapter number with description
            let displayTitle = chapter.title;
            if (chapter.description) {
                // Use description if available, otherwise fall back to title
                displayTitle = `Chapter ${chapter.number}: ${chapter.description}`;
            } else if (chapter.title && chapter.title !== `Chapter ${chapter.number}`) {
                // Use title if it's not just "Chapter X"
                displayTitle = chapter.title;
            } else {
                // Fallback to generic title
                displayTitle = `Chapter ${chapter.number}`;
            }

            option.textContent = displayTitle;
            chapterSelector.appendChild(option);
        });

        // Set up event listener (only once)
        if (!chapterSelector._listenerAdded) {
            chapterSelector.addEventListener('change', async (e) => {
                const selectedChapterId = e.target.value;
                if (selectedChapterId) {
                    try {
                        Logger.info(`Loading chapter: ${selectedChapterId}`);
                        await this.loadChapter(selectedChapterId);
                        Logger.info(`✅ Loaded chapter: ${selectedChapterId}`);
                    } catch (error) {
                        Logger.error(`❌ Failed to load chapter ${selectedChapterId}:`, error);
                    }
                }
            });
            chapterSelector._listenerAdded = true;
            Logger.info('✅ Chapter selector event listener added');
        } else {
            Logger.info('ℹ️ Chapter selector event listener already exists');
        }

        Logger.info(`✅ Chapter selector populated with ${chapters.length} chapters`);
    }
}

export { AppController };