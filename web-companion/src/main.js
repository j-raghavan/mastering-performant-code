/**
 * Main application entry point for the Pyodide Interactive Companion
 */

import { AppController } from './services/AppController.js';
import { ChapterManager } from './services/ChapterManager.js';
import { StorageService } from './services/StorageService.js';
import { PyodideExecutor } from './services/PyodideExecutor.js';
import { ContentSyncService } from './services/ContentSyncService.js';
import { StateManager } from './data/StateManager.js';
import { ErrorHandler } from './utils/ErrorHandler.js';
import { Logger } from './utils/Logger.js';

// Global application instance
let app = null;

/**
 * Initialize the application
 */
async function initializeApp() {
  try {
    Logger.info('🚀 Initializing Pyodide Interactive Companion...');

    // Record start time for metrics
    const startTime = performance.now();

    // Initialize services
    const stateManager = new StateManager();
    const storageService = new StorageService();
    const contentSyncService = new ContentSyncService();
    const pyodideExecutor = new PyodideExecutor();
    const chapterManager = new ChapterManager(contentSyncService);
    const errorHandler = new ErrorHandler();

    // Initialize app controller
    app = new AppController({
      stateManager,
      storageService,
      contentSyncService,
      pyodideExecutor,
      chapterManager,
      errorHandler
    });

    // Store start time for metrics
    app.startTime = startTime;

    // Initialize the application
    await app.initialize();

    // Make app globally accessible for debugging
    window.app = app;

    Logger.info('✅ Application initialized successfully');

    // Don't automatically load a chapter - let users select from the dropdown
    // await app.loadChapter('chapter_01');

  } catch (error) {
    Logger.error('❌ Failed to initialize application:', error);
    showErrorScreen(error);
  }
}

/**
 * Show error notification
 */
function showErrorNotification(message) {
  // Create notification element
  const notification = document.createElement('div');
  notification.className = 'notification error';
  notification.textContent = message;

  // Add to page
  document.body.appendChild(notification);

  // Remove after 5 seconds
  setTimeout(() => {
    if (notification.parentNode) {
      notification.parentNode.removeChild(notification);
    }
  }, 5000);
}

/**
 * Show error screen
 */
function showErrorScreen(error) {
  const container = document.querySelector('.container');
  if (container) {
    container.innerHTML = `
      <div style="text-align: center; padding: 50px;">
        <h1 style="color: #dc2626;">❌ Application Error</h1>
        <p style="color: #6b7280; margin: 20px 0;">Failed to initialize the application</p>
        <div style="background: #fee2e2; border: 1px solid #fecaca; border-radius: 8px; padding: 20px; margin: 20px 0; text-align: left;">
          <h3>Error Details:</h3>
          <pre style="color: #991b1b; font-size: 0.875rem; overflow-x: auto;">${error.message}</pre>
          ${error.stack ? `<details><summary>Stack Trace</summary><pre style="color: #991b1b; font-size: 0.75rem; overflow-x: auto;">${error.stack}</pre></details>` : ''}
        </div>
        <button onclick="location.reload()" style="background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer;">
          Reload Application
        </button>
      </div>
    `;
  }
}

/**
 * Handle unhandled errors
 */
window.addEventListener('error', (event) => {
  Logger.error('Unhandled error:', event.error);
  if (app && app.errorHandler) {
    app.errorHandler.handleError(event.error);
  }
});

window.addEventListener('unhandledrejection', (event) => {
  Logger.error('Unhandled promise rejection:', event.reason);
  if (app && app.errorHandler) {
    app.errorHandler.handleError(event.reason);
  }
});

/**
 * Handle page visibility changes
 */
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    // Page is hidden, save state
    if (app) {
      app.saveUserProgress();
    }
  }
});

/**
 * Handle beforeunload
 */
window.addEventListener('beforeunload', () => {
  if (app) {
    app.saveUserProgress();
  }
});

/**
 * Initialize the application when DOM is ready
 */
function ensureDOMReady() {
  return new Promise((resolve) => {
    if (document.readyState === 'complete') {
      resolve();
    } else if (document.readyState === 'interactive') {
      // DOM is parsed but subresources may still be loading
      document.addEventListener('DOMContentLoaded', resolve, { once: true });
    } else {
      // DOM is still loading
      document.addEventListener('DOMContentLoaded', resolve, { once: true });
    }

    // Fallback: also listen for load event
    window.addEventListener('load', resolve, { once: true });
  });
}

// Initialize the application when DOM is fully ready
ensureDOMReady().then(() => {
  // Add a small delay to ensure all elements are available
  setTimeout(initializeApp, 100);
}).catch((error) => {
  Logger.error('Failed to wait for DOM ready:', error);
  // Fallback: try to initialize anyway
  initializeApp();
});

// Export for debugging
window.initializeApp = initializeApp; 