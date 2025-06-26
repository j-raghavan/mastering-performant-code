/**
 * Chapter Manager Service
 * 
 * Manages chapter navigation and progress tracking
 */

import { Logger } from '../utils/Logger.js';

class ChapterManager {
    constructor(contentSyncService) {
        this.contentSyncService = contentSyncService;
        this.progress = new Map();
    }

    /**
     * Initialize the chapter manager
     */
    async initialize() {
        try {
            Logger.info('Initializing ChapterManager...');
            
            // Load saved progress from localStorage
            await this.loadProgress();
            
            Logger.info('ChapterManager initialized successfully');
        } catch (error) {
            Logger.error('Failed to initialize ChapterManager:', error);
            // Don't throw error, continue with empty progress
        }
    }

    /**
     * Load progress from localStorage
     */
    async loadProgress() {
        try {
            const savedProgress = localStorage.getItem('chapter-progress');
            if (savedProgress) {
                const progressData = JSON.parse(savedProgress);
                this.progress = new Map(Object.entries(progressData));
                Logger.info('Chapter progress loaded from localStorage');
            }
        } catch (error) {
            Logger.warn('Failed to load chapter progress:', error);
        }
    }

    /**
     * Save progress to localStorage
     */
    async saveProgress() {
        try {
            const progressData = Object.fromEntries(this.progress);
            localStorage.setItem('chapter-progress', JSON.stringify(progressData));
        } catch (error) {
            Logger.warn('Failed to save chapter progress:', error);
        }
    }

    async getChapter(id) {
        return this.contentSyncService.getChapter(id);
    }

    getAllChapters() {
        return this.contentSyncService.getAllChapters();
    }

    getNextChapter(currentId) {
        return this.contentSyncService.getNextChapter(currentId);
    }

    getPreviousChapter(currentId) {
        return this.contentSyncService.getPreviousChapter(currentId);
    }

    markAsCompleted(chapterId) {
        this.progress.set(chapterId, { completed: true, timestamp: Date.now() });
        this.saveProgress(); // Auto-save progress
        Logger.info(`Chapter ${chapterId} marked as completed`);
    }

    /**
     * Get progress for a chapter
     */
    getProgress(chapterId) {
        return this.progress.get(chapterId) || { completed: false, timestamp: null };
    }

    /**
     * Get all progress
     */
    getAllProgress() {
        return Object.fromEntries(this.progress);
    }

    /**
     * Clear progress for a chapter
     */
    clearProgress(chapterId) {
        this.progress.delete(chapterId);
        this.saveProgress();
    }

    /**
     * Clear all progress
     */
    clearAllProgress() {
        this.progress.clear();
        this.saveProgress();
    }
}

export { ChapterManager }; 