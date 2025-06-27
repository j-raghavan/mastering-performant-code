/**
 * Package Status Panel Component
 * 
 * Displays the status of the mastering_performant_code package installation
 */

class PackageStatusPanel {
    constructor(containerId = 'package-status-panel') {
        this.containerId = containerId;
        this.container = null;
        this.packageManager = null;
        this.isVisible = false;
    }

    /**
     * Initialize the panel
     */
    init(packageManager) {
        this.packageManager = packageManager;
        this.createPanel();
        this.setupEventListeners();
        this.updateDisplay();
    }

    /**
     * Create the panel HTML
     */
    createPanel() {
        // Find or create container
        this.container = document.getElementById(this.containerId);
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = this.containerId;
            this.container.className = 'package-status-panel';
            this.container.style.display = 'none'; // Hide by default

            // Add to page if not already present
            const existingPanel = document.querySelector('.package-status-panel');
            if (!existingPanel) {
                document.body.appendChild(this.container);
            }
        }

        this.container.innerHTML = `
            <div class="package-status-header">
                <h3>📦 Package Status</h3>
                <button class="package-status-toggle" onclick="this.parentElement.parentElement.classList.toggle('collapsed')">
                    <span class="toggle-icon">▼</span>
                </button>
            </div>
            <div class="package-status-content">
                <div class="package-info">
                    <div class="package-name">mastering_performant_code</div>
                    <div class="package-version">v1.0.0</div>
                </div>
                <div class="package-status">
                    <div class="status-indicator">
                        <span class="status-dot" id="status-dot"></span>
                        <span class="status-text" id="status-text">Unknown</span>
                    </div>
                </div>
                <div class="package-progress" id="package-progress" style="display: none;">
                    <div class="progress-bar">
                        <div class="progress-fill" id="progress-fill"></div>
                    </div>
                    <div class="progress-text" id="progress-text">Initializing...</div>
                </div>
                <div class="package-actions">
                    <button class="btn btn-secondary" id="verify-btn" onclick="window.packageStatusPanel.verifyPackage()" style="display: none;">
                        Verify Installation
                    </button>
                    <button class="btn btn-danger" id="reset-btn" onclick="window.packageStatusPanel.resetPackage()" style="display: none;">
                        Reset
                    </button>
                    <button class="btn btn-primary" id="retry-btn" onclick="window.packageStatusPanel.retryInstall()" style="display: none;">
                        Retry Installation
                    </button>
                </div>
                <div class="package-diagnostics" id="package-diagnostics" style="display: none;">
                    <h4>Installation Details</h4>
                    <div class="diagnostic-content" id="diagnostic-content"></div>
                </div>
            </div>
        `;

