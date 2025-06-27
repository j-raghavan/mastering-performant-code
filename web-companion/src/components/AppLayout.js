/**
 * AppLayout Component
 * 
 * Main application layout that integrates all UI components
 * and manages the overall application structure
 */

import { NavigationBar } from './navigation/NavigationBar.js';
import { CodePanel } from './editor/CodePanel.js';
import { OutputPanel } from './output/OutputPanel.js';
import { ChartPanel } from './charts/ChartPanel.js';
import { Logger } from '../utils/Logger.js';

class AppLayout {
    constructor(container, options = {}) {
        this.container = container;
        this.options = {
            theme: 'light',
            layout: 'horizontal', // 'horizontal' or 'vertical'
            ...options
        };

        this.components = {
            navigation: null,
            codePanel: null,
            outputPanel: null,
            chartPanel: null
        };

        this.init();
    }

    init() {
        this.createLayoutStructure();
        this.initializeComponents();
        this.bindEvents();
    }

    createLayoutStructure() {
        this.container.innerHTML = `
            <div class="app-layout ${this.options.layout}">
                <header class="app-header" id="app-header"></header>
                
                <main class="app-main">
                    <div class="app-content">
                        <div class="code-section" id="code-section"></div>
                        <div class="output-section" id="output-section"></div>
                        <div class="chart-section" id="chart-section"></div>
                    </div>
                </main>
                
                <div class="app-overlay" id="app-overlay" style="display: none;">
                    <div class="overlay-content" id="overlay-content"></div>
                </div>
            </div>
        `;

        // Get references to sections
        this.headerSection = this.container.querySelector('#app-header');
        this.codeSection = this.container.querySelector('#code-section');
        this.outputSection = this.container.querySelector('#output-section');
        this.chartSection = this.container.querySelector('#chart-section');
        this.overlay = this.container.querySelector('#app-overlay');
        this.overlayContent = this.container.querySelector('#overlay-content');
    }

    initializeComponents() {
        // Initialize NavigationBar
        this.components.navigation = new NavigationBar(this.headerSection, {
            theme: this.options.theme,
            showProgress: true,
            showSearch: true
        });

        // Initialize CodePanel
        this.components.codePanel = new CodePanel(this.codeSection, {
            theme: this.options.theme,
            showFileTree: true
        });

        // Initialize OutputPanel
        this.components.outputPanel = new OutputPanel(this.outputSection, {
            theme: this.options.theme,
            maxOutputLines: 1000
        });

        // Initialize ChartPanel
        this.components.chartPanel = new ChartPanel(this.chartSection, {
            theme: this.options.theme,
            showLegend: true,
            responsive: true
        });
    }

    bindEvents() {
        // Navigation events
        this.components.navigation.addEventListener('chapterSelected', (event) => {
            this.handleChapterSelected(event.detail);
        });

        this.components.navigation.addEventListener('openSettings', (event) => {
            this.openSettings();
        });

        this.components.navigation.addEventListener('openHelp', (event) => {
            this.openHelp();
        });

        // Code panel events
        this.components.codePanel.addEventListener('runCode', (event) => {
            this.handleRunCode(event.detail);
        });

        // Search events
        this.components.navigation.onSearch((query) => {
            this.handleSearch(query);
        });
    }

    handleChapterSelected(detail) {
        const { chapter } = detail;

        // Emit event for parent components
        this.emit('chapterSelected', { chapter });

        // Update layout if needed
        this.updateLayoutForChapter(chapter);

        Logger.info(`Chapter selected in layout: ${chapter.title}`);
    }

    handleRunCode(detail) {
        const { fileId, code } = detail;

        // Emit event for parent components
        this.emit('runCode', { fileId, code });

        Logger.info(`Code run requested for file: ${fileId}`);
    }

    handleSearch(query) {
        // Emit search event
        this.emit('search', { query });

        Logger.info(`Search requested: ${query}`);
    }

    updateLayoutForChapter(chapter) {
        // Update chapter title in layout
        const titleElement = this.container.querySelector('.chapter-title');
        if (titleElement) {
            // Create a more descriptive title for display
            let displayTitle = chapter.title;
            if (chapter.description) {
                displayTitle = `Chapter ${chapter.number}: ${chapter.description}`;
            } else if (chapter.title && chapter.title !== `Chapter ${chapter.number}`) {
                displayTitle = chapter.title;
            } else {
                displayTitle = `Chapter ${chapter.number}`;
            }

            titleElement.textContent = displayTitle;
        }

        // Update progress if available
        if (chapter.progress !== undefined) {
            this.components.navigation.updateProgress(chapter.id, chapter.progress);
        }
    }

    openSettings() {
        this.showOverlay('settings', {
            title: 'Settings',
            content: this.createSettingsContent()
        });
    }

    openHelp() {
        this.showOverlay('help', {
            title: 'Help',
            content: this.createHelpContent()
        });
    }

    createSettingsContent() {
        return `
            <div class="settings-content">
                <div class="setting-group">
                    <h3>Theme</h3>
                    <select id="theme-select" class="setting-select">
                        <option value="light">Light</option>
                        <option value="dark">Dark</option>
                    </select>
                </div>
                
                <div class="setting-group">
                    <h3>Layout</h3>
                    <select id="layout-select" class="setting-select">
                        <option value="horizontal">Horizontal</option>
                        <option value="vertical">Vertical</option>
                    </select>
                </div>
                
                <div class="setting-group">
                    <h3>Editor</h3>
                    <label class="setting-checkbox">
                        <input type="checkbox" id="show-file-tree" checked>
                        Show file tree
                    </label>
                    <label class="setting-checkbox">
                        <input type="checkbox" id="auto-save" checked>
                        Auto-save changes
                    </label>
                </div>
                
                <div class="setting-actions">
                    <button class="btn btn-primary" id="save-settings">Save Settings</button>
                    <button class="btn btn-secondary" id="reset-settings">Reset to Default</button>
                </div>
            </div>
        `;
    }

