/**
 * State Manager for the Pyodide Interactive Companion
 */

import { Logger } from '../utils/Logger.js';

class StateManager {
    constructor() {
        this.state = {
            currentChapter: null,
            currentFile: null,
            userCode: {},
            executionResults: [],
            testResults: [],
            performanceMetrics: [],
            isLoading: false,
            error: null,
            theme: 'light'
        };

        this.subscribers = new Map();
        this.history = [];
        this.historyIndex = -1;
        this.maxHistorySize = 50;
    }

    /**
     * Initialize the state manager
     */
    async initialize() {
        try {
            Logger.info('Initializing StateManager...');

            // Load saved state from localStorage if available
            await this.loadSavedState();

            Logger.info('StateManager initialized successfully');
        } catch (error) {
            Logger.error('Failed to initialize StateManager:', error);
            // Don't throw error, continue with default state
        }
    }

    /**
     * Load saved state from localStorage
     */
    async loadSavedState() {
        try {
            const savedState = localStorage.getItem('app-state');
            if (savedState) {
                const parsedState = JSON.parse(savedState);
                // Only restore safe state properties
                const safeUpdates = {
                    theme: parsedState.theme || 'light',
                    userCode: parsedState.userCode || {}
                };
                this.setState(safeUpdates);
                Logger.info('Saved state loaded from localStorage');
            }
        } catch (error) {
            Logger.warn('Failed to load saved state:', error);
        }
    }

    /**
     * Save current state to localStorage
     */
    async saveState() {
        try {
            const stateToSave = {
                theme: this.state.theme,
                userCode: this.state.userCode
            };
            localStorage.setItem('app-state', JSON.stringify(stateToSave));
        } catch (error) {
            Logger.warn('Failed to save state:', error);
        }
    }

    /**
     * Get current state
     */
    getState() {
        return { ...this.state };
    }

    /**
     * Update state
     */
    setState(updates) {
        const previousState = { ...this.state };

        // Update state
        this.state = { ...this.state, ...updates };

        // Add to history
        this.addToHistory(previousState);

        // Notify subscribers
        this.notifySubscribers(updates);

        // Auto-save state
        this.saveState();

        Logger.debug('State updated', updates);
    }

    /**
     * Subscribe to state changes
     */
    subscribe(key, callback) {
        if (!this.subscribers.has(key)) {
            this.subscribers.set(key, []);
        }
        this.subscribers.get(key).push(callback);

        // Return unsubscribe function
        return () => {
            const callbacks = this.subscribers.get(key);
            if (callbacks) {
                const index = callbacks.indexOf(callback);
                if (index > -1) {
                    callbacks.splice(index, 1);
                }
            }
        };
    }

    /**
     * Notify subscribers of state changes
     */
    notifySubscribers(updates) {
        Object.keys(updates).forEach(key => {
            const callbacks = this.subscribers.get(key);
            if (callbacks) {
                callbacks.forEach(callback => {
                    try {
                        callback(this.state[key], updates[key]);
                    } catch (error) {
                        Logger.error(`Error in state subscriber for ${key}`, error);
                    }
                });
            }
        });
    }

    /**
     * Add state to history
     */
    addToHistory(state) {
        // Remove future history if we're not at the end
        if (this.historyIndex < this.history.length - 1) {
            this.history = this.history.slice(0, this.historyIndex + 1);
        }

        // Add new state
        this.history.push(state);
        this.historyIndex++;

        // Limit history size
        if (this.history.length > this.maxHistorySize) {
            this.history.shift();
            this.historyIndex--;
        }
    }

    /**
     * Undo last state change
     */
    undo() {
        if (this.historyIndex > 0) {
            this.historyIndex--;
            const previousState = this.history[this.historyIndex];
            this.state = { ...previousState };
            this.notifySubscribers(this.state);
            return true;
        }
        return false;
    }

    /**
     * Redo last undone state change
     */
    redo() {
        if (this.historyIndex < this.history.length - 1) {
            this.historyIndex++;
            const nextState = this.history[this.historyIndex];
            this.state = { ...nextState };
            this.notifySubscribers(this.state);
            return true;
        }
        return false;
    }

    /**
     * Set current chapter
     */
    setCurrentChapter(chapter) {
        this.setState({ currentChapter: chapter });
    }

    /**
     * Get current chapter
     */
    getCurrentChapter() {
        return this.state.currentChapter;
    }

    /**
     * Set current file
     */
    setCurrentFile(file) {
        this.setState({ currentFile: file });
    }

    /**
     * Get current file
     */
    getCurrentFile() {
        return this.state.currentFile;
    }

    /**
     * Update user code
     */
    updateUserCode(chapterId, fileId, code) {
        const key = `${chapterId}:${fileId}`;
        const userCode = { ...this.state.userCode, [key]: code };
        this.setState({ userCode });
    }

    /**
     * Get user code for a file
     */
    getUserCode(chapterId, fileId) {
        const key = `${chapterId}:${fileId}`;
        return this.state.userCode[key] || null;
    }

    /**
     * Add execution result
     */
    addExecutionResult(result) {
        const executionResults = [...this.state.executionResults, result];
        this.setState({ executionResults });
    }

    /**
     * Get execution results
     */
    getExecutionResults() {
        return this.state.executionResults;
    }

    /**
     * Add test result
     */
    addTestResult(result) {
        const testResults = [...this.state.testResults, result];
        this.setState({ testResults });
    }

    /**
     * Get test results
     */
    getTestResults() {
        return this.state.testResults;
    }

    /**
     * Add performance metric
     */
    addPerformanceMetric(metric) {
        const performanceMetrics = [...this.state.performanceMetrics, metric];
        this.setState({ performanceMetrics });
    }

    /**
     * Set loading state
     */
    setLoading(isLoading) {
        this.setState({ isLoading });
    }

    /**
     * Set error state
     */
    setError(error) {
        this.setState({ error });
    }

    /**
     * Clear error state
     */
    clearError() {
        this.setState({ error: null });
    }

    /**
     * Toggle theme
     */
    toggleTheme() {
        const newTheme = this.state.theme === 'light' ? 'dark' : 'light';
        this.setState({ theme: newTheme });
    }

    /**
     * Reset state for a specific chapter
     */
    resetChapterState(chapterId) {
        // Remove user code for this chapter
        const userCode = { ...this.state.userCode };
        Object.keys(userCode).forEach(key => {
            if (key.startsWith(`${chapterId}:`)) {
                delete userCode[key];
            }
        });

        this.setState({ userCode });
    }

    /**
     * Clear all state
     */
    clearAll() {
        this.state = {
            currentChapter: null,
            currentFile: null,
            userCode: {},
            executionResults: [],
            testResults: [],
            performanceMetrics: [],
            isLoading: false,
            error: null,
            theme: this.state.theme // Keep theme preference
        };

        this.history = [];
        this.historyIndex = -1;

        this.notifySubscribers(this.state);
        this.saveState();
    }

    /**
     * Reset to initial state
     */
    reset() {
        this.clearAll();
    }

    /**
     * Export current state
     */
    exportState() {
        return {
            state: this.state,
            history: this.history,
            historyIndex: this.historyIndex
        };
    }

    /**
     * Import state
     */
    importState(data) {
        if (data.state) {
            this.state = { ...data.state };
        }
        if (data.history) {
            this.history = [...data.history];
            this.historyIndex = data.historyIndex || -1;
        }

        this.notifySubscribers(this.state);
        this.saveState();
    }
}

export { StateManager }; 