/**
 * Code Panel Component
 * 
 * Manages multiple code files with tabs and file tree navigation
 */

import { CodeEditor } from './CodeEditor.js';
import { Logger } from '../../utils/Logger.js';

class CodePanel {
    constructor(container, options = {}) {
        this.container = container;
        this.options = {
            theme: 'light',
            showFileTree: true,
            showTabs: true,
            ...options
        };

        this.files = [];
        this.currentFile = null;
        this.editors = new Map();
        this.eventListeners = new Map();

        this.init();
    }

    init() {
        this.createPanelStructure();
        this.bindEvents();
    }

    createPanelStructure() {
        this.container.innerHTML = `
            <div class="code-panel">
                <div class="code-panel-header">
                    <div class="file-tabs" id="file-tabs"></div>
                    <div class="code-panel-actions">
                        <button class="btn btn-sm btn-primary" id="run-btn" title="Run Code">
                            <span class="icon">▶</span> Run
                        </button>
                        <button class="btn btn-sm btn-secondary" id="reset-btn" title="Reset to Original">
                            <span class="icon">↺</span> Reset
                        </button>
                        <button class="btn btn-sm btn-secondary" id="format-btn" title="Format Code">
                            <span class="icon">⚡</span> Format
                        </button>
                    </div>
                </div>
                
                <div class="code-panel-body">
                    ${this.options.showFileTree ? `
                        <div class="file-tree" id="file-tree"></div>
                    ` : ''}
                    <div class="editor-container" id="editor-container"></div>
                </div>
            </div>
        `;

        // Get references to elements
        this.fileTabs = this.container.querySelector('#file-tabs');
        this.fileTree = this.container.querySelector('#file-tree');
        this.editorContainer = this.container.querySelector('#editor-container');
        this.runBtn = this.container.querySelector('#run-btn');
        this.resetBtn = this.container.querySelector('#reset-btn');
        this.formatBtn = this.container.querySelector('#format-btn');
    }

    bindEvents() {
        // Action buttons
        this.runBtn.addEventListener('click', () => this.handleRunCode());
        this.resetBtn.addEventListener('click', () => this.handleResetCode());
        this.formatBtn.addEventListener('click', () => this.handleFormatCode());

        // File tree events (if enabled)
        if (this.fileTree) {
            this.fileTree.addEventListener('click', (e) => {
                const fileItem = e.target.closest('.file-item');
                if (fileItem) {
                    const fileId = fileItem.dataset.fileId;
                    this.selectFile(fileId);
                }
            });
        }
    }

    setFiles(files) {
        Logger.info(`Setting ${files.length} files in CodePanel`);

        this.files = files;
        this.renderFileTabs();
        this.renderFileTree();

        // Select first file if none selected
        if (files.length > 0 && !this.currentFile) {
            this.selectFile(files[0].name);
        }
    }

    renderFileTabs() {
        if (!this.fileTabs) return;

        this.fileTabs.innerHTML = '';

        this.files.forEach(file => {
            const tab = document.createElement('div');
            tab.className = `file-tab ${file.name === this.currentFile ? 'active' : ''}`;
            tab.dataset.fileId = file.name;
            tab.innerHTML = `
                <span class="tab-name">${this.getDisplayName(file.name)}</span>
                <span class="tab-close" data-file-id="${file.name}">×</span>
            `;

            // Tab click handler
            tab.addEventListener('click', (e) => {
                if (e.target.classList.contains('tab-close')) {
                    e.stopPropagation();
                    // Don't allow closing for now
                    return;
                }
                this.selectFile(file.name);
            });

            this.fileTabs.appendChild(tab);
        });
    }

    renderFileTree() {
        if (!this.fileTree) return;

        this.fileTree.innerHTML = '';

        // Group files by type
        const groups = this.groupFilesByType();

        Object.entries(groups).forEach(([groupName, groupFiles]) => {
            const groupDiv = document.createElement('div');
            groupDiv.className = 'file-group';

            const groupHeader = document.createElement('div');
            groupHeader.className = 'group-header';
            groupHeader.innerHTML = `
                <span class="group-name">${groupName}</span>
                <span class="group-count">${groupFiles.length}</span>
            `;

            const groupFilesDiv = document.createElement('div');
            groupFilesDiv.className = 'group-files';

            groupFiles.forEach(file => {
                const fileItem = document.createElement('div');
                fileItem.className = `file-item ${file.name === this.currentFile ? 'active' : ''}`;
                fileItem.dataset.fileId = file.name;
                fileItem.innerHTML = `
                    <span class="file-icon">${this.getFileIcon(file.type)}</span>
                    <span class="file-name">${this.getDisplayName(file.name)}</span>
                `;

                groupFilesDiv.appendChild(fileItem);
            });

            groupDiv.appendChild(groupHeader);
            groupDiv.appendChild(groupFilesDiv);
            this.fileTree.appendChild(groupDiv);
        });
    }

    groupFilesByType() {
        const groups = {
            'Implementation': [],
            'Demo': [],
            'Tests': [],
            'Other': []
        };

        this.files.forEach(file => {
            if (file.type === 'implementation' || file.name.includes('_array') || file.name.includes('_table')) {
                groups['Implementation'].push(file);
            } else if (file.type === 'demo' || file.name.includes('demo')) {
                groups['Demo'].push(file);
            } else if (file.name.includes('test_')) {
                groups['Tests'].push(file);
            } else {
                groups['Other'].push(file);
            }
        });

        // Remove empty groups
        Object.keys(groups).forEach(key => {
            if (groups[key].length === 0) {
                delete groups[key];
            }
        });

        return groups;
    }

