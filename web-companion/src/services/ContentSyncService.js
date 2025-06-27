/**
 * Content Synchronization Service
 * 
 * Loads and manages chapter content from the generated metadata
 */

import { Logger } from '../utils/Logger.js';

class ContentSyncService {
    constructor() {
        this.chapters = null;
        this.chaptersPath = '/generated/chapters.json';
        this.contentBasePath = '/generated/content';
        this.cache = new Map();
    }

    /**
     * Initialize the service
     */
    async initialize() {
        try {
            Logger.info('Initializing ContentSyncService...');
            await this.loadChaptersMetadata();
            Logger.info('ContentSyncService initialized successfully');
        } catch (error) {
            Logger.error('Failed to initialize ContentSyncService', error);
            throw error;
        }
    }

    /**
     * Load chapters metadata from JSON file
     */
    async loadChaptersMetadata() {
        try {
            Logger.info('Loading chapters metadata...');
            Logger.info(`Fetching from: ${this.chaptersPath}`);

            // Create a controller for timeout
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

            const response = await fetch(this.chaptersPath, {
                signal: controller.signal
            });

            clearTimeout(timeoutId);
            Logger.info(`Response status: ${response.status} ${response.statusText}`);

            if (!response.ok) {
                throw new Error(`Failed to load chapters metadata: ${response.status} ${response.statusText}`);
            }

            Logger.info('Parsing JSON response...');
            this.chapters = await response.json();
            Logger.info(`Loaded ${this.chapters.length} chapters`);

            // Log first few chapters for debugging
            if (this.chapters && this.chapters.length > 0) {
                Logger.info('First 3 chapters:');
                this.chapters.slice(0, 3).forEach((chapter, index) => {
                    let displayTitle = chapter.title;
                    if (chapter.description) {
                        displayTitle = `Chapter ${chapter.number}: ${chapter.description}`;
                    } else if (chapter.title && chapter.title !== `Chapter ${chapter.number}`) {
                        displayTitle = chapter.title;
                    } else {
                        displayTitle = `Chapter ${chapter.number}`;
                    }
                    Logger.info(`  Chapter ${index + 1}: id="${chapter.id}", title="${displayTitle}", order=${chapter.order}`);
                });
            } else {
                Logger.warn('⚠️ No chapters found in the JSON file');
            }

            // Pre-cache chapter data
            await this.preloadChapters();

        } catch (error) {
            if (error.name === 'AbortError') {
                Logger.error('❌ Timeout while loading chapters metadata (30 seconds)');
                Logger.warn('⚠️ Using fallback chapter data...');
                this.loadFallbackChapters();
                return;
            }
            Logger.error('Error loading chapters metadata', error);
            Logger.warn('⚠️ Using fallback chapter data...');
            this.loadFallbackChapters();
        }
    }

    /**
     * Load fallback chapter data if the main file fails to load
     */
    loadFallbackChapters() {
        Logger.info('Loading fallback chapter data...');

        this.chapters = [
            {
                id: 'chapter_01',
                number: 1,
                order: 1,
                title: 'Chapter 1: Data Structures Fundamentals',
                description: 'Dynamic Arrays, Hash Tables, and Sets',
                sourceFiles: [],
                testFiles: []
            },
            {
                id: 'chapter_02',
                number: 2,
                order: 2,
                title: 'Chapter 2: Algorithm Analysis',
                description: 'Time and Space Complexity Analysis',
                sourceFiles: [],
                testFiles: []
            },
            {
                id: 'chapter_03',
                number: 3,
                order: 3,
                title: 'Chapter 3: Linked Lists',
                description: 'Singly and Doubly Linked Lists',
                sourceFiles: [],
                testFiles: []
            },
            {
                id: 'chapter_04',
                number: 4,
                order: 4,
                title: 'Chapter 4: Stacks and Queues',
                description: 'Stack and Queue Implementations',
                sourceFiles: [],
                testFiles: []
            },
            {
                id: 'chapter_05',
                number: 5,
                order: 5,
                title: 'Chapter 5: Trees',
                description: 'Binary Trees and Tree Traversal',
                sourceFiles: [],
                testFiles: []
            }
        ];

        Logger.info(`✅ Loaded ${this.chapters.length} fallback chapters`);
    }

    /**
     * Preload all chapters for better performance
     */
    async preloadChapters() {
        Logger.info('Preloading chapters...');

        const promises = this.chapters.map(chapter =>
            this.loadChapterContent(chapter.id).catch(error => {
                Logger.warn(`Failed to preload chapter ${chapter.id}`, error);
                return null;
            })
        );

        await Promise.all(promises);
        Logger.info('Chapter preloading completed');
    }

    /**
     * Get all chapters
     */
    getAllChapters() {
        if (!this.chapters) {
            Logger.error('❌ Chapters not loaded. Call initialize() first.');
            throw new Error('Chapters not loaded. Call initialize() first.');
        }

        Logger.info(`getAllChapters() called, returning ${this.chapters.length} chapters`);
        return [...this.chapters];
    }

