#!/usr/bin/env node

/**
 * Content Synchronization Script
 * 
 * This script synchronizes Python source code and tests from the parent directories
 * and generates metadata for the web companion application.
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Paths relative to the web-companion directory
const SOURCE_DIR = path.resolve(__dirname, '../../src/mastering_performant_code');
const TESTS_DIR = path.resolve(__dirname, '../../tests');
const OUTPUT_DIR = path.resolve(__dirname, '../public/generated');

/**
 * Parse Python file and extract metadata
 */
async function parsePythonFile(filePath) {
    try {
        const content = await fs.readFile(filePath, 'utf-8');
        const fileName = path.basename(filePath, '.py');

        // Extract basic metadata
        const metadata = {
            name: fileName,
            path: path.relative(SOURCE_DIR, filePath),
            content: content,
            size: content.length,
            lines: content.split('\n').length,
            type: determineFileType(fileName, content),
            dependencies: extractDependencies(content),
            docstring: extractDocstring(content),
            classes: extractClasses(content),
            functions: extractFunctions(content),
            imports: extractImports(content)
        };

        return metadata;
    } catch (error) {
        console.error(`Error parsing file ${filePath}:`, error.message);
        return null;
    }
}

/**
 * Determine the type of file based on name and content
 */
function determineFileType(fileName, content) {
    const lowerContent = content.toLowerCase();

    if (fileName.includes('demo') || fileName.includes('example')) {
        return 'demo';
    }
    if (fileName.includes('test')) {
        return 'test';
    }
    if (fileName.includes('analyzer') || fileName.includes('profiler')) {
        return 'analyzer';
    }
    if (fileName.includes('benchmark') || fileName.includes('performance')) {
        return 'benchmark';
    }
    if (fileName.includes('config') || fileName.includes('manager')) {
        return 'config';
    }

    // Default to implementation
    return 'implementation';
}

/**
 * Extract Python imports from content
 */
function extractImports(content) {
    const imports = [];
    const lines = content.split('\n');

    for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed.startsWith('import ') || trimmed.startsWith('from ')) {
            imports.push(trimmed);
        }
    }

    return imports;
}

/**
 * Extract dependencies (imports from local modules)
 */
function extractDependencies(content) {
    const dependencies = [];
    const lines = content.split('\n');

    for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed.startsWith('from .') || trimmed.startsWith('import .')) {
            // Extract module name from relative import
            const match = trimmed.match(/from \.(\w+)/) || trimmed.match(/import \.(\w+)/);
            if (match) {
                dependencies.push(match[1]);
            }
        }
    }

    return dependencies;
}

/**
 * Extract docstring from Python file
 */
function extractDocstring(content) {
    const lines = content.split('\n');
    let inDocstring = false;
    let docstring = '';

    for (const line of lines) {
        const trimmed = line.trim();

        if (trimmed.startsWith('"""') || trimmed.startsWith("'''")) {
            if (!inDocstring) {
                inDocstring = true;
                docstring = trimmed.slice(3);
                if (docstring.endsWith('"""') || docstring.endsWith("'''")) {
                    return docstring.slice(0, -3);
                }
            } else {
                inDocstring = false;
                docstring += trimmed.slice(0, -3);
                return docstring;
            }
        } else if (inDocstring) {
            docstring += '\n' + line;
        }
    }

    return docstring || null;
}

/**
 * Extract class definitions from Python file
 */
function extractClasses(content) {
    const classes = [];
    const lines = content.split('\n');

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (line.startsWith('class ')) {
            const className = line.match(/class\s+(\w+)/)?.[1];
            if (className) {
                classes.push({
                    name: className,
                    line: i + 1,
                    docstring: extractClassDocstring(lines, i)
                });
            }
        }
    }

    return classes;
}

/**
 * Extract function definitions from Python file
 */
function extractFunctions(content) {
    const functions = [];
    const lines = content.split('\n');

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (line.startsWith('def ') && !line.includes('class ')) {
            const funcName = line.match(/def\s+(\w+)/)?.[1];
            if (funcName) {
                functions.push({
                    name: funcName,
                    line: i + 1,
                    docstring: extractFunctionDocstring(lines, i)
                });
            }
        }
    }

    return functions;
}

/**
 * Extract docstring for a class
 */
