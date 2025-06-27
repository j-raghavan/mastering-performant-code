/**
 * File Loader Service
 * 
 * Handles loading Python files from the content system
 * Adapted from pyodide-demo for web-companion architecture
 */

import { Logger } from '../utils/Logger.js';

class FileLoader {
    constructor(contentSyncService) {
        this.contentSyncService = contentSyncService;
        this.loadedFiles = new Map();
        this.currentChapter = null;
        this.fileCategories = {
            'demo': 'Demo',
            'implementation': 'Implementation',
            'analyzer': 'Analyzer',
            'benchmark': 'Benchmark',
            'test': 'Test',
            'config': 'Configuration'
        };
    }

    /**
     * Initialize the file loader
     */
    async initialize() {
        try {
            Logger.info('FileLoader: Starting initialization...');

            // Initialize content sync service if not already done
            if (!this.contentSyncService.isInitialized) {
                await this.contentSyncService.initialize();
            }

            Logger.info('FileLoader: Initialization completed');
            return {
                success: true,
                filesLoaded: this.loadedFiles.size,
                message: 'File loader initialized successfully'
            };
        } catch (error) {
            Logger.error('FileLoader: Initialization failed:', error);
            return {
                success: false,
                error: error.message,
                message: 'Failed to initialize file loader'
            };
        }
    }

    /**
     * Load files for a specific chapter
     */
    async loadChapterFiles(chapterId) {
        try {
            Logger.info(`FileLoader: Loading files for chapter ${chapterId}`);

            const chapterContent = await this.contentSyncService.loadChapterContent(chapterId);
            this.currentChapter = chapterId;

            // Clear previous files
            this.loadedFiles.clear();

            // Load source files
            if (chapterContent.sourceFiles) {
                for (const sourceFile of chapterContent.sourceFiles) {
                    const fileData = {
                        path: `${chapterId}/${sourceFile.name}`,
                        content: sourceFile.content,
                        category: sourceFile.type || 'implementation',
                        name: sourceFile.name,
                        chapterId: chapterId,
                        loadedAt: new Date(),
                        size: sourceFile.content.length,
                        docstring: sourceFile.docstring,
                        classes: sourceFile.classes || [],
                        functions: sourceFile.functions || []
                    };

                    this.loadedFiles.set(fileData.path, fileData);
                }
            }

            // Load test files
            if (chapterContent.testFiles) {
                for (const testFile of chapterContent.testFiles) {
                    const fileData = {
                        path: `${chapterId}/tests/${testFile.name}`,
                        content: testFile.content,
                        category: 'test',
                        name: testFile.name,
                        chapterId: chapterId,
                        loadedAt: new Date(),
                        size: testFile.content.length,
                        docstring: testFile.docstring,
                        classes: testFile.classes || [],
                        functions: testFile.functions || []
                    };

                    this.loadedFiles.set(fileData.path, fileData);
                }
            }

            Logger.info(`FileLoader: Loaded ${this.loadedFiles.size} files for chapter ${chapterId}`);
            return {
                success: true,
                filesLoaded: this.loadedFiles.size,
                chapterId: chapterId
            };

        } catch (error) {
            Logger.error(`FileLoader: Failed to load chapter files for ${chapterId}:`, error);
            return {
                success: false,
                error: error.message,
                chapterId: chapterId
            };
        }
    }

    /**
     * Get file content by path
     */
    getFileContent(path) {
        const fileData = this.loadedFiles.get(path);
        return fileData ? fileData.content : null;
    }

    /**
     * Get file info by path
     */
    getFileInfo(path) {
        return this.loadedFiles.get(path) || null;
    }

    /**
     * Get files by category
     */
    getFilesByCategory(category) {
        return Array.from(this.loadedFiles.values())
            .filter(file => file.category === category)
            .sort((a, b) => a.name.localeCompare(b.name));
    }

    /**
     * Get all loaded files
     */
    getAllFiles() {
        return Array.from(this.loadedFiles.values())
            .sort((a, b) => a.name.localeCompare(b.name));
    }

