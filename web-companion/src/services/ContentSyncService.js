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

            const response = await fetch(this.chaptersPath);
            if (!response.ok) {
                throw new Error(`Failed to load chapters metadata: ${response.status} ${response.statusText}`);
            }

            this.chapters = await response.json();
            Logger.info(`Loaded ${this.chapters.length} chapters`);

            // Pre-cache chapter data
            await this.preloadChapters();

        } catch (error) {
            Logger.error('Error loading chapters metadata', error);
            throw new Error(`ContentError: ${error.message}`);
        }
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
            throw new Error('Chapters not loaded. Call initialize() first.');
        }
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