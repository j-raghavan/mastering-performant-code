/**
 * PerformanceAnalyzer Service
 * 
 * Analyzes execution results, tracks performance metrics,
 * and provides complexity analysis for algorithms
 */

import { Logger } from '../utils/Logger.js';

class PerformanceAnalyzer {
    constructor() {
        this.executionHistory = [];
        this.performanceMetrics = new Map();
        this.complexityData = new Map();
    }

    /**
     * Initialize the performance analyzer
     */
    async initialize() {
        try {
            Logger.info('Initializing PerformanceAnalyzer...');

            // Load saved metrics from localStorage if available
            await this.loadSavedMetrics();

            Logger.info('PerformanceAnalyzer initialized successfully');
        } catch (error) {
            Logger.error('Failed to initialize PerformanceAnalyzer:', error);
            // Don't throw error, continue with empty metrics
        }
    }

    /**
     * Load saved metrics from localStorage
     */
    async loadSavedMetrics() {
        try {
            const savedMetrics = localStorage.getItem('performance-metrics');
            if (savedMetrics) {
                const metricsData = JSON.parse(savedMetrics);
                this.performanceMetrics = new Map(Object.entries(metricsData.metrics || {}));
                this.executionHistory = metricsData.history || [];
                Logger.info('Performance metrics loaded from localStorage');
            }
        } catch (error) {
            Logger.warn('Failed to load performance metrics:', error);
        }
    }

    /**
     * Save metrics to localStorage
     */
    async saveMetrics() {
        try {
            const metricsData = {
                metrics: Object.fromEntries(this.performanceMetrics),
                history: this.executionHistory.slice(-50) // Keep last 50 entries
            };
            localStorage.setItem('performance-metrics', JSON.stringify(metricsData));
        } catch (error) {
            Logger.warn('Failed to save performance metrics:', error);
        }
    }

    analyzeExecution(result) {
        const metrics = {
            executionTime: result.executionTime,
            memoryUsage: result.memoryUsage,
            success: result.success,
            timestamp: Date.now(),
            warnings: result.warnings || []
        };

        // Store in history
        this.executionHistory.push({
            id: result.id,
            metrics,
            timestamp: Date.now()
        });

        // Limit history size
        if (this.executionHistory.length > 100) {
            this.executionHistory.shift();
        }

        // Analyze complexity if possible
        const complexity = this.analyzeComplexity(result);
        metrics.complexity = complexity;

        // Store metrics
        this.performanceMetrics.set(result.id, metrics);

        // Auto-save metrics
        this.saveMetrics();

        Logger.info(`Performance analysis completed for execution ${result.id}`);

        return metrics;
    }

    analyzeComplexity(result) {
        // Basic complexity analysis based on code structure
        const code = result.code || '';
        const lines = code.split('\n');

        const complexity = {
            timeComplexity: 'O(1)',
            spaceComplexity: 'O(1)',
            confidence: 'low'
        };

        // Analyze loops and nested structures
        let maxNesting = 0;
        let currentNesting = 0;
        let hasLoops = false;
        let hasNestedLoops = false;

        for (const line of lines) {
            const trimmed = line.trim();

            // Check for loop constructs
            if (trimmed.startsWith('for ') || trimmed.startsWith('while ')) {
                hasLoops = true;
                currentNesting++;
                maxNesting = Math.max(maxNesting, currentNesting);
            }

            // Check for nested loops
            if (hasLoops && (trimmed.startsWith('for ') || trimmed.startsWith('while '))) {
                hasNestedLoops = true;
            }

            // Check for function calls that might indicate recursion
            if (trimmed.includes('(') && !trimmed.includes('=')) {
                // This is a very basic heuristic
            }
        }

        // Determine time complexity
        if (hasNestedLoops) {
            complexity.timeComplexity = 'O(n²)';
            complexity.confidence = 'medium';
        } else if (hasLoops) {
            complexity.timeComplexity = 'O(n)';
            complexity.confidence = 'medium';
        }

        // Analyze space complexity (basic heuristic)
        const variables = this.countVariables(code);
        if (variables > 10) {
            complexity.spaceComplexity = 'O(n)';
        }

        return complexity;
    }

    countVariables(code) {
        // Simple variable counting heuristic
        const variablePatterns = [
            /\b\w+\s*=/g,  // Assignment patterns
            /\bdef\s+\w+/g,  // Function definitions
            /\bclass\s+\w+/g,  // Class definitions
            /\bimport\s+\w+/g,  // Import statements
        ];

        let count = 0;
        for (const pattern of variablePatterns) {
            const matches = code.match(pattern);
            if (matches) {
                count += matches.length;
            }
        }

        return count;
    }

    compareAlgorithms(results) {
        if (results.length < 2) {
            return {
                comparison: 'insufficient_data',
                message: 'Need at least 2 algorithms to compare'
            };
        }

        const comparison = {
            algorithms: results.map(result => ({
                id: result.id,
                name: result.name || `Algorithm ${result.id}`,
                executionTime: result.executionTime,
                memoryUsage: result.memoryUsage?.used || 0,
                success: result.success
            })),
            fastest: null,
            mostEfficient: null,
            recommendations: []
        };

        // Find fastest algorithm
        const successfulResults = comparison.algorithms.filter(alg => alg.success);
        if (successfulResults.length > 0) {
            comparison.fastest = successfulResults.reduce((fastest, current) =>
                current.executionTime < fastest.executionTime ? current : fastest
            );
        }

        // Find most memory efficient
        if (successfulResults.length > 0) {
            comparison.mostEfficient = successfulResults.reduce((most, current) =>
                current.memoryUsage < most.memoryUsage ? current : most
            );
        }

        // Generate recommendations
        comparison.recommendations = this.generateRecommendations(comparison);

        return comparison;
    }

