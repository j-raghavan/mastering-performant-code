/**
 * NavigationBar Component
 * 
 * Provides chapter navigation, progress tracking,
 * search functionality, and settings access
 */

import { Logger } from '../../utils/Logger.js';

class NavigationBar {
    constructor(container, options = {}) {
        this.container = container;
        this.options = {
            theme: 'light',
            showProgress: true,
            showSearch: true,
            ...options
        };

        this.chapters = [];
        this.currentChapter = null;
        this.progress = new Map();
        this.searchCallbacks = [];
        this.navigationCallbacks = [];
        this.eventListeners = new Map();

        this.init();
    }

    init() {
        this.createNavigationStructure();
        this.bindEvents();
    }

    createNavigationStructure() {
        this.container.innerHTML = `
            <nav class="navigation-bar">
                <div class="nav-left">
                    <div class="logo">
                        <span class="logo-icon">🐍</span>
                        <span class="logo-text">Mastering Performant Code</span>
                    </div>
                    <div class="python-version" id="python-version">
                        <span class="version-label">Python:</span>
                        <span class="version-text">Loading...</span>
                    </div>
                </div>
                
                <div class="nav-center">
                    <div class="chapter-navigation">
                        <button class="nav-btn" id="prev-chapter" title="Previous Chapter">
                            <span class="icon">◀</span>
                        </button>
                        
                        <div class="chapter-selector">
                            <select id="chapter-select" class="chapter-select">
                                <option value="">Select Chapter...</option>
                            </select>
                            <div class="chapter-info" id="chapter-info">
                                <span class="chapter-title">No chapter selected</span>
                                <span class="chapter-progress" id="chapter-progress"></span>
                            </div>
                        </div>
                        
                        <button class="nav-btn" id="next-chapter" title="Next Chapter">
                            <span class="icon">▶</span>
                        </button>
                    </div>
                </div>
                
                <div class="nav-right">
                    ${this.options.showSearch ? `
                        <div class="search-container">
                            <input type="text" id="search-input" class="search-input" placeholder="Search code...">
                            <button class="search-btn" id="search-btn" title="Search">
                                <span class="icon">🔍</span>
                            </button>
                        </div>
                    ` : ''}
                    
                    <div class="nav-actions">
                        <button class="nav-btn" id="settings-btn" title="Settings">
                            <span class="icon">⚙️</span>
                        </button>
                        <button class="nav-btn" id="help-btn" title="Help">
                            <span class="icon">❓</span>
                        </button>
                    </div>
                </div>
            </nav>
        `;

        // Get references to elements
        this.chapterSelect = this.container.querySelector('#chapter-select');
        this.chapterInfo = this.container.querySelector('#chapter-info');
        this.chapterTitle = this.container.querySelector('.chapter-title');
        this.chapterProgress = this.container.querySelector('#chapter-progress');
        this.prevBtn = this.container.querySelector('#prev-chapter');
        this.nextBtn = this.container.querySelector('#next-chapter');
        this.searchInput = this.container.querySelector('#search-input');
        this.searchBtn = this.container.querySelector('#search-btn');
        this.settingsBtn = this.container.querySelector('#settings-btn');
        this.helpBtn = this.container.querySelector('#help-btn');
        this.pythonVersion = this.container.querySelector('#python-version .version-text');
    }