    /**
     * Get files organized for display
     * @param {Object} options - Options for display
     * @param {boolean} options.includeTests - Whether to include test files (default: false)
     */
    getFilesForDisplay(options = {}) {
        const { includeTests = false } = options;
        const files = this.getAllFiles();
        const organized = {
            'src': [],
            'tests': [],
            'demos': []
        };

        // Group files into three main sections, robustly excluding __init__.py and __init__
        for (const file of files) {
            // Skip __init__.py and __init__ (with or without extension)
            if (file.name === '__init__.py' || file.name === '__init__') {
                continue;
            }

            // Categorize files into three main sections
            if (file.category === 'demo') {
                organized.demos.push(file);
            } else if (file.category === 'test') {
                if (includeTests) {
                    organized.tests.push(file);
                }
                // Otherwise, skip test files
            } else {
                // All other files (implementation, analyzer, benchmark, config, etc.) go to src
                organized.src.push(file);
            }
        }

        // Convert to array format for UI with proper section names
        const result = [];

        // Add SRC section if it has files
        if (organized.src.length > 0) {
            result.push({
                category: 'src',
                displayName: 'Source Files',
                files: organized.src.sort((a, b) => a.name.localeCompare(b.name))
            });
        }

        // Add DEMOS section if it has files
        if (organized.demos.length > 0) {
            result.push({
                category: 'demos',
                displayName: 'Demo Files',
                files: organized.demos.sort((a, b) => a.name.localeCompare(b.name))
            });
        }

        // Optionally add TESTS section if requested
        if (includeTests && organized.tests.length > 0) {
            result.push({
                category: 'tests',
                displayName: 'Test Files',
                files: organized.tests.sort((a, b) => a.name.localeCompare(b.name))
            });
        }

        return result;
    }

    /**
     * Get demo files for the current chapter
     */
    getDemoFiles() {
        return this.getFilesByCategory('demo');
    }

    /**
     * Get test files for the current chapter
     */
    getTestFiles() {
        return this.getFilesByCategory('test');
    }

    /**
     * Get implementation files for the current chapter
     */
    getImplementationFiles() {
        return this.getFilesByCategory('implementation');
    }

    /**
     * Check if a file exists
     */
    hasFile(path) {
        return this.loadedFiles.has(path);
    }

    /**
     * Get all file paths
     */
    getFilePaths() {
        return Array.from(this.loadedFiles.keys());
    }

    /**
     * Get current chapter
     */
    getCurrentChapter() {
        return this.currentChapter;
    }

    /**
     * Get file statistics
     */
    getStats() {
        const files = this.getAllFiles();
        const stats = {
            totalFiles: files.length,
            totalSize: files.reduce((sum, file) => sum + file.size, 0),
            byCategory: {},
            byChapter: this.currentChapter
        };

        // Count by category
        for (const file of files) {
            const category = file.category;
            if (!stats.byCategory[category]) {
                stats.byCategory[category] = 0;
            }
            stats.byCategory[category]++;
        }

        return stats;
    }

    /**
     * Refresh file discovery for current chapter
     */
    async refreshDiscovery() {
        if (!this.currentChapter) {
            throw new Error('No current chapter loaded');
        }

        Logger.info(`FileLoader: Refreshing discovery for chapter ${this.currentChapter}`);
        return await this.loadChapterFiles(this.currentChapter);
    }

    /**
     * Get file by name (searches across all loaded files)
     */
    getFileByName(fileName) {
        return Array.from(this.loadedFiles.values())
            .find(file => file.name === fileName);
    }

    /**
     * Get files that contain a specific class or function
     */
    searchFiles(query) {
        const results = [];
        const lowerQuery = query.toLowerCase();

        for (const file of this.loadedFiles.values()) {
            let match = false;

            // Check file name
            if (file.name.toLowerCase().includes(lowerQuery)) {
                match = true;
            }

            // Check classes
            for (const cls of file.classes) {
                if (cls.name.toLowerCase().includes(lowerQuery)) {
                    match = true;
                    break;
                }
            }

            // Check functions
            for (const func of file.functions) {
                if (func.name.toLowerCase().includes(lowerQuery)) {
                    match = true;
                    break;
                }
            }

            // Check docstring
            if (file.docstring && file.docstring.toLowerCase().includes(lowerQuery)) {
                match = true;
            }

            if (match) {
                results.push(file);
            }
        }

        return results;
    }
}

export { FileLoader }; 