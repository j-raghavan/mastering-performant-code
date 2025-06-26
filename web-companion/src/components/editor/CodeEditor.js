/**
 * Code Editor Component
 * 
 * Provides syntax-highlighted code editing with CodeMirror
 */

import { Logger } from '../../utils/Logger.js';

class CodeEditor {
    constructor(container, options = {}) {
        this.container = container;
        this.options = {
            theme: 'light',
            language: 'python',
            initialValue: '',
            readOnly: false,
            lineNumbers: true,
            autoComplete: true,
            ...options
        };

        this.view = null;
        this.textarea = null;
        this.changeCallbacks = [];
        this.errorMarkers = new Map();
        this.isInitialized = false;

        this.init();
    }

    async init() {
        try {
            console.log('Initializing CodeEditor...');

            // Try to load CodeMirror dynamically
            await this.loadCodeMirror();

            if (window.CodeMirror) {
                console.log('CodeMirror loaded successfully, creating editor...');
                this.createCodeMirrorEditor();
            } else {
                console.log('CodeMirror not available, using textarea fallback...');
                this.createTextareaFallback();
            }

            this.isInitialized = true;
            console.log('CodeEditor initialized successfully');

        } catch (error) {
            console.error('Failed to initialize CodeEditor:', error);
            console.log('Falling back to textarea...');
            this.createTextareaFallback();
        }
    }

    async loadCodeMirror() {
        if (window.CodeMirror) {
            return; // Already loaded
        }

        return new Promise((resolve, reject) => {
            // Try to load CodeMirror from a reliable CDN
            const script = document.createElement('script');
            script.src = 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/codemirror.min.js';
            script.onload = () => {
                // Load CSS
                const link = document.createElement('link');
                link.rel = 'stylesheet';
                link.href = 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/codemirror.min.css';
                link.onload = () => {
                    // Load Python mode
                    const pythonScript = document.createElement('script');
                    pythonScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/python/python.min.js';
                    pythonScript.onload = resolve;
                    pythonScript.onerror = () => {
                        console.warn('Python mode failed to load, using basic mode');
                        resolve(); // Continue without Python mode
                    };
                    document.head.appendChild(pythonScript);
                };
                link.onerror = () => {
                    console.warn('CodeMirror CSS failed to load');
                    resolve(); // Continue without CSS
                };
                document.head.appendChild(link);
            };
            script.onerror = () => {
                console.warn('CodeMirror failed to load, using textarea fallback');
                reject(new Error('CodeMirror not available'));
            };
            document.head.appendChild(script);
        });
    }

    createCodeMirrorEditor() {
        // Clear container
        this.container.innerHTML = '';

        // Create textarea for CodeMirror
        const textarea = document.createElement('textarea');
        textarea.value = this.options.initialValue || '';
        this.container.appendChild(textarea);

        // Initialize CodeMirror
        this.view = window.CodeMirror.fromTextArea(textarea, {
            mode: 'python',
            theme: this.getThemeName(),
            lineNumbers: this.options.lineNumbers,
            readOnly: this.options.readOnly,
            indentUnit: 4,
            tabSize: 4,
            indentWithTabs: false,
            lineWrapping: true,
            foldGutter: true,
            gutters: this.options.lineNumbers ? ['CodeMirror-linenumbers'] : [],
            extraKeys: {
                'Tab': 'indentMore',
                'Shift-Tab': 'indentLess',
                'Ctrl-Space': 'autocomplete'
            }
        });

        // Set up event listeners
        this.view.on('change', (cm, change) => {
            this.notifyChangeCallbacks(cm.getValue());
        });

        // Apply theme
        this.applyTheme(this.options.theme);

        console.log('CodeMirror editor created successfully');
    }

