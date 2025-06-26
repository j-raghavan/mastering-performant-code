/**
 * Chart Panel Component
 * 
 * Handles performance visualization and chart rendering
 */

import { Logger } from '../../utils/Logger.js';

class ChartPanel {
    constructor(container, options = {}) {
        this.container = container;
        this.options = {
            theme: 'light',
            showLegend: true,
            responsive: true,
            ...options
        };

        this.charts = new Map();
        this.currentData = null;
        this.isInitialized = false;

        this.init();
    }

    init() {
        this.createLayout();
        this.loadPlotly();
        this.isInitialized = true;
        Logger.info('ChartPanel initialized');
    }

    createLayout() {
        this.container.innerHTML = `
            <div class="chart-panel">
                <div class="chart-header">
                    <h3 class="chart-title">Performance Analysis</h3>
                    <div class="chart-controls">
                        <button class="btn btn-sm btn-secondary" id="export-chart">Export</button>
                        <button class="btn btn-sm btn-secondary" id="reset-chart">Reset</button>
                    </div>
                </div>
                <div class="chart-container" id="chart-container">
                    <div class="chart-loading">Loading charts...</div>
                </div>
                <div class="chart-legend" id="chart-legend"></div>
            </div>
        `;

        this.chartContainer = this.container.querySelector('#chart-container');
        this.chartLegend = this.container.querySelector('#chart-legend');
        this.bindEvents();
    }

