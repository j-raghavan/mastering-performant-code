/**
 * OutputPanel Component
 * 
 * Displays execution results, test results, error messages,
 * and performance metrics in a structured format
 */

import { Logger } from '../../utils/Logger.js';

class OutputPanel {
    constructor(container, options = {}) {
        this.container = container;
        this.options = {
            theme: 'light',
            maxOutputLines: 1000,
            ...options
        };

        this.outputHistory = [];
        this.currentExecution = null;

        this.init();
    }

    init() {
        this.createPanelStructure();
        this.bindEvents();
    }

    createPanelStructure() {
        this.container.innerHTML = `
            <div class="output-panel">
                <div class="output-panel-header">
                    <div class="output-tabs">
                        <button class="tab-btn active" data-tab="output">Output</button>
                        <button class="tab-btn" data-tab="tests">Tests</button>
                        <button class="tab-btn" data-tab="performance">Performance</button>
                    </div>
                    <div class="output-actions">
                        <button class="btn btn-secondary" id="clear-btn" title="Clear output">
                            <span class="icon">🗑️</span> Clear
                        </button>
                        <button class="btn btn-secondary" id="copy-btn" title="Copy output">
                            <span class="icon">📋</span> Copy
                        </button>
                    </div>
                </div>
                <div class="output-panel-body">
                    <div class="output-content active" id="output-content">
                        <div class="output-messages" id="output-messages"></div>
                    </div>
                    <div class="output-content" id="tests-content">
                        <div class="test-results" id="test-results"></div>
                    </div>
                    <div class="output-content" id="performance-content">
                        <div class="performance-metrics" id="performance-metrics"></div>
                    </div>
                </div>
            </div>
        `;

        this.outputMessages = this.container.querySelector('#output-messages');
        this.testResults = this.container.querySelector('#test-results');
        this.performanceMetrics = this.container.querySelector('#performance-metrics');
        this.clearBtn = this.container.querySelector('#clear-btn');
        this.copyBtn = this.container.querySelector('#copy-btn');
        this.tabButtons = this.container.querySelectorAll('.tab-btn');
        this.tabContents = this.container.querySelectorAll('.output-content');
    }