    createTextareaFallback() {
        // Clear container
        this.container.innerHTML = '';

        // Create textarea
        this.textarea = document.createElement('textarea');
        this.textarea.className = 'code-editor-fallback';
        this.textarea.value = this.options.initialValue || '';
        this.textarea.style.cssText = `
            width: 100%;
            height: 100%;
            min-height: 400px;
            font-family: 'Monaco', 'Consolas', 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.6;
            padding: 16px;
            border: 1px solid #e1e5e9;
            border-radius: 8px;
            background: #ffffff;
            color: #24292e;
            resize: vertical;
            outline: none;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
            tab-size: 4;
            white-space: pre;
            overflow-wrap: normal;
            overflow-x: auto;
        `;

        // Add event listener
        this.textarea.addEventListener('input', (e) => {
            this.notifyChangeCallbacks(e.target.value);
        });

        // Add tab support and Python-like features
        this.textarea.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                e.preventDefault();
                const start = this.textarea.selectionStart;
                const end = this.textarea.selectionEnd;

                if (e.shiftKey) {
                    // Shift+Tab: Remove indentation
                    const lines = this.textarea.value.split('\n');
                    const currentLine = this.textarea.value.substring(0, start).split('\n').length - 1;
                    const lineStart = this.textarea.value.lastIndexOf('\n', start - 1) + 1;
                    const lineEnd = this.textarea.value.indexOf('\n', start);
                    const lineEndPos = lineEnd === -1 ? this.textarea.value.length : lineEnd;
                    const currentLineText = this.textarea.value.substring(lineStart, lineEndPos);

                    if (currentLineText.startsWith('    ')) {
                        const newLineText = currentLineText.substring(4);
                        this.textarea.value = this.textarea.value.substring(0, lineStart) + newLineText + this.textarea.value.substring(lineEndPos);
                        this.textarea.selectionStart = this.textarea.selectionEnd = start - 4;
                    }
                } else {
                    // Tab: Add indentation
                    this.textarea.value = this.textarea.value.substring(0, start) + '    ' + this.textarea.value.substring(end);
                    this.textarea.selectionStart = this.textarea.selectionEnd = start + 4;
                }

                // Trigger change event
                this.notifyChangeCallbacks(this.textarea.value);
            } else if (e.key === 'Enter') {
                // Auto-indent on Enter
                const start = this.textarea.selectionStart;
                const lines = this.textarea.value.split('\n');
                const currentLine = this.textarea.value.substring(0, start).split('\n').length - 1;
                const currentLineText = lines[currentLine] || '';
                const indentMatch = currentLineText.match(/^(\s*)/);
                const currentIndent = indentMatch ? indentMatch[1] : '';

                // Check if line ends with colon (Python block start)
                if (currentLineText.trim().endsWith(':')) {
                    const newIndent = currentIndent + '    ';
                    setTimeout(() => {
                        const newStart = this.textarea.selectionStart;
                        this.textarea.value = this.textarea.value.substring(0, newStart) + newIndent + this.textarea.value.substring(newStart);
                        this.textarea.selectionStart = this.textarea.selectionEnd = newStart + newIndent.length;
                    }, 0);
                }
            }
        });

        this.container.appendChild(this.textarea);
        console.log('Enhanced textarea fallback created successfully');
    }

    setValue(code) {
        if (this.view) {
            this.view.setValue(code);
        } else if (this.textarea) {
            this.textarea.value = code;
        }
    }

    getValue() {
        if (this.view) {
            return this.view.getValue();
        } else if (this.textarea) {
            return this.textarea.value;
        }
        return '';
    }

    insertText(text, position) {
        if (this.view) {
            const pos = position || this.view.getCursor();
            this.view.replaceRange(text, pos);
        }
    }

    format() {
        // Basic Python formatting - in a real implementation,
        // you might want to use a Python formatter like black
        const code = this.getValue();
        const formatted = this.formatPythonCode(code);
        this.setValue(formatted);
    }

    formatPythonCode(code) {
        // Simple formatting - indent with 4 spaces
        const lines = code.split('\n');
        const formatted = lines.map(line => {
            // Remove leading whitespace and add proper indentation
            const trimmed = line.trim();
            if (trimmed === '') return '';

            // Count leading spaces to determine indentation level
            const leadingSpaces = line.length - line.trimStart().length;
            const indentLevel = Math.floor(leadingSpaces / 4);

            return '    '.repeat(indentLevel) + trimmed;
        });

        return formatted.join('\n');
    }

    focus() {
        if (this.view) {
            this.view.focus();
        } else if (this.textarea) {
            this.textarea.focus();
        }
    }

    markError(line, message) {
        if (this.view) {
            // Add error marker
            const marker = this.view.addLineClass(line - 1, 'background', 'error-line');
            this.errorMarkers.set(line, marker);

            // Add error tooltip or annotation
            console.warn(`Error on line ${line}: ${message}`);
        } else {
            console.warn(`Error on line ${line}: ${message}`);
        }
    }

    clearErrors() {
        if (this.view) {
            // Clear all error markers
            this.errorMarkers.forEach((marker, line) => {
                this.view.removeLineClass(line - 1, 'background', 'error-line');
            });
            this.errorMarkers.clear();
        }
    }

    onCodeChange(callback) {
        this.changeCallbacks.push(callback);
    }

    notifyChangeCallbacks(code) {
        this.changeCallbacks.forEach(callback => {
            try {
                callback(code);
            } catch (error) {
                console.error('Error in change callback:', error);
            }
        });
    }

    getThemeName() {
        return this.options.theme === 'dark' ? 'monokai' : 'default';
    }

    applyTheme(theme) {
        if (this.view) {
            this.view.setOption('theme', this.getThemeName());
        }
    }

    getThemeStyles(theme) {
        const styles = {
            light: {
                background: '#ffffff',
                color: '#24292e',
                border: '#e1e5e9'
            },
            dark: {
                background: '#1f2937',
                color: '#f9fafb',
                border: '#4b5563'
            }
        };
        return styles[theme] || styles.light;
    }

    destroy() {
        if (this.view) {
            this.view.toTextArea();
            this.view = null;
        }
        if (this.textarea) {
            this.textarea.remove();
            this.textarea = null;
        }
        this.changeCallbacks = [];
        this.errorMarkers.clear();
    }

    getCursorPosition() {
        if (this.view) {
            return this.view.getCursor();
        }
        return { line: 0, ch: 0 };
    }

    setCursorPosition(position) {
        if (this.view) {
            this.view.setCursor(position);
        }
    }

    getSelectedText() {
        if (this.view) {
            return this.view.getSelection();
        }
        return '';
    }

    replaceSelection(text) {
        if (this.view) {
            this.view.replaceSelection(text);
        }
    }
}

export { CodeEditor }; 