    getFileIcon(type) {
        const icons = {
            'implementation': '📦',
            'demo': '🎯',
            'analyzer': '📊',
            'benchmark': '⚡',
            'test': '🧪'
        };
        return icons[type] || '📄';
    }

    getDisplayName(fileName) {
        // Remove .py extension and convert underscores to spaces
        return fileName.replace('.py', '').replace(/_/g, ' ');
    }

    selectFile(fileId) {
        Logger.info(`Selecting file: ${fileId}`);

        const file = this.files.find(f => f.name === fileId);
        if (!file) {
            Logger.error(`File not found: ${fileId}`);
            return;
        }

        this.currentFile = fileId;
        this.updateActiveTab();
        this.updateActiveFileTree();
        this.loadFileContent(file);
    }

    updateActiveTab() {
        // Update tab active state
        this.fileTabs.querySelectorAll('.file-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.fileId === this.currentFile);
        });
    }

    updateActiveFileTree() {
        if (!this.fileTree) return;

        // Update file tree active state
        this.fileTree.querySelectorAll('.file-item').forEach(item => {
            item.classList.toggle('active', item.dataset.fileId === this.currentFile);
        });
    }

    loadFileContent(file) {
        Logger.info(`Loading content for file: ${file.name}`);

        // Create editor if it doesn't exist
        if (!this.editors.has(file.name)) {
            this.createEditor(file);
        }

        // Show the editor
        this.showEditor(file.name);

        // Set content
        const editor = this.editors.get(file.name);
        if (editor) {
            editor.setValue(file.content || '');
        }
    }

    createEditor(file) {
        Logger.info(`Creating editor for file: ${file.name}`);

        const editorContainer = document.createElement('div');
        editorContainer.className = 'editor-wrapper';
        editorContainer.style.display = 'none';
        editorContainer.dataset.fileId = file.name;

        this.editorContainer.appendChild(editorContainer);

        const editor = new CodeEditor(editorContainer, {
            theme: this.options.theme,
            language: 'python',
            initialValue: file.content || '',
            lineNumbers: true
        });

        // Set up change listener
        editor.onCodeChange((code) => {
            this.handleCodeChange(file.name, code);
        });

        this.editors.set(file.name, editor);
    }

    showEditor(fileId) {
        // Hide all editors
        this.editorContainer.querySelectorAll('.editor-wrapper').forEach(wrapper => {
            wrapper.style.display = 'none';
        });

        // Show current editor
        const currentEditor = this.editorContainer.querySelector(`[data-file-id="${fileId}"]`);
        if (currentEditor) {
            currentEditor.style.display = 'block';
        }
    }

    handleCodeChange(fileId, code) {
        // Update file content
        const file = this.files.find(f => f.name === fileId);
        if (file) {
            file.content = code;
        }

        // Emit change event
        this.emit('codeChanged', { fileId, code });
    }

    handleRunCode() {
        if (!this.currentFile) {
            Logger.warn('No file selected for execution');
            return;
        }

        const editor = this.editors.get(this.currentFile);
        if (!editor) {
            Logger.error('Editor not found for current file');
            return;
        }

        const code = editor.getValue();
        Logger.info(`Running code for file: ${this.currentFile}`);

        this.emit('runCode', { fileId: this.currentFile, code });
    }

    handleResetCode() {
        if (!this.currentFile) {
            Logger.warn('No file selected for reset');
            return;
        }

        const file = this.files.find(f => f.name === this.currentFile);
        if (!file) {
            Logger.error('File not found for reset');
            return;
        }

        const editor = this.editors.get(this.currentFile);
        if (editor) {
            editor.setValue(file.content || '');
            Logger.info(`Reset code for file: ${this.currentFile}`);
        }
    }

    handleFormatCode() {
        if (!this.currentFile) {
            Logger.warn('No file selected for formatting');
            return;
        }

        const editor = this.editors.get(this.currentFile);
        if (editor) {
            editor.format();
            Logger.info(`Formatted code for file: ${this.currentFile}`);
        }
    }

    getCurrentCode() {
        if (!this.currentFile) return null;

        const editor = this.editors.get(this.currentFile);
        return editor ? editor.getValue() : null;
    }

    setCurrentCode(code) {
        if (!this.currentFile) return;

        const editor = this.editors.get(this.currentFile);
        if (editor) {
            editor.setValue(code);
        }
    }

    markError(fileId, line, message) {
        const editor = this.editors.get(fileId);
        if (editor) {
            editor.markError(line, message);
        }
    }

    clearErrors(fileId) {
        const editor = this.editors.get(fileId);
        if (editor) {
            editor.clearErrors();
        }
    }

    setTheme(theme) {
        this.options.theme = theme;
        this.editors.forEach(editor => {
            editor.applyTheme(theme);
        });
    }

    emit(event, data) {
        const callbacks = this.eventListeners.get(event) || [];
        callbacks.forEach(callback => {
            try {
                callback(data);
            } catch (error) {
                Logger.error(`Error in event callback for ${event}:`, error);
            }
        });
    }

    addEventListener(event, callback) {
        if (!this.eventListeners.has(event)) {
            this.eventListeners.set(event, []);
        }
        this.eventListeners.get(event).push(callback);
    }

    removeEventListener(event, callback) {
        const callbacks = this.eventListeners.get(event);
        if (callbacks) {
            const index = callbacks.indexOf(callback);
            if (index > -1) {
                callbacks.splice(index, 1);
            }
        }
    }

    destroy() {
        // Destroy all editors
        this.editors.forEach(editor => {
            editor.destroy();
        });
        this.editors.clear();

        // Clear event listeners
        this.eventListeners.clear();

        // Clear container
        this.container.innerHTML = '';
    }
}

export { CodePanel }; 