        // Add styles
        this.addStyles();
    }

    /**
     * Add CSS styles for the panel
     */
    addStyles() {
        if (document.getElementById('package-status-styles')) {
            return; // Styles already added
        }

        const style = document.createElement('style');
        style.id = 'package-status-styles';
        style.textContent = `
            .package-status-panel {
                position: fixed;
                top: 20px;
                right: 20px;
                width: 350px;
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                z-index: 1000;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                transition: all 0.3s ease;
                display: none; /* Hidden by default */
            }

            .package-status-panel.collapsed .package-status-content {
                display: none;
            }

            .package-status-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px 16px;
                background: #f8f9fa;
                border-bottom: 1px solid #ddd;
                border-radius: 8px 8px 0 0;
            }

            .package-status-header h3 {
                margin: 0;
                font-size: 14px;
                font-weight: 600;
                color: #333;
            }

            .package-status-toggle {
                background: none;
                border: none;
                cursor: pointer;
                padding: 4px;
                border-radius: 4px;
                transition: background-color 0.2s;
            }

            .package-status-toggle:hover {
                background-color: #e9ecef;
            }

            .package-status-content {
                padding: 16px;
            }

            .package-info {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
            }

            .package-name {
                font-weight: 600;
                color: #333;
            }

            .package-version {
                color: #666;
                font-size: 12px;
            }

            .package-status {
                margin-bottom: 12px;
            }

            .status-indicator {
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .status-dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background-color: #ccc;
            }

            .status-dot.installed {
                background-color: #28a745;
            }

            .status-dot.installing {
                background-color: #ffc107;
                animation: pulse 1.5s infinite;
            }

            .status-dot.error {
                background-color: #dc3545;
            }

            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }

            .status-text {
                font-size: 14px;
                color: #333;
            }

            .package-progress {
                margin-bottom: 12px;
            }

            .progress-bar {
                width: 100%;
                height: 6px;
                background-color: #e9ecef;
                border-radius: 3px;
                overflow: hidden;
                margin-bottom: 8px;
            }

            .progress-fill {
                height: 100%;
                background-color: #007bff;
                width: 0%;
                transition: width 0.3s ease;
            }

            .progress-text {
                font-size: 12px;
                color: #666;
                text-align: center;
            }

            .package-actions {
                display: flex;
                gap: 8px;
                margin-bottom: 12px;
            }

            .btn {
                padding: 6px 12px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 12px;
                transition: background-color 0.2s;
            }

            .btn-primary {
                background-color: #007bff;
                color: white;
            }

            .btn-primary:hover {
                background-color: #0056b3;
            }

            .btn-secondary {
                background-color: #6c757d;
                color: white;
            }

            .btn-secondary:hover {
                background-color: #545b62;
            }

            .btn-danger {
                background-color: #dc3545;
                color: white;
            }

            .btn-danger:hover {
                background-color: #c82333;
            }

            .package-diagnostics {
                border-top: 1px solid #ddd;
                padding-top: 12px;
            }

            .package-diagnostics h4 {
                margin: 0 0 8px 0;
                font-size: 12px;
                color: #333;
            }

            .diagnostic-content {
                font-size: 11px;
                color: #666;
                background: #f8f9fa;
                padding: 8px;
                border-radius: 4px;
                max-height: 100px;
                overflow-y: auto;
            }
        `;

        document.head.appendChild(style);
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Set up progress callback
        if (this.packageManager) {
            this.packageManager.setProgressCallback((progress) => {
                this.updateProgress(progress);
            });
        }
    }

    /**
     * Update the display based on current state
     */
    updateDisplay() {
        if (!this.container) return;

        const statusDot = document.getElementById('status-dot');
        const statusText = document.getElementById('status-text');
        const verifyBtn = document.getElementById('verify-btn');
        const resetBtn = document.getElementById('reset-btn');
        const progressDiv = document.getElementById('package-progress');
        const retryBtn = document.getElementById('retry-btn');

        if (!this.packageManager) {
            statusDot.className = 'status-dot error';
            statusText.textContent = 'Not initialized';
            verifyBtn.style.display = 'none';
            resetBtn.style.display = 'none';
            retryBtn.style.display = 'none';
            return;
        }

        const packageInfo = this.packageManager.getPackageInfo();
        const progress = this.packageManager.getInstallationProgress();

        // Update status
        if (packageInfo.isInstalled) {
            statusDot.className = 'status-dot installed';
            statusText.textContent = 'Installed';
            verifyBtn.style.display = 'inline-block';
            resetBtn.style.display = 'inline-block';
            progressDiv.style.display = 'none';
            retryBtn.style.display = 'none';
        } else if (packageInfo.isInstalling) {
            statusDot.className = 'status-dot installing';
            statusText.textContent = 'Installing...';
            verifyBtn.style.display = 'none';
            resetBtn.style.display = 'none';
            progressDiv.style.display = 'block';
            retryBtn.style.display = 'none';
        } else if (progress.status === 'error') {
            statusDot.className = 'status-dot error';
            statusText.textContent = 'Installation failed';
            verifyBtn.style.display = 'none';
            resetBtn.style.display = 'none';
            progressDiv.style.display = 'none';
            retryBtn.style.display = 'inline-block';
        } else {
            statusDot.className = 'status-dot';
            statusText.textContent = 'Not installed';
            verifyBtn.style.display = 'none';
            resetBtn.style.display = 'none';
            progressDiv.style.display = 'none';
            retryBtn.style.display = 'none';
        }
    }

    /**
     * Update progress display
     */
    updateProgress(progress) {
        const progressFill = document.getElementById('progress-fill');
        const progressText = document.getElementById('progress-text');

        if (progressFill && progressText) {
            progressFill.style.width = `${progress.percentage}%`;
            progressText.textContent = progress.message;
        }

        this.updateDisplay();
    }

    /**
     * Verify package installation
     */
    async verifyPackage() {
        if (!this.packageManager) {
            console.error('Package manager not initialized');
            return;
        }

        try {
            const verified = await this.packageManager.verifyInstallation();
            console.log('Package verification result:', verified);
            this.updateDisplay();
        } catch (error) {
            console.error('Package verification failed:', error);
        }
    }

    /**
     * Reset package
     */
    resetPackage() {
        if (!this.packageManager) {
            console.error('Package manager not initialized');
            return;
        }

        this.packageManager.reset();
        this.updateDisplay();
    }

    async retryInstall() {
        if (!this.packageManager) return;
        try {
            await this.packageManager.installPackage(window.pyodideExecutor?.pyodide);
            this.updateDisplay();
        } catch (error) {
            this.updateDisplay();
        }
    }

    /**
     * Show the panel
     */
    show() {
        if (this.container) {
            this.container.style.display = 'block';
            this.isVisible = true;
        }
    }

    /**
     * Hide the panel
     */
    hide() {
        if (this.container) {
            this.container.style.display = 'none';
            this.isVisible = false;
        }
    }

    /**
     * Toggle panel visibility
     */
    toggle() {
        if (this.isVisible) {
            this.hide();
        } else {
            this.show();
        }
    }
}

// Export for use in other modules
export { PackageStatusPanel };

// Make available globally for testing
window.PackageStatusPanel = PackageStatusPanel; 