    async loadPlotly() {
        if (window.Plotly) {
            return;
        }

        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = 'https://cdn.plot.ly/plotly-2.27.1.min.js';
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    bindEvents() {
        const exportBtn = this.container.querySelector('#export-chart');
        const resetBtn = this.container.querySelector('#reset-chart');

        exportBtn?.addEventListener('click', () => this.exportChart());
        resetBtn?.addEventListener('click', () => this.resetChart());
    }

    /**
     * Display performance comparison chart
     */
    async displayPerformanceChart(data) {
        try {
            await this.loadPlotly();

            const chartData = this.preparePerformanceData(data);
            const layout = this.createPerformanceLayout();

            Plotly.newPlot(this.chartContainer, chartData, layout, {
                responsive: true,
                displayModeBar: true,
                modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
            });

            this.currentData = data;
            Logger.info('Performance chart displayed');

        } catch (error) {
            Logger.error('Failed to display performance chart:', error);
            this.showError('Failed to load performance chart');
        }
    }

    /**
     * Display complexity analysis chart
     */
    async displayComplexityChart(data) {
        try {
            await this.loadPlotly();

            const chartData = this.prepareComplexityData(data);
            const layout = this.createComplexityLayout();

            Plotly.newPlot(this.chartContainer, chartData, layout, {
                responsive: true,
                displayModeBar: true
            });

            this.currentData = data;
            Logger.info('Complexity chart displayed');

        } catch (error) {
            Logger.error('Failed to display complexity chart:', error);
            this.showError('Failed to load complexity chart');
        }
    }

    /**
     * Display memory usage chart
     */
    async displayMemoryChart(data) {
        try {
            await this.loadPlotly();

            const chartData = this.prepareMemoryData(data);
            const layout = this.createMemoryLayout();

            Plotly.newPlot(this.chartContainer, chartData, layout, {
                responsive: true,
                displayModeBar: true
            });

            this.currentData = data;
            Logger.info('Memory chart displayed');

        } catch (error) {
            Logger.error('Failed to display memory chart:', error);
            this.showError('Failed to load memory chart');
        }
    }

    preparePerformanceData(data) {
        const traces = [];

        if (data.algorithms) {
            data.algorithms.forEach((algo, index) => {
                traces.push({
                    x: algo.inputSizes,
                    y: algo.executionTimes,
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: algo.name,
                    line: {
                        color: this.getColor(index),
                        width: 2
                    },
                    marker: {
                        size: 6
                    }
                });
            });
        }

        return traces;
    }

    prepareComplexityData(data) {
        const traces = [];

        if (data.complexities) {
            data.complexities.forEach((complexity, index) => {
                traces.push({
                    x: complexity.inputSizes,
                    y: complexity.expectedTimes,
                    type: 'scatter',
                    mode: 'lines',
                    name: `${complexity.name} (${complexity.bigO})`,
                    line: {
                        color: this.getColor(index),
                        width: 2,
                        dash: 'dash'
                    }
                });
            });
        }

        return traces;
    }

    prepareMemoryData(data) {
        return [{
            x: data.timestamps,
            y: data.memoryUsage,
            type: 'scatter',
            mode: 'lines',
            name: 'Memory Usage',
            line: {
                color: '#3b82f6',
                width: 2
            },
            fill: 'tonexty',
            fillcolor: 'rgba(59, 130, 246, 0.1)'
        }];
    }

    createPerformanceLayout() {
        return {
            title: {
                text: 'Algorithm Performance Comparison',
                font: { size: 18 }
            },
            xaxis: {
                title: 'Input Size',
                type: 'log',
                gridcolor: '#e5e7eb'
            },
            yaxis: {
                title: 'Execution Time (ms)',
                type: 'log',
                gridcolor: '#e5e7eb'
            },
            plot_bgcolor: 'rgba(0,0,0,0)',
            paper_bgcolor: 'rgba(0,0,0,0)',
            font: {
                color: this.options.theme === 'dark' ? '#f9fafb' : '#1f2937'
            },
            legend: {
                x: 0.02,
                y: 0.98,
                bgcolor: 'rgba(255,255,255,0.8)',
                bordercolor: '#e5e7eb'
            },
            margin: {
                l: 60,
                r: 40,
                t: 60,
                b: 60
            }
        };
    }

    createComplexityLayout() {
        return {
            title: {
                text: 'Algorithm Complexity Analysis',
                font: { size: 18 }
            },
            xaxis: {
                title: 'Input Size',
                type: 'log',
                gridcolor: '#e5e7eb'
            },
            yaxis: {
                title: 'Expected Time',
                type: 'log',
                gridcolor: '#e5e7eb'
            },
            plot_bgcolor: 'rgba(0,0,0,0)',
            paper_bgcolor: 'rgba(0,0,0,0)',
            font: {
                color: this.options.theme === 'dark' ? '#f9fafb' : '#1f2937'
            },
            legend: {
                x: 0.02,
                y: 0.98,
                bgcolor: 'rgba(255,255,255,0.8)',
                bordercolor: '#e5e7eb'
            },
            margin: {
                l: 60,
                r: 40,
                t: 60,
                b: 60
            }
        };
    }

    createMemoryLayout() {
        return {
            title: {
                text: 'Memory Usage Over Time',
                font: { size: 18 }
            },
            xaxis: {
                title: 'Time',
                gridcolor: '#e5e7eb'
            },
            yaxis: {
                title: 'Memory Usage (MB)',
                gridcolor: '#e5e7eb'
            },
            plot_bgcolor: 'rgba(0,0,0,0)',
            paper_bgcolor: 'rgba(0,0,0,0)',
            font: {
                color: this.options.theme === 'dark' ? '#f9fafb' : '#1f2937'
            },
            margin: {
                l: 60,
                r: 40,
                t: 60,
                b: 60
            }
        };
    }

    getColor(index) {
        const colors = [
            '#3b82f6', '#ef4444', '#10b981', '#f59e0b',
            '#8b5cf6', '#06b6d4', '#84cc16', '#f97316'
        ];
        return colors[index % colors.length];
    }

    exportChart() {
        if (!this.currentData) {
            Logger.warn('No chart data to export');
            return;
        }

        try {
            Plotly.downloadImage(this.chartContainer, {
                format: 'png',
                filename: 'performance-chart',
                width: 800,
                height: 600
            });
        } catch (error) {
            Logger.error('Failed to export chart:', error);
        }
    }

    resetChart() {
        this.chartContainer.innerHTML = '<div class="chart-loading">No data to display</div>';
        this.currentData = null;
        Logger.info('Chart reset');
    }

    showError(message) {
        this.chartContainer.innerHTML = `
            <div class="chart-error">
                <div class="error-icon">⚠️</div>
                <div class="error-message">${message}</div>
            </div>
        `;
    }

    setTheme(theme) {
        this.options.theme = theme;
        // Re-render current chart with new theme if available
        if (this.currentData) {
            this.displayPerformanceChart(this.currentData);
        }
    }

    destroy() {
        if (this.chartContainer) {
            Plotly.purge(this.chartContainer);
        }
        this.container.innerHTML = '';
        this.charts.clear();
        Logger.info('ChartPanel destroyed');
    }
}

export { ChartPanel }; 