    createHelpContent() {
        return `
            <div class="help-content">
                <div class="help-section">
                    <h3>Getting Started</h3>
                    <p>Welcome to the Pyodide Interactive Companion for "Mastering Performant Code"!</p>
                    <ul>
                        <li>Select a chapter from the navigation bar</li>
                        <li>Edit code in the code panel</li>
                        <li>Run code to see results in the output panel</li>
                        <li>Run tests to verify your implementations</li>
                    </ul>
                </div>
                
                <div class="help-section">
                    <h3>Keyboard Shortcuts</h3>
                    <ul>
                        <li><kbd>Ctrl+Enter</kbd> - Run current code</li>
                        <li><kbd>Ctrl+F</kbd> - Search in code</li>
                        <li><kbd>Ctrl+S</kbd> - Save changes</li>
                        <li><kbd>Ctrl+Z</kbd> - Undo</kbd></li>
                        <li><kbd>Ctrl+Y</kbd> - Redo</kbd></li>
                    </ul>
                </div>
                
                <div class="help-section">
                    <h3>Features</h3>
                    <ul>
                        <li><strong>Code Editor:</strong> Syntax highlighting, auto-completion, error marking</li>
                        <li><strong>Python Execution:</strong> Run code directly in the browser using Pyodide</li>
                        <li><strong>Test Runner:</strong> Execute unit tests with detailed results</li>
                        <li><strong>Performance Analysis:</strong> Track execution time and memory usage</li>
                        <li><strong>Progress Tracking:</strong> Monitor your learning progress</li>
                    </ul>
                </div>
            </div>
        `;
    }

    showOverlay(type, options) {
        this.overlayContent.innerHTML = `
            <div class="overlay-header">
                <h2>${options.title}</h2>
                <button class="overlay-close" id="overlay-close">×</button>
            </div>
            <div class="overlay-body">
                ${options.content}
            </div>
        `;

        this.overlay.style.display = 'flex';

        // Bind overlay events
        const closeBtn = this.overlayContent.querySelector('#overlay-close');
        closeBtn.addEventListener('click', () => this.hideOverlay());

        // Bind specific events based on type
        if (type === 'settings') {
            this.bindSettingsEvents();
        }
    }

    bindSettingsEvents() {
        const themeSelect = this.overlayContent.querySelector('#theme-select');
        const layoutSelect = this.overlayContent.querySelector('#layout-select');
        const saveBtn = this.overlayContent.querySelector('#save-settings');
        const resetBtn = this.overlayContent.querySelector('#reset-settings');

        // Set current values
        themeSelect.value = this.options.theme;
        layoutSelect.value = this.options.layout;

        saveBtn.addEventListener('click', () => {
            this.saveSettings({
                theme: themeSelect.value,
                layout: layoutSelect.value
            });
            this.hideOverlay();
        });

        resetBtn.addEventListener('click', () => {
            this.resetSettings();
        });
    }

    hideOverlay() {
        this.overlay.style.display = 'none';
    }

    saveSettings(settings) {
        // Apply settings
        this.setTheme(settings.theme);
        this.setLayout(settings.layout);

        // Save to storage
        localStorage.setItem('app-settings', JSON.stringify(settings));

        // Emit settings change event
        this.emit('settingsChanged', { settings });

        Logger.info('Settings saved:', settings);
    }

    resetSettings() {
        const defaultSettings = {
            theme: 'light',
            layout: 'horizontal'
        };

        this.saveSettings(defaultSettings);
        Logger.info('Settings reset to default');
    }

    setTheme(theme) {
        this.options.theme = theme;
        this.container.className = `app-layout ${this.options.layout} theme-${theme}`;

        // Update component themes
        this.components.navigation.setTheme(theme);
        this.components.codePanel.options.theme = theme;
        this.components.outputPanel.options.theme = theme;
        this.components.chartPanel.options.theme = theme;
    }

    setLayout(layout) {
        this.options.layout = layout;
        this.container.className = `app-layout ${layout} theme-${this.options.theme}`;
    }

    setChapters(chapters) {
        this.components.navigation.setChapters(chapters);
    }

    setFiles(files) {
        this.components.codePanel.setFiles(files);
    }

    displayExecutionResult(result) {
        this.components.outputPanel.displayExecutionResult(result);
    }

    displayTestResults(results) {
        this.components.outputPanel.displayTestResults(results);
    }

    displayPerformanceChart(data) {
        this.components.chartPanel.displayPerformanceChart(data);
    }

    displayComplexityChart(data) {
        this.components.chartPanel.displayComplexityChart(data);
    }

    displayMemoryChart(data) {
        this.components.chartPanel.displayMemoryChart(data);
    }

    markError(fileId, line, message) {
        this.components.codePanel.markError(fileId, line, message);
    }

    clearErrors(fileId) {
        this.components.codePanel.clearErrors(fileId);
    }

    showLoading(show = true) {
        this.components.navigation.showLoading(show);
    }

    emit(event, data) {
        const customEvent = new CustomEvent(event, { detail: data });
        this.container.dispatchEvent(customEvent);
    }

    destroy() {
        // Destroy all components
        Object.values(this.components).forEach(component => {
            if (component && typeof component.destroy === 'function') {
                component.destroy();
            }
        });

        // Clear container
        this.container.innerHTML = '';
    }

    addEventListener(event, callback) {
        this.container.addEventListener(event, callback);
    }

    removeEventListener(event, callback) {
        this.container.removeEventListener(event, callback);
    }
}

export { AppLayout }; 