    generateRecommendations(comparison) {
        const recommendations = [];

        if (comparison.algorithms.length >= 2) {
            const timeRange = Math.max(...comparison.algorithms.map(a => a.executionTime)) -
                Math.min(...comparison.algorithms.map(a => a.executionTime));
            const timeRatio = timeRange / Math.min(...comparison.algorithms.map(a => a.executionTime));

            if (timeRatio > 10) {
                recommendations.push({
                    type: 'performance',
                    message: 'Significant performance differences detected. Consider optimizing slower algorithms.',
                    priority: 'high'
                });
            }

            const memoryRange = Math.max(...comparison.algorithms.map(a => a.memoryUsage)) -
                Math.min(...comparison.algorithms.map(a => a.memoryUsage));
            const memoryRatio = memoryRange / Math.min(...comparison.algorithms.map(a => a.memoryUsage));

            if (memoryRatio > 5) {
                recommendations.push({
                    type: 'memory',
                    message: 'Significant memory usage differences detected. Consider memory optimization.',
                    priority: 'medium'
                });
            }
        }

        return recommendations;
    }

    generateComplexityChart(data) {
        // Implementation for generating complexity charts
        return {
            type: 'line',
            data: {
                labels: data.labels || [],
                datasets: [{
                    label: 'Time Complexity',
                    data: data.timeComplexity || [],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        };
    }

    trackMemoryUsage(callback) {
        // Set up memory tracking
        const trackMemory = () => {
            if (window.performance && window.performance.memory) {
                const memoryInfo = {
                    used: window.performance.memory.usedJSHeapSize,
                    total: window.performance.memory.totalJSHeapSize,
                    limit: window.performance.memory.jsHeapSizeLimit,
                    timestamp: Date.now()
                };
                callback(memoryInfo);
            }
        };

        // Track memory every 5 seconds
        const intervalId = setInterval(trackMemory, 5000);
        trackMemory(); // Initial call

        // Return function to stop tracking
        return () => clearInterval(intervalId);
    }

    getPerformanceTrends(algorithmId, timeRange = 3600000) { // Default 1 hour
        const now = Date.now();
        const cutoff = now - timeRange;

        const relevantHistory = this.executionHistory.filter(entry => {
            return entry.id === algorithmId && entry.timestamp > cutoff;
        });

        if (relevantHistory.length < 2) {
            return {
                trend: 'insufficient_data',
                message: 'Not enough data for trend analysis'
            };
        }

        const executionTimes = relevantHistory.map(entry => entry.metrics.executionTime);
        const trend = this.calculateTrend(executionTimes);

        return {
            trend: trend.direction,
            slope: trend.slope,
            confidence: trend.confidence,
            dataPoints: relevantHistory.length,
            averageTime: executionTimes.reduce((a, b) => a + b, 0) / executionTimes.length,
            minTime: Math.min(...executionTimes),
            maxTime: Math.max(...executionTimes)
        };
    }

    calculateTrend(values) {
        const n = values.length;
        if (n < 2) {
            return { direction: 'stable', slope: 0, confidence: 'low' };
        }

        // Calculate linear regression
        const xValues = Array.from({ length: n }, (_, i) => i);
        const sumX = xValues.reduce((a, b) => a + b, 0);
        const sumY = values.reduce((a, b) => a + b, 0);
        const sumXY = xValues.reduce((sum, x, i) => sum + x * values[i], 0);
        const sumXX = xValues.reduce((sum, x) => sum + x * x, 0);

        const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
        const intercept = (sumY - slope * sumX) / n;

        // Calculate R-squared for confidence
        const yMean = sumY / n;
        const ssRes = values.reduce((sum, y, i) => {
            const yPred = slope * xValues[i] + intercept;
            return sum + Math.pow(y - yPred, 2);
        }, 0);
        const ssTot = values.reduce((sum, y) => sum + Math.pow(y - yMean, 2), 0);
        const rSquared = 1 - (ssRes / ssTot);

        let direction = 'stable';
        if (Math.abs(slope) > 0.01) {
            direction = slope > 0 ? 'increasing' : 'decreasing';
        }

        let confidence = 'low';
        if (rSquared > 0.7) confidence = 'high';
        else if (rSquared > 0.3) confidence = 'medium';

        return { direction, slope, confidence, rSquared };
    }

    getExecutionHistory(limit = 50) {
        return this.executionHistory.slice(-limit);
    }

    clearHistory() {
        this.executionHistory = [];
        this.performanceMetrics.clear();
        this.saveMetrics();
        Logger.info('Performance history cleared');
    }

    exportMetrics() {
        return {
            metrics: Object.fromEntries(this.performanceMetrics),
            history: this.executionHistory,
            exportDate: new Date().toISOString()
        };
    }

    importMetrics(data) {
        if (data.metrics) {
            this.performanceMetrics = new Map(Object.entries(data.metrics));
        }
        if (data.history) {
            this.executionHistory = data.history;
        }
        this.saveMetrics();
        Logger.info('Performance metrics imported');
    }
}

export { PerformanceAnalyzer }; 