    /**
     * Get chapter by ID
     */
    getChapter(id) {
        if (!this.chapters) {
            throw new Error('Chapters not loaded. Call initialize() first.');
        }

        const chapter = this.chapters.find(c => c.id === id);
        if (!chapter) {
            throw new Error(`Chapter not found: ${id}`);
        }

        return { ...chapter };
    }

    /**
     * Get chapter by number
     */
    getChapterByNumber(number) {
        if (!this.chapters) {
            throw new Error('Chapters not loaded. Call initialize() first.');
        }

        const chapter = this.chapters.find(c => c.number === number);
        if (!chapter) {
            throw new Error(`Chapter not found: ${number}`);
        }

        return { ...chapter };
    }

    /**
     * Load chapter content (source files and test files)
     */
    async loadChapterContent(chapterId) {
        // Check cache first
        if (this.cache.has(chapterId)) {
            Logger.debug(`Chapter ${chapterId} loaded from cache`);
            return this.cache.get(chapterId);
        }

        try {
            Logger.info(`Loading chapter content: ${chapterId}`);

            const chapter = this.getChapter(chapterId);

            // The content is already in the chapter object from chapters.json
            // No need to fetch files separately
            const chapterContent = {
                ...chapter,
                sourceFiles: chapter.sourceFiles || [],
                testFiles: chapter.testFiles || []
            };

            // Cache the result
            this.cache.set(chapterId, chapterContent);

            Logger.info(`Chapter ${chapterId} content loaded successfully`);
            return chapterContent;

        } catch (error) {
            Logger.error(`Error loading chapter content: ${chapterId}`, error);
            throw error;
        }
    }

    /**
     * Get source file content
     */
    async getSourceFileContent(chapterId, fileName) {
        const chapter = await this.loadChapterContent(chapterId);
        const sourceFile = chapter.sourceFiles.find(f => f.name === fileName);

        if (!sourceFile) {
            throw new Error(`Source file not found: ${fileName} in chapter ${chapterId}`);
        }

        return sourceFile.content;
    }

    /**
     * Get test file content
     */
    async getTestFileContent(chapterId, fileName) {
        const chapter = await this.loadChapterContent(chapterId);
        const testFile = chapter.testFiles.find(f => f.name === fileName);

        if (!testFile) {
            throw new Error(`Test file not found: ${fileName} in chapter ${chapterId}`);
        }

        return testFile.content;
    }

    /**
     * Get demo file for a chapter
     */
    async getDemoFile(chapterId) {
        const chapter = await this.loadChapterContent(chapterId);

        if (!chapter.demoFile) {
            return null;
        }

        return chapter.sourceFiles.find(f => f.name === chapter.demoFile);
    }

    /**
     * Get benchmark files for a chapter
     */
    async getBenchmarkFiles(chapterId) {
        const chapter = await this.loadChapterContent(chapterId);

        return chapter.sourceFiles.filter(f =>
            chapter.benchmarkFiles.includes(f.name)
        );
    }

    /**
     * Search chapters by content
     */
    searchChapters(query) {
        if (!this.chapters) {
            return [];
        }

        const lowerQuery = query.toLowerCase();

        return this.chapters.filter(chapter => {
            // Search in title and description
            if (chapter.title.toLowerCase().includes(lowerQuery) ||
                chapter.description.toLowerCase().includes(lowerQuery)) {
                return true;
            }

            // Search in file names
            const fileNames = [
                ...chapter.sourceFiles.map(f => f.name),
                ...chapter.testFiles.map(f => f.name)
            ];

            return fileNames.some(name => name.toLowerCase().includes(lowerQuery));
        });
    }

    /**
     * Get chapters by complexity
     */
    getChaptersByComplexity(complexity) {
        if (!this.chapters) {
            return [];
        }

        return this.chapters.filter(chapter => chapter.complexity === complexity);
    }

    /**
     * Get next chapter
     */
    getNextChapter(currentId) {
        if (!this.chapters) {
            return null;
        }

        const currentIndex = this.chapters.findIndex(c => c.id === currentId);
        if (currentIndex === -1 || currentIndex === this.chapters.length - 1) {
            return null;
        }

        return { ...this.chapters[currentIndex + 1] };
    }

    /**
     * Get previous chapter
     */
    getPreviousChapter(currentId) {
        if (!this.chapters) {
            return null;
        }

        const currentIndex = this.chapters.findIndex(c => c.id === currentId);
        if (currentIndex <= 0) {
            return null;
        }

        return { ...this.chapters[currentIndex - 1] };
    }

    /**
     * Clear cache
     */
    clearCache() {
        this.cache.clear();
        Logger.info('Content cache cleared');
    }

    /**
     * Get cache statistics
     */
    getCacheStats() {
        return {
            size: this.cache.size,
            keys: Array.from(this.cache.keys())
        };
    }
}

export { ContentSyncService }; 