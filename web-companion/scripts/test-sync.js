#!/usr/bin/env node

/**
 * Test script to validate content synchronization output
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const GENERATED_DIR = path.resolve(__dirname, '../public/generated');

async function testContentSync() {
    console.log('🧪 Testing content synchronization output...');

    try {
        // Check if chapters.json exists
        const chaptersPath = path.join(GENERATED_DIR, 'chapters.json');
        const chaptersData = await fs.readFile(chaptersPath, 'utf-8');
        const chapters = JSON.parse(chaptersData);

        console.log(`✅ Found ${chapters.length} chapters`);

        // Validate chapter structure
        for (const chapter of chapters) {
            console.log(`\n📚 Chapter ${chapter.number}: ${chapter.title}`);
            console.log(`   Description: ${chapter.description}`);
            console.log(`   Source files: ${chapter.sourceFiles.length}`);
            console.log(`   Test files: ${chapter.testFiles.length}`);
            console.log(`   Demo file: ${chapter.demoFile || 'None'}`);
            console.log(`   Complexity: ${chapter.complexity}`);
            console.log(`   Estimated time: ${chapter.estimatedTime} minutes`);

            // Check if content directory exists
            const contentDir = path.join(GENERATED_DIR, 'content', chapter.id);
            const contentExists = await fs.access(contentDir).then(() => true).catch(() => false);
            console.log(`   Content directory: ${contentExists ? '✅' : '❌'}`);

            if (contentExists) {
                const files = await fs.readdir(contentDir);
                console.log(`   Files in directory: ${files.length}`);
            }
        }

        // Test specific chapter
        const testChapter = chapters.find(c => c.number === 1);
        if (testChapter) {
            console.log(`\n🔍 Detailed test for Chapter 1:`);
            console.log(`   Source files: ${testChapter.sourceFiles.map(f => f.name).join(', ')}`);

            const demoFile = testChapter.sourceFiles.find(f => f.type === 'demo');
            if (demoFile) {
                console.log(`   Demo file: ${demoFile.name} (${demoFile.lines} lines)`);
                console.log(`   Demo docstring: ${demoFile.docstring ? 'Present' : 'None'}`);
                console.log(`   Demo classes: ${demoFile.classes.length}`);
                console.log(`   Demo functions: ${demoFile.functions.length}`);
            }
        }

        console.log('\n✅ Content synchronization test completed successfully!');

    } catch (error) {
        console.error('❌ Content synchronization test failed:', error);
        process.exit(1);
    }
}

// Run test
testContentSync(); 