function extractClassDocstring(lines, classLine) {
    let docstring = '';
    let inDocstring = false;

    for (let i = classLine + 1; i < lines.length; i++) {
        const line = lines[i];
        const trimmed = line.trim();

        if (trimmed.startsWith('"""') || trimmed.startsWith("'''")) {
            if (!inDocstring) {
                inDocstring = true;
                docstring = trimmed.slice(3);
                if (docstring.endsWith('"""') || docstring.endsWith("'''")) {
                    return docstring.slice(0, -3);
                }
            } else {
                docstring += trimmed.slice(0, -3);
                return docstring;
            }
        } else if (inDocstring) {
            docstring += '\n' + line;
        } else if (trimmed && !trimmed.startsWith('#')) {
            break; // End of class docstring
        }
    }

    return docstring || null;
}

/**
 * Extract docstring for a function
 */
function extractFunctionDocstring(lines, funcLine) {
    let docstring = '';
    let inDocstring = false;

    for (let i = funcLine + 1; i < lines.length; i++) {
        const line = lines[i];
        const trimmed = line.trim();

        if (trimmed.startsWith('"""') || trimmed.startsWith("'''")) {
            if (!inDocstring) {
                inDocstring = true;
                docstring = trimmed.slice(3);
                if (docstring.endsWith('"""') || docstring.endsWith("'''")) {
                    return docstring.slice(0, -3);
                }
            } else {
                docstring += trimmed.slice(0, -3);
                return docstring;
            }
        } else if (inDocstring) {
            docstring += '\n' + line;
        } else if (trimmed && !trimmed.startsWith('#')) {
            break; // End of function docstring
        }
    }

    return docstring || null;
}

/**
 * Scan directory for Python files
 */
async function scanPythonFiles(dirPath) {
    const files = [];

    try {
        const entries = await fs.readdir(dirPath, { withFileTypes: true });

        for (const entry of entries) {
            const fullPath = path.join(dirPath, entry.name);

            if (entry.isDirectory()) {
                const subFiles = await scanPythonFiles(fullPath);
                files.push(...subFiles);
            } else if (entry.name.endsWith('.py')) {
                files.push(fullPath);
            }
        }
    } catch (error) {
        console.error(`Error scanning directory ${dirPath}:`, error.message);
    }

    return files;
}

/**
 * Generate chapter metadata
 */
async function generateChapterMetadata() {
    const chapters = [];

    try {
        const sourceEntries = await fs.readdir(SOURCE_DIR, { withFileTypes: true });

        for (const entry of sourceEntries) {
            if (entry.isDirectory() && entry.name.startsWith('chapter_')) {
                const chapterId = entry.name;
                const chapterPath = path.join(SOURCE_DIR, entry.name);
                const testPath = path.join(TESTS_DIR, entry.name);

                // Get chapter number
                const chapterNum = parseInt(chapterId.replace('chapter_', ''));

                // Scan source files
                const sourceFiles = await scanPythonFiles(chapterPath);
                const sourceMetadata = [];

                for (const file of sourceFiles) {
                    const metadata = await parsePythonFile(file);
                    if (metadata) {
                        sourceMetadata.push(metadata);
                    }
                }

                // Scan test files
                const testFiles = await scanPythonFiles(testPath);
                const testMetadata = [];

                for (const file of testFiles) {
                    const metadata = await parsePythonFile(file);
                    if (metadata) {
                        testMetadata.push(metadata);
                    }
                }

                // Find demo file
                const demoFile = sourceMetadata.find(file => file.type === 'demo');

                // Generate chapter info
                const chapter = {
                    id: chapterId,
                    number: chapterNum,
                    title: `Chapter ${chapterNum}`,
                    description: generateChapterDescription(chapterNum, sourceMetadata),
                    sourceFiles: sourceMetadata,
                    testFiles: testMetadata,
                    demoFile: demoFile ? demoFile.name : null,
                    benchmarkFiles: sourceMetadata.filter(f => f.type === 'benchmark').map(f => f.name),
                    dependencies: extractChapterDependencies(sourceMetadata),
                    estimatedTime: estimateChapterTime(sourceMetadata),
                    complexity: determineChapterComplexity(chapterNum),
                    order: chapterNum
                };

                chapters.push(chapter);
            }
        }

        // Sort by chapter number
        chapters.sort((a, b) => a.number - b.number);

    } catch (error) {
        console.error('Error generating chapter metadata:', error);
    }

    return chapters;
}

/**
 * Generate chapter description based on content
 */
function generateChapterDescription(chapterNum, sourceFiles) {
    const descriptions = {
        1: 'Data Structures Fundamentals - Dynamic Arrays, Hash Tables, and Sets',
        2: 'Algorithm Analysis and Profiling',
        3: 'Dynamic Arrays and Memory Management',
        4: 'Linked Lists and Iterators',
        5: 'Priority Queues and Skip Lists',
        6: 'Binary Search Trees',
        7: 'AVL Trees and Self-Balancing',
        8: 'Red-Black Trees',
        9: 'B-Trees and Database Indexing',
        10: 'Tries and String Processing',
        11: 'Binary Heaps and Heap Sort',
        12: 'Disjoint Sets and Union-Find',
        13: 'Hash Tables and Applications',
        14: 'Bloom Filters and Probabilistic Data Structures',
        15: 'Caching Strategies - LRU and LFU',
        16: 'Memory Management and Object Pools'
    };

    return descriptions[chapterNum] || `Chapter ${chapterNum} - Advanced Data Structures and Algorithms`;
}

/**
 * Extract chapter dependencies
 */
function extractChapterDependencies(sourceFiles) {
    const dependencies = new Set();

    for (const file of sourceFiles) {
        for (const dep of file.dependencies) {
            dependencies.add(dep);
        }
    }

    return Array.from(dependencies);
}

/**
 * Estimate chapter completion time
 */
function estimateChapterTime(sourceFiles) {
    let time = 0;

    for (const file of sourceFiles) {
        switch (file.type) {
            case 'demo':
                time += 15; // 15 minutes for demos
                break;
            case 'implementation':
                time += 20; // 20 minutes for implementations
                break;
            case 'test':
                time += 10; // 10 minutes for tests
                break;
            case 'analyzer':
                time += 25; // 25 minutes for analyzers
                break;
            case 'benchmark':
                time += 15; // 15 minutes for benchmarks
                break;
        }
    }

    return Math.max(30, time); // Minimum 30 minutes
}

/**
 * Determine chapter complexity
 */
function determineChapterComplexity(chapterNum) {
    if (chapterNum <= 5) return 'beginner';
    if (chapterNum <= 10) return 'intermediate';
    return 'advanced';
}

/**
 * Main synchronization function
 */
async function syncContent() {
    console.log('🔄 Starting content synchronization...');

    try {
        // Ensure output directory exists
        await fs.mkdir(OUTPUT_DIR, { recursive: true });

        // Generate chapter metadata
        console.log('📚 Generating chapter metadata...');
        const chapters = await generateChapterMetadata();

        // Write chapters.json
        const chaptersPath = path.join(OUTPUT_DIR, 'chapters.json');
        await fs.writeFile(chaptersPath, JSON.stringify(chapters, null, 2));
        console.log(`✅ Generated ${chapters.length} chapters metadata`);

        // Copy source files to generated directory
        console.log('📁 Copying source files...');
        for (const chapter of chapters) {
            const chapterDir = path.join(OUTPUT_DIR, 'content', chapter.id);
            await fs.mkdir(chapterDir, { recursive: true });

            for (const file of chapter.sourceFiles) {
                const sourcePath = path.join(SOURCE_DIR, file.path);
                const destPath = path.join(chapterDir, path.basename(file.path));
                try {
                    await fs.copyFile(sourcePath, destPath);
                } catch (error) {
                    console.warn(`⚠️ Could not copy ${sourcePath}: ${error.message}`);
                }
            }

            // Copy test files
            const testDir = path.join(chapterDir, 'tests');
            await fs.mkdir(testDir, { recursive: true });

            for (const file of chapter.testFiles) {
                const sourcePath = path.join(TESTS_DIR, file.path);
                const destPath = path.join(testDir, path.basename(file.path));
                try {
                    await fs.copyFile(sourcePath, destPath);
                } catch (error) {
                    console.warn(`⚠️ Could not copy test file ${sourcePath}: ${error.message}`);
                }
            }
        }

        console.log('✅ Content synchronization completed successfully!');
        console.log(`📊 Generated metadata for ${chapters.length} chapters`);
        console.log(`📁 Output directory: ${OUTPUT_DIR}`);

    } catch (error) {
        console.error('❌ Content synchronization failed:', error);
        process.exit(1);
    }
}

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
    syncContent();
}

export { syncContent, parsePythonFile, generateChapterMetadata }; 