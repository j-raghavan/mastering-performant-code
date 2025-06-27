/**
 * Test Chapters JavaScript Module
 * 
 * This file provides test data and utilities for the chapter testing functionality
 */

// Test chapter data
window.testChapters = [
    {
        id: 'chapter_01',
        title: 'Dynamic Arrays and Memory Management',
        description: 'Understanding dynamic arrays and memory allocation strategies',
        files: [
            'dynamic_array.py',
            'hash_table.py',
            'simple_set.py',
            'analyzer.py'
        ]
    },
    {
        id: 'chapter_02',
        title: 'Algorithm Analysis and Profiling',
        description: 'Performance analysis and algorithm optimization techniques',
        files: [
            'algorithms.py',
            'benchmarks.py',
            'profiler.py'
        ]
    },
    {
        id: 'chapter_03',
        title: 'Real-World Applications',
        description: 'Practical applications of data structures and algorithms',
        files: [
            'applications.py',
            'dynamic_array.py'
        ]
    }
];

// Test utilities
window.testUtils = {
    /**
     * Get chapter by ID
     */
    getChapter(id) {
        return window.testChapters.find(chapter => chapter.id === id);
    },

    /**
     * Get all chapter IDs
     */
    getChapterIds() {
        return window.testChapters.map(chapter => chapter.id);
    },

    /**
     * Get files for a specific chapter
     */
    getChapterFiles(chapterId) {
        const chapter = this.getChapter(chapterId);
        return chapter ? chapter.files : [];
    },

    /**
     * Validate chapter structure
     */
    validateChapter(chapter) {
        return chapter &&
            chapter.id &&
            chapter.title &&
            chapter.files &&
            Array.isArray(chapter.files);
    }
};

// For backward compatibility
window.testChaptersModule = {
    testChapters: window.testChapters,
    testUtils: window.testUtils
}; 