    bindEvents() {
        this.clearBtn.addEventListener('click', () => this.clearOutput());
        this.copyBtn.addEventListener('click', () => this.copyOutput());

        this.tabButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                this.switchTab(btn.dataset.tab);
            });
        });
    }

    switchTab(tabName) {
        // Update tab buttons
        this.tabButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabName);
        });

        // Update tab contents
        this.tabContents.forEach(content => {
            content.classList.toggle('active', content.id === `${tabName}-content`);
        });
    }

    displayExecutionResult(result) {
        this.currentExecution = result;

        // Add to history
        this.outputHistory.push({
            type: 'execution',
            timestamp: Date.now(),
            data: result
        });

        // Display in output tab
        this.displayOutput(result);

        // Display performance metrics
        this.displayPerformanceMetrics(result);

        // Switch to output tab
        this.switchTab('output');
    }

    displayOutput(result) {
        const outputElement = document.createElement('div');
        outputElement.className = 'execution-result';

        if (result.success) {
            outputElement.innerHTML = `
                <div class="result-header success">
                    <span class="icon">✅</span>
                    <span class="title">Execution Successful</span>
                    <span class="time">${this.formatTime(result.executionTime)}</span>
                </div>
                <div class="result-content">
                    <div class="output-text">${this.formatOutput(result.output)}</div>
                </div>
            `;
        } else {
            outputElement.innerHTML = `
                <div class="result-header error">
                    <span class="icon">❌</span>
                    <span class="title">Execution Failed</span>
                    <span class="time">${this.formatTime(result.executionTime)}</span>
                </div>
                <div class="result-content">
                    <div class="error-text">${this.formatError(result.error)}</div>
                </div>
            `;
        }

        this.outputMessages.appendChild(outputElement);
        this.scrollToBottom(this.outputMessages);
    }

    displayTestResults(results) {
        this.testResults.innerHTML = '';

        if (!results || results.length === 0) {
            this.testResults.innerHTML = '<div class="no-results">No test results available</div>';
            return;
        }

        const summary = this.calculateTestSummary(results);
        const summaryElement = document.createElement('div');
        summaryElement.className = 'test-summary';
        summaryElement.innerHTML = `
            <div class="summary-stats">
                <span class="stat passed">${summary.passed} passed</span>
                <span class="stat failed">${summary.failed} failed</span>
                <span class="stat skipped">${summary.skipped} skipped</span>
                <span class="stat total">${summary.total} total</span>
            </div>
            <div class="summary-time">Total time: ${this.formatTime(summary.totalTime)}</div>
        `;

        this.testResults.appendChild(summaryElement);

        results.forEach(test => {
            const testElement = document.createElement('div');
            testElement.className = `test-result ${test.status}`;
            testElement.innerHTML = `
                <div class="test-header">
                    <span class="test-icon">${this.getTestIcon(test.status)}</span>
                    <span class="test-name">${test.name}</span>
                    <span class="test-time">${this.formatTime(test.duration)}</span>
                </div>
                ${test.output ? `<div class="test-output">${this.formatOutput(test.output)}</div>` : ''}
                ${test.error ? `<div class="test-error">${this.formatError(test.error)}</div>` : ''}
            `;

            this.testResults.appendChild(testElement);
        });

        this.switchTab('tests');
    }

    displayPerformanceMetrics(result) {
        this.performanceMetrics.innerHTML = '';

        if (!result) return;

        const metricsElement = document.createElement('div');
        metricsElement.className = 'performance-metrics-container';

        metricsElement.innerHTML = `
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-title">Execution Time</div>
                    <div class="metric-value">${this.formatTime(result.executionTime)}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-title">Memory Usage</div>
                    <div class="metric-value">${this.formatMemory(result.memoryUsage?.used || 0)}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-title">Peak Memory</div>
                    <div class="metric-value">${this.formatMemory(result.memoryUsage?.peak || 0)}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-title">Status</div>
                    <div class="metric-value ${result.success ? 'success' : 'error'}">
                        ${result.success ? 'Success' : 'Failed'}
                    </div>
                </div>
            </div>
            ${result.warnings && result.warnings.length > 0 ? `
                <div class="warnings-section">
                    <h4>Warnings</h4>
                    <ul class="warnings-list">
                        ${result.warnings.map(warning => `<li>${warning}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
        `;

        this.performanceMetrics.appendChild(metricsElement);
    }

    calculateTestSummary(results) {
        return results.reduce((summary, test) => {
            summary[test.status]++;
            summary.total++;
            summary.totalTime += test.duration;
            return summary;
        }, { passed: 0, failed: 0, skipped: 0, total: 0, totalTime: 0 });
    }

    getTestIcon(status) {
        const icons = {
            passed: '✅',
            failed: '❌',
            skipped: '⏭️'
        };
        return icons[status] || '❓';
    }

    formatOutput(output) {
        if (!output) return '';

        // Escape HTML and preserve whitespace
        const escaped = output
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');

        // Convert to pre-formatted text
        return `<pre class="output-text">${escaped}</pre>`;
    }

    formatError(error) {
        if (!error) return '';

        // Format error with syntax highlighting
        const escaped = error
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');

        return `<pre class="error-text">${escaped}</pre>`;
    }

    formatTime(milliseconds) {
        if (milliseconds < 1000) {
            return `${milliseconds.toFixed(2)}ms`;
        } else if (milliseconds < 60000) {
            return `${(milliseconds / 1000).toFixed(2)}s`;
        } else {
            return `${(milliseconds / 60000).toFixed(2)}m`;
        }
    }

    formatMemory(bytes) {
        if (bytes < 1024) {
            return `${bytes.toFixed(0)}B`;
        } else if (bytes < 1024 * 1024) {
            return `${(bytes / 1024).toFixed(1)}KB`;
        } else {
            return `${(bytes / (1024 * 1024)).toFixed(1)}MB`;
        }
    }

    clearOutput() {
        this.outputMessages.innerHTML = '';
        this.testResults.innerHTML = '';
        this.performanceMetrics.innerHTML = '';
        this.outputHistory = [];
        this.currentExecution = null;
    }

    copyOutput() {
        const activeTab = this.container.querySelector('.tab-btn.active').dataset.tab;
        let content = '';

        switch (activeTab) {
            case 'output':
                content = this.outputMessages.textContent;
                break;
            case 'tests':
                content = this.testResults.textContent;
                break;
            case 'performance':
                content = this.performanceMetrics.textContent;
                break;
        }

        navigator.clipboard.writeText(content).then(() => {
            Logger.info('Output copied to clipboard');
        }).catch(err => {
            Logger.error('Failed to copy output:', err);
        });
    }

    scrollToBottom(element) {
        element.scrollTop = element.scrollHeight;
    }

    addMessage(message, type = 'info') {
        const messageElement = document.createElement('div');
        messageElement.className = `output-message ${type}`;
        messageElement.innerHTML = `
            <span class="message-icon">${this.getMessageIcon(type)}</span>
            <span class="message-text">${message}</span>
            <span class="message-time">${new Date().toLocaleTimeString()}</span>
        `;

        this.outputMessages.appendChild(messageElement);
        this.scrollToBottom(this.outputMessages);
    }

    getMessageIcon(type) {
        const icons = {
            info: 'ℹ️',
            success: '✅',
            warning: '⚠️',
            error: '❌'
        };
        return icons[type] || 'ℹ️';
    }

    destroy() {
        this.container.innerHTML = '';
    }
}

export { OutputPanel }; 