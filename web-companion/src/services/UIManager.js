/**
 * UI Manager Service
 * 
 * Manages UI interactions and display updates
 * Adapted from pyodide-demo for web-companion architecture
 */

import { Logger } from '../utils/Logger.js';

class UIManager {
    constructor() {
        this.currentFile = null;
        this.executionLog = [];
        this.maxLogEntries = 100;
        this.isInitialized = false;
    }

    /**
     * Initialize the UI manager
     */
    async initialize() {
        try {
            Logger.info('UIManager: Starting initialization...');

            // Initialize UI elements
            this.initializeUIElements();

            // Setup event listeners
            this.setupEventListeners();

            this.isInitialized = true;
            Logger.info('UIManager: Initialization completed');

            return {
                success: true,
                message: 'UI Manager initialized successfully'
            };
        } catch (error) {
            Logger.error('UIManager: Initialization failed:', error);
            return {
                success: false,
                error: error.message,
                message: 'Failed to initialize UI Manager'
            };
        }
    }

    /**
     * Initialize UI elements
     */
    initializeUIElements() {
        // Get or create UI elements
        this.elements = {
            status: document.getElementById('status') || this.createStatusElement(),
            loadTime: document.getElementById('loadTime') || this.createMetricElement('loadTime'),
            filesLoaded: document.getElementById('filesLoaded') || this.createMetricElement('filesLoaded'),
            memoryUsage: document.getElementById('memoryUsage') || this.createMetricElement('memoryUsage'),
            fileExplorer: document.getElementById('fileExplorer') || this.createFileExplorer(),
            fileSelector: document.getElementById('fileSelector') || this.createFileSelector(),
            codeEditor: document.getElementById('codeEditor') || this.createCodeEditor(),
            output: document.getElementById('output') || this.createOutputPanel(),
            executionLog: document.getElementById('executionLog') || this.createExecutionLog(),
            runBtn: document.getElementById('runBtn') || this.createButton('runBtn', 'Run Selected File'),
            runAllBtn: document.getElementById('runAllBtn') || this.createButton('runAllBtn', 'Run All Examples'),
            runTestsBtn: document.getElementById('runTestsBtn') || this.createButton('runTestsBtn', 'Run Tests'),
            currentFile: document.getElementById('currentFile') || this.createCurrentFileDisplay()
        };

        // Set initial states
        this.setButtonsEnabled(false);
        this.updateStatus('Initializing...', 'loading');
    }

    /**
     * Create status element if it doesn't exist
     */
    createStatusElement() {
        const status = document.createElement('div');
        status.id = 'status';
        status.className = 'status loading';
        status.textContent = 'Initializing...';

        // Find a good place to insert it
        const container = document.querySelector('.container') || document.body;
        container.appendChild(status);

        return status;
    }

    /**
     * Create metric element
     */
    createMetricElement(id) {
        const element = document.createElement('span');
        element.id = id;
        element.className = 'metric-value';
        element.textContent = '--';
        return element;
    }

    /**
     * Create file explorer
     */
    createFileExplorer() {
        const explorer = document.createElement('div');
        explorer.id = 'fileExplorer';
        explorer.className = 'file-explorer';
        explorer.innerHTML = '<div class="loading-placeholder">Loading files...</div>';
        return explorer;
    }

    /**
     * Create file selector
     */
    createFileSelector() {
        const selector = document.createElement('select');
        selector.id = 'fileSelector';
        selector.disabled = true;
        selector.innerHTML = '<option value="">Select a Python file...</option>';
        return selector;
    }

    /**
     * Create code editor
     */
    createCodeEditor() {
        const editor = document.createElement('textarea');
        editor.id = 'codeEditor';
        editor.readOnly = true;
        editor.placeholder = 'Select a file to view its content...';
        return editor;
    }

    /**
     * Create output panel
     */
    createOutputPanel() {
        const output = document.createElement('div');
        output.id = 'output';
        output.className = 'output';
        output.textContent = 'Ready to run Python files...';
        return output;
    }

    /**
     * Create execution log
     */
    createExecutionLog() {
        const log = document.createElement('div');
        log.id = 'executionLog';
        log.className = 'execution-log';
        log.innerHTML = '<div class="log-entry info">System ready. Waiting for file operations...</div>';
        return log;
    }

    /**
     * Create button
     */
    createButton(id, text) {
        const button = document.createElement('button');
        button.id = id;
        button.textContent = text;
        button.disabled = true;
        return button;
    }

    /**
     * Create current file display
     */
    createCurrentFileDisplay() {
        const display = document.createElement('span');
        display.id = 'currentFile';
        display.textContent = 'None';
        return display;
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // File selector change
        if (this.elements.fileSelector) {
            this.elements.fileSelector.addEventListener('change', (e) => {
                if (e.target.value) {
                    this.onFileSelected(e.target.value);
                }
            });
        }

        // Run button
        if (this.elements.runBtn) {
            this.elements.runBtn.addEventListener('click', () => {
                this.onRunFile();
            });
        }

        // Run all button
        if (this.elements.runAllBtn) {
            this.elements.runAllBtn.addEventListener('click', () => {
                this.onRunAllFiles();
            });
        }

        // Run tests button
        if (this.elements.runTestsBtn) {
            this.elements.runTestsBtn.addEventListener('click', () => {
                this.onRunTests();
            });
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch (e.key) {
                    case 'Enter':
                        e.preventDefault();
                        this.onRunFile();
                        break;
                    case 'r':
                        e.preventDefault();
                        this.onRunAllFiles();
                        break;
                    case 't':
                        e.preventDefault();
                        this.onRunTests();
                        break;
                }
            }
        });
    }

    /**
     * Update status display
     */
    updateStatus(message, type = 'info') {
        if (this.elements.status) {
            this.elements.status.textContent = message;
            this.elements.status.className = `status ${type}`;
        }
        Logger.info(`Status: ${message}`);
    }

    /**
     * Update metrics display
     */
    updateMetrics(metrics) {
        if (metrics.loadTime && this.elements.loadTime) {
            this.elements.loadTime.textContent = `${metrics.loadTime.toFixed(0)}ms`;
        }

        if (metrics.filesLoaded && this.elements.filesLoaded) {
            this.elements.filesLoaded.textContent = metrics.filesLoaded;
        }

        if (metrics.memoryUsage && this.elements.memoryUsage) {
            const mb = (metrics.memoryUsage / 1024 / 1024).toFixed(1);
            this.elements.memoryUsage.textContent = `${mb}MB`;
        }
    }

    /**
     * Display file explorer
     */
    displayFileExplorer(files) {
        if (!this.elements.fileExplorer) return;

        if (!files || files.length === 0) {
            this.elements.fileExplorer.innerHTML = '<div class="no-files">No files found</div>';
            return;
        }

        let html = '';

        for (const category of files) {
            html += `
                <div class="file-category">
                    <h4>${category.displayName}</h4>
                    <div class="file-list">
            `;

            for (const file of category.files) {
                html += `
                    <div class="file-item" data-path="${file.path}">
                        <span class="file-name">${file.name}</span>
                        <span class="file-size">${this.formatFileSize(file.size)}</span>
                    </div>
                `;
            }

            html += `
                    </div>
                </div>
            `;
        }

        this.elements.fileExplorer.innerHTML = html;

        // Add click handlers
        const fileItems = this.elements.fileExplorer.querySelectorAll('.file-item');
        fileItems.forEach(item => {
            item.addEventListener('click', () => {
                const path = item.dataset.path;
                this.onFileSelected(path);
            });
        });
    }

    /**
     * Populate file selector
     */
    populateFileSelector(files) {
        if (!this.elements.fileSelector) return;

        // Clear existing options
        this.elements.fileSelector.innerHTML = '<option value="">Select a Python file...</option>';

        // Add files by category
        for (const category of files) {
            if (category.files.length > 0) {
                const optgroup = document.createElement('optgroup');
                optgroup.label = category.displayName;

                for (const file of category.files) {
                    const option = document.createElement('option');
                    option.value = file.path;
                    option.textContent = file.name;
                    optgroup.appendChild(option);
                }

                this.elements.fileSelector.appendChild(optgroup);
            }
        }

        this.elements.fileSelector.disabled = false;
    }

    /**
     * Display file content
     */
    displayFileContent(path, content) {
        this.currentFile = path;

        if (this.elements.codeEditor) {
            this.elements.codeEditor.value = content;
            this.elements.codeEditor.readOnly = false;
        }

        if (this.elements.currentFile) {
            this.elements.currentFile.textContent = path.split('/').pop();
        }

        this.log(`Selected file: ${path}`, 'info');
    }

    /**
     * Get current file
     */
    getCurrentFile() {
        return this.currentFile;
    }

    /**
     * Set buttons enabled/disabled
     */
    setButtonsEnabled(enabled) {
        const buttons = [this.elements.runBtn, this.elements.runAllBtn, this.elements.runTestsBtn];
        buttons.forEach(button => {
            if (button) {
                button.disabled = !enabled;
            }
        });
    }

    /**
     * Display execution result
     */
    displayExecutionResult(result) {
        if (!this.elements.output) return;

        let output = '';

        if (result.success) {
            output += `<div class="execution-success">✅ Execution completed successfully</div>`;
            if (result.output) {
                output += `<pre class="output-content">${this.escapeHtml(result.output)}</pre>`;
            }
        } else {
            output += `<div class="execution-error">❌ Execution failed</div>`;
            if (result.error) {
                output += `<pre class="error-content">${this.escapeHtml(result.error)}</pre>`;
            }
        }

        if (result.executionTime) {
            output += `<div class="execution-time">⏱️ Execution time: ${result.executionTime.toFixed(2)}ms</div>`;
        }

        this.elements.output.innerHTML = output;
    }

    /**
     * Clear output
     */
    clearOutput() {
        if (this.elements.output) {
            this.elements.output.innerHTML = '<div class="output-placeholder">Ready to run Python files...</div>';
        }
    }

    /**
     * Add log entry
     */
    log(message, type = 'info') {
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = {
            timestamp,
            message,
            type
        };

        this.executionLog.push(logEntry);

        // Keep only the last maxLogEntries
        if (this.executionLog.length > this.maxLogEntries) {
            this.executionLog.shift();
        }

        this.updateExecutionLog();
    }

    /**
     * Update execution log display
     */
    updateExecutionLog() {
        if (!this.elements.executionLog) return;

        let html = '';
        for (const entry of this.executionLog) {
            html += `<div class="log-entry ${entry.type}">[${entry.timestamp}] ${this.escapeHtml(entry.message)}</div>`;
        }

        this.elements.executionLog.innerHTML = html;
        this.elements.executionLog.scrollTop = this.elements.executionLog.scrollHeight;
    }

    /**
     * Clear execution log
     */
    clearLog() {
        this.executionLog = [];
        this.updateExecutionLog();
    }

    /**
     * Show notification
     */
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;

        // Add to page
        document.body.appendChild(notification);

        // Remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }

    /**
     * Format file size
     */
    formatFileSize(bytes) {
        if (bytes < 1024) return `${bytes}B`;
        if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
        return `${(bytes / 1024 / 1024).toFixed(1)}MB`;
    }

    /**
     * Escape HTML
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Event handlers - these will be overridden by the app controller
     */
    onFileSelected(path) {
        Logger.info(`File selected: ${path}`);
        // This will be handled by the app controller
    }

    onRunFile() {
        Logger.info('Run file requested');
        // This will be handled by the app controller
    }

    onRunAllFiles() {
        Logger.info('Run all files requested');
        // This will be handled by the app controller
    }

    onRunTests() {
        Logger.info('Run tests requested');
        // This will be handled by the app controller
    }

    /**
     * Set event handlers
     */
    setEventHandlers(handlers) {
        if (handlers.onFileSelected) {
            this.onFileSelected = handlers.onFileSelected;
        }
        if (handlers.onRunFile) {
            this.onRunFile = handlers.onRunFile;
        }
        if (handlers.onRunAllFiles) {
            this.onRunAllFiles = handlers.onRunAllFiles;
        }
        if (handlers.onRunTests) {
            this.onRunTests = handlers.onRunTests;
        }
    }
}

export { UIManager }; 