/**
 * Error handling utility for the Pyodide Interactive Companion
 */

import { Logger } from './Logger.js';

class ErrorHandler {
    constructor() {
        this.errorListeners = [];
        this.recoveryStrategies = new Map();
    }

    /**
     * Initialize the error handler
     */
    async initialize() {
        try {
            Logger.info('Initializing ErrorHandler...');

            // Initialize default recovery strategies
            this.initializeDefaultStrategies();

            // Set up global error handlers
            this.setupGlobalErrorHandlers();

            Logger.info('ErrorHandler initialized successfully');
        } catch (error) {
            Logger.error('Failed to initialize ErrorHandler:', error);
            // Don't throw error, continue with basic functionality
        }
    }

    /**
     * Set up global error handlers
     */
    setupGlobalErrorHandlers() {
        // Handle unhandled promise rejections
        window.addEventListener('unhandledrejection', (event) => {
            Logger.error('Unhandled promise rejection:', event.reason);
            this.handleError(event.reason, { type: 'unhandledrejection' });
        });

        // Handle global errors
        window.addEventListener('error', (event) => {
            Logger.error('Global error:', event.error);
            this.handleError(event.error, { type: 'global' });
        });
    }

    /**
     * Register an error listener
     */
    addErrorListener(listener) {
        this.errorListeners.push(listener);
    }

    /**
     * Remove an error listener
     */
    removeErrorListener(listener) {
        const index = this.errorListeners.indexOf(listener);
        if (index > -1) {
            this.errorListeners.splice(index, 1);
        }
    }

    /**
     * Register a recovery strategy for a specific error type
     */
    registerRecoveryStrategy(errorType, strategy) {
        this.recoveryStrategies.set(errorType, strategy);
    }

    /**
     * Handle an error
     */
    handleError(error, context = {}) {
        Logger.error('Error occurred', { error: error.message, stack: error.stack, context });

        // Create error object
        const appError = {
            message: error.message,
            stack: error.stack,
            type: this.getErrorType(error),
            context,
            timestamp: Date.now(),
            recoverable: this.isRecoverable(error)
        };

        // Notify listeners
        this.errorListeners.forEach(listener => {
            try {
                listener(appError);
            } catch (listenerError) {
                Logger.error('Error in error listener', listenerError);
            }
        });

        // Try recovery strategy
        if (appError.recoverable) {
            this.attemptRecovery(appError);
        }

        return appError;
    }

    /**
     * Determine error type
     */
    getErrorType(error) {
        if (error.name === 'PyodideError') return 'PYODIDE_ERROR';
        if (error.name === 'NetworkError') return 'NETWORK_ERROR';
        if (error.name === 'StorageError') return 'STORAGE_ERROR';
        if (error.name === 'ContentError') return 'CONTENT_ERROR';
        if (error.name === 'ExecutionError') return 'EXECUTION_ERROR';
        if (error.name === 'TimeoutError') return 'TIMEOUT_ERROR';
        return 'UNKNOWN_ERROR';
    }

    /**
     * Check if error is recoverable
     */
    isRecoverable(error) {
        const nonRecoverableTypes = [
            'INITIALIZATION_ERROR',
            'CRITICAL_SYSTEM_ERROR'
        ];

        return !nonRecoverableTypes.includes(this.getErrorType(error));
    }

    /**
     * Attempt to recover from error
     */
    async attemptRecovery(error) {
        const strategy = this.recoveryStrategies.get(error.type);

        if (strategy) {
            try {
                Logger.info(`Attempting recovery for ${error.type}`);
                await strategy(error);
                Logger.info(`Recovery successful for ${error.type}`);
            } catch (recoveryError) {
                Logger.error(`Recovery failed for ${error.type}`, recoveryError);
            }
        }
    }

    /**
     * Create user-friendly error message
     */
    getUserFriendlyMessage(error) {
        const messages = {
            PYODIDE_ERROR: 'Python execution failed. Please check your code and try again.',
            NETWORK_ERROR: 'Network connection failed. Please check your internet connection.',
            STORAGE_ERROR: 'Failed to save your progress. Your changes may not be preserved.',
            CONTENT_ERROR: 'Failed to load chapter content. Please refresh the page.',
            EXECUTION_ERROR: 'Code execution failed. Please check for syntax errors.',
            TIMEOUT_ERROR: 'Operation timed out. Please try again with a smaller input.',
            UNKNOWN_ERROR: 'An unexpected error occurred. Please refresh the page.'
        };

        return messages[error.type] || messages.UNKNOWN_ERROR;
    }

    /**
     * Show error notification to user
     */
    showErrorNotification(error) {
        const message = this.getUserFriendlyMessage(error);

        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'error-notification';
        notification.innerHTML = `
      <div class="error-content">
        <span class="error-icon">⚠️</span>
        <span class="error-message">${message}</span>
        <button class="error-close" onclick="this.parentElement.parentElement.remove()">×</button>
      </div>
    `;

        // Add styles
        notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: #fee2e2;
      border: 1px solid #fecaca;
      border-radius: 8px;
      padding: 1rem;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      z-index: 1000;
      max-width: 400px;
      animation: slideIn 0.3s ease-out;
    `;

        // Add to page
        document.body.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }

    /**
     * Initialize default recovery strategies
     */
    initializeDefaultStrategies() {
        // Network error recovery
        this.registerRecoveryStrategy('NETWORK_ERROR', async (error) => {
            // Wait and retry
            await new Promise(resolve => setTimeout(resolve, 2000));
            throw new Error('Retry after network error');
        });

        // Storage error recovery
        this.registerRecoveryStrategy('STORAGE_ERROR', async (error) => {
            // Try to clear storage and retry
            try {
                localStorage.clear();
                sessionStorage.clear();
            } catch (clearError) {
                Logger.warn('Failed to clear storage', clearError);
            }
        });

        // Content error recovery
        this.registerRecoveryStrategy('CONTENT_ERROR', async (error) => {
            // Reload content
            window.location.reload();
        });
    }
}

export { ErrorHandler }; 