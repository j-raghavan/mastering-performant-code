/**
 * Storage Service
 * 
 * Manages local storage for user data and preferences
 */

import { Logger } from '../utils/Logger.js';

class StorageService {
    constructor() {
        this.storageKey = 'pyodide-companion';
    }

    async initialize() {
        Logger.info('StorageService initialized');
    }

    async saveUserCode(chapterId, fileId, code) {
        const key = `${this.storageKey}:code:${chapterId}:${fileId}`;
        localStorage.setItem(key, code);
    }

    async getUserCode(chapterId, fileId) {
        const key = `${this.storageKey}:code:${chapterId}:${fileId}`;
        return localStorage.getItem(key);
    }

    async saveProgress(chapterId, progress) {
        const key = `${this.storageKey}:progress:${chapterId}`;
        localStorage.setItem(key, JSON.stringify(progress));
    }

    async getProgress(chapterId) {
        const key = `${this.storageKey}:progress:${chapterId}`;
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    }

    async saveApplicationState(state) {
        localStorage.setItem(`${this.storageKey}:state`, JSON.stringify(state));
    }

    async getApplicationState() {
        const data = localStorage.getItem(`${this.storageKey}:state`);
        return data ? JSON.parse(data) : null;
    }

    async clearUserData() {
        const keys = Object.keys(localStorage);
        keys.forEach(key => {
            if (key.startsWith(this.storageKey)) {
                localStorage.removeItem(key);
            }
        });
    }
}

export { StorageService }; 