    bindEvents() {
        // Chapter navigation
        this.chapterSelect.addEventListener('change', (e) => {
            this.selectChapter(e.target.value);
        });

        this.prevBtn.addEventListener('click', () => this.navigateToPrevious());
        this.nextBtn.addEventListener('click', () => this.navigateToNext());

        // Search functionality
        if (this.searchInput) {
            this.searchInput.addEventListener('input', (e) => {
                this.handleSearch(e.target.value);
            });

            this.searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.performSearch();
                }
            });

            this.searchBtn.addEventListener('click', () => this.performSearch());
        }

        // Settings and help
        this.settingsBtn.addEventListener('click', () => this.openSettings());
        this.helpBtn.addEventListener('click', () => this.openHelp());
    }

    setChapters(chapters) {
        this.chapters = chapters;
        this.renderChapterOptions();
        this.updateNavigationState();
    }

    renderChapterOptions() {
        this.chapterSelect.innerHTML = '<option value="">Select Chapter...</option>';

        this.chapters.forEach(chapter => {
            const option = document.createElement('option');
            option.value = chapter.id;
            option.textContent = `${chapter.order}. ${chapter.title}`;
            this.chapterSelect.appendChild(option);
        });
    }

    selectChapter(chapterId) {
        if (!chapterId) return;

        const chapter = this.chapters.find(c => c.id === chapterId);
        if (!chapter) return;

        this.currentChapter = chapter;
        this.updateChapterInfo();
        this.updateNavigationState();

        // Emit navigation event
        this.emit('chapterSelected', { chapter });

        Logger.info(`Selected chapter: ${chapter.title}`);
    }

    updateChapterInfo() {
        if (!this.currentChapter) {
            this.chapterTitle.textContent = 'No chapter selected';
            this.chapterProgress.textContent = '';
            return;
        }

        this.chapterTitle.textContent = this.currentChapter.title;

        // Update progress
        const progress = this.progress.get(this.currentChapter.id) || 0;
        this.chapterProgress.textContent = `${progress}% complete`;

        // Update select value
        this.chapterSelect.value = this.currentChapter.id;
    }

    updateNavigationState() {
        if (!this.currentChapter) {
            this.prevBtn.disabled = true;
            this.nextBtn.disabled = true;
            return;
        }

        const currentIndex = this.chapters.findIndex(c => c.id === this.currentChapter.id);

        this.prevBtn.disabled = currentIndex <= 0;
        this.nextBtn.disabled = currentIndex >= this.chapters.length - 1;
    }

    navigateToPrevious() {
        if (!this.currentChapter) return;

        const currentIndex = this.chapters.findIndex(c => c.id === this.currentChapter.id);
        if (currentIndex > 0) {
            const prevChapter = this.chapters[currentIndex - 1];
            this.selectChapter(prevChapter.id);
        }
    }

    navigateToNext() {
        if (!this.currentChapter) return;

        const currentIndex = this.chapters.findIndex(c => c.id === this.currentChapter.id);
        if (currentIndex < this.chapters.length - 1) {
            const nextChapter = this.chapters[currentIndex + 1];
            this.selectChapter(nextChapter.id);
        }
    }

    handleSearch(query) {
        // Debounce search input
        clearTimeout(this.searchTimeout);
        this.searchTimeout = setTimeout(() => {
            this.notifySearchCallbacks(query);
        }, 300);
    }

    performSearch() {
        const query = this.searchInput ? this.searchInput.value.trim() : '';
        if (query) {
            this.notifySearchCallbacks(query);
            Logger.info(`Performing search: ${query}`);
        }
    }

    openSettings() {
        this.emit('openSettings', {});
        Logger.info('Opening settings');
    }

    openHelp() {
        this.emit('openHelp', {});
        Logger.info('Opening help');
    }

    updateProgress(chapterId, progress) {
        this.progress.set(chapterId, progress);

        if (this.currentChapter && this.currentChapter.id === chapterId) {
            this.updateChapterInfo();
        }
    }

    getProgress(chapterId) {
        return this.progress.get(chapterId) || 0;
    }

    getAllProgress() {
        const progressData = {};
        this.chapters.forEach(chapter => {
            progressData[chapter.id] = this.getProgress(chapter.id);
        });
        return progressData;
    }

    onSearch(callback) {
        this.searchCallbacks.push(callback);
    }

    onNavigation(callback) {
        this.navigationCallbacks.push(callback);
    }

    notifySearchCallbacks(query) {
        this.searchCallbacks.forEach(callback => {
            try {
                callback(query);
            } catch (error) {
                Logger.error('Error in search callback:', error);
            }
        });
    }

    emit(event, data) {
        // Trigger custom callbacks
        if (event === 'search') {
            this.notifySearchCallbacks(data);
        } else if (event === 'navigation') {
            this.notifyNavigationCallbacks(data);
        }

        // Trigger standard event listeners
        if (this.eventListeners.has(event)) {
            const callbacks = this.eventListeners.get(event);
            callbacks.forEach(callback => {
                try {
                    callback({ detail: data });
                } catch (error) {
                    Logger.error(`Error in event listener for ${event}:`, error);
                }
            });
        }
    }

    setTheme(theme) {
        this.container.className = `navigation-bar theme-${theme}`;
    }

    showLoading(show = true) {
        const loadingElement = this.container.querySelector('.loading-indicator');
        if (loadingElement) {
            loadingElement.style.display = show ? 'block' : 'none';
        }
    }

    setPythonVersion(version) {
        if (this.pythonVersion) {
            this.pythonVersion.textContent = version;
        }
    }

    destroy() {
        // Clear timeouts
        if (this.searchTimeout) {
            clearTimeout(this.searchTimeout);
        }

        // Clear container
        this.container.innerHTML = '';
    }

    addEventListener(event, callback) {
        if (!this.eventListeners.has(event)) {
            this.eventListeners.set(event, []);
        }
        this.eventListeners.get(event).push(callback);
    }

    removeEventListener(event, callback) {
        if (this.eventListeners.has(event)) {
            const callbacks = this.eventListeners.get(event);
            const index = callbacks.indexOf(callback);
            if (index > -1) {
                callbacks.splice(index, 1);
            }
        }
    }
}

export { NavigationBar }; 