/**
 * Import Path Resolver Service
 * 
 * Transforms import statements from 'src.' to 'mastering_performant_code.'
 * to resolve import path issues in the web companion
 */

import { Logger } from '../utils/Logger.js';

class ImportPathResolver {
    constructor() {
        // Use regex patterns for flexible whitespace
        this.importTransformations = [
            { pattern: /from\s+src\./g, replacement: 'from mastering_performant_code.' },
            { pattern: /import\s+src\./g, replacement: 'import mastering_performant_code.' },
            { pattern: /__import__\(["']src\./g, replacement: '__import__("mastering_performant_code.' },
            { pattern: /'src\./g, replacement: "'mastering_performant_code." },
            { pattern: /"src\./g, replacement: '"mastering_performant_code.' }
        ];

        // Add patterns for relative imports that need to be mapped to specific chapters
        this.relativeImportMappings = [
            // Chapter 1 imports
            { pattern: /from\s+dynamic_array\b/g, replacement: 'from mastering_performant_code.chapter_01.dynamic_array' },
            { pattern: /import\s+dynamic_array\b/g, replacement: 'import mastering_performant_code.chapter_01.dynamic_array' },
            { pattern: /from\s+hash_table\b/g, replacement: 'from mastering_performant_code.chapter_01.hash_table' },
            { pattern: /import\s+hash_table\b/g, replacement: 'import mastering_performant_code.chapter_01.hash_table' },
            { pattern: /from\s+simple_set\b/g, replacement: 'from mastering_performant_code.chapter_01.simple_set' },
            { pattern: /import\s+simple_set\b/g, replacement: 'import mastering_performant_code.chapter_01.simple_set' },
            { pattern: /from\s+analyzer\b/g, replacement: 'from mastering_performant_code.chapter_01.analyzer' },
            { pattern: /import\s+analyzer\b/g, replacement: 'import mastering_performant_code.chapter_01.analyzer' },

            // Chapter 2 imports - including relative imports
            { pattern: /from\s+algorithms\b/g, replacement: 'from mastering_performant_code.chapter_02.algorithms' },
            { pattern: /import\s+algorithms\b/g, replacement: 'import mastering_performant_code.chapter_02.algorithms' },
            { pattern: /from\s+benchmarks\b/g, replacement: 'from mastering_performant_code.chapter_02.benchmarks' },
            { pattern: /import\s+benchmarks\b/g, replacement: 'import mastering_performant_code.chapter_02.benchmarks' },
            { pattern: /from\s+profiler\b/g, replacement: 'from mastering_performant_code.chapter_02.profiler' },
            { pattern: /import\s+profiler\b/g, replacement: 'import mastering_performant_code.chapter_02.profiler' },

            // Handle relative imports for Chapter 2
            { pattern: /from\s+\.algorithms\b/g, replacement: 'from mastering_performant_code.chapter_02.algorithms' },
            { pattern: /from\s+\.benchmarks\b/g, replacement: 'from mastering_performant_code.chapter_02.benchmarks' },
            { pattern: /from\s+\.profiler\b/g, replacement: 'from mastering_performant_code.chapter_02.profiler' },

            // Chapter 3 imports
            { pattern: /from\s+applications\b/g, replacement: 'from mastering_performant_code.chapter_03.applications' },
            { pattern: /import\s+applications\b/g, replacement: 'import mastering_performant_code.chapter_03.applications' },
            { pattern: /from\s+\.applications\b/g, replacement: 'from mastering_performant_code.chapter_03.applications' },
            { pattern: /from\s+dynamic_array\b/g, replacement: 'from mastering_performant_code.chapter_03.dynamic_array' },
            { pattern: /import\s+dynamic_array\b/g, replacement: 'import mastering_performant_code.chapter_03.dynamic_array' },
            { pattern: /from\s+\.dynamic_array\b/g, replacement: 'from mastering_performant_code.chapter_03.dynamic_array' },

            // Add more chapter-specific mappings as needed
            // Chapter 4 imports
            { pattern: /from\s+singly_linked_list\b/g, replacement: 'from mastering_performant_code.chapter_04.singly_linked_list' },
            { pattern: /from\s+doubly_linked_list\b/g, replacement: 'from mastering_performant_code.chapter_04.doubly_linked_list' },
            { pattern: /from\s+\.singly_linked_list\b/g, replacement: 'from mastering_performant_code.chapter_04.singly_linked_list' },
            { pattern: /from\s+\.doubly_linked_list\b/g, replacement: 'from mastering_performant_code.chapter_04.doubly_linked_list' },

            // Chapter 5 imports
            { pattern: /from\s+priority_queue\b/g, replacement: 'from mastering_performant_code.chapter_05.priority_queue' },
            { pattern: /from\s+skip_list\b/g, replacement: 'from mastering_performant_code.chapter_05.skip_list' },
            { pattern: /from\s+\.priority_queue\b/g, replacement: 'from mastering_performant_code.chapter_05.priority_queue' },
            { pattern: /from\s+\.skip_list\b/g, replacement: 'from mastering_performant_code.chapter_05.skip_list' },

            // Chapter 6 imports
            { pattern: /from\s+bst_node\b/g, replacement: 'from mastering_performant_code.chapter_06.bst_node' },
            { pattern: /from\s+\.bst_node\b/g, replacement: 'from mastering_performant_code.chapter_06.bst_node' },

            // Chapter 7 imports
            { pattern: /from\s+avl_node\b/g, replacement: 'from mastering_performant_code.chapter_07.avl_node' },
            { pattern: /from\s+\.avl_node\b/g, replacement: 'from mastering_performant_code.chapter_07.avl_node' },

            // Chapter 8 imports
            { pattern: /from\s+red_black_tree\b/g, replacement: 'from mastering_performant_code.chapter_08.red_black_tree' },
            { pattern: /from\s+\.red_black_tree\b/g, replacement: 'from mastering_performant_code.chapter_08.red_black_tree' },

            // Chapter 9 imports
            { pattern: /from\s+btree_node\b/g, replacement: 'from mastering_performant_code.chapter_09.btree_node' },
            { pattern: /from\s+\.btree_node\b/g, replacement: 'from mastering_performant_code.chapter_09.btree_node' },

            // Chapter 10 imports
            { pattern: /from\s+autocomplete\b/g, replacement: 'from mastering_performant_code.chapter_10.autocomplete' },
            { pattern: /from\s+\.autocomplete\b/g, replacement: 'from mastering_performant_code.chapter_10.autocomplete' },

            // Chapter 11 imports
            { pattern: /from\s+binary_heap\b/g, replacement: 'from mastering_performant_code.chapter_11.binary_heap' },
            { pattern: /from\s+\.binary_heap\b/g, replacement: 'from mastering_performant_code.chapter_11.binary_heap' },
            { pattern: /from\s+heap_sort\b/g, replacement: 'from mastering_performant_code.chapter_11.heap_sort' },
            { pattern: /from\s+\.heap_sort\b/g, replacement: 'from mastering_performant_code.chapter_11.heap_sort' },
            { pattern: /from\s+task_scheduler\b/g, replacement: 'from mastering_performant_code.chapter_11.task_scheduler' },
            { pattern: /from\s+\.task_scheduler\b/g, replacement: 'from mastering_performant_code.chapter_11.task_scheduler' },

            // Chapter 12 imports
            { pattern: /from\s+disjoint_set\b/g, replacement: 'from mastering_performant_code.chapter_12.disjoint_set' },
            { pattern: /from\s+\.disjoint_set\b/g, replacement: 'from mastering_performant_code.chapter_12.disjoint_set' },

            // Chapter 13 imports
            { pattern: /from\s+hash_table\b/g, replacement: 'from mastering_performant_code.chapter_13.hash_table' },
            { pattern: /from\s+\.hash_table\b/g, replacement: 'from mastering_performant_code.chapter_13.hash_table' },

            // Chapter 14 imports
            { pattern: /from\s+bloom_filter\b/g, replacement: 'from mastering_performant_code.chapter_14.bloom_filter' },
            { pattern: /from\s+counting_bloom_filter\b/g, replacement: 'from mastering_performant_code.chapter_14.counting_bloom_filter' },
            { pattern: /from\s+scalable_bloom_filter\b/g, replacement: 'from mastering_performant_code.chapter_14.scalable_bloom_filter' },
            { pattern: /from\s+\.bloom_filter\b/g, replacement: 'from mastering_performant_code.chapter_14.bloom_filter' },
            { pattern: /from\s+\.counting_bloom_filter\b/g, replacement: 'from mastering_performant_code.chapter_14.counting_bloom_filter' },
            { pattern: /from\s+\.scalable_bloom_filter\b/g, replacement: 'from mastering_performant_code.chapter_14.scalable_bloom_filter' },

            // Chapter 15 imports
            { pattern: /from\s+lru_cache\b/g, replacement: 'from mastering_performant_code.chapter_15.lru_cache' },
            { pattern: /from\s+lfu_cache\b/g, replacement: 'from mastering_performant_code.chapter_15.lfu_cache' },
            { pattern: /from\s+real_world_applications\b/g, replacement: 'from mastering_performant_code.chapter_15.real_world_applications' },
            { pattern: /from\s+performance_analyzer\b/g, replacement: 'from mastering_performant_code.chapter_15.performance_analyzer' },
            { pattern: /from\s+\.lru_cache\b/g, replacement: 'from mastering_performant_code.chapter_15.lru_cache' },
            { pattern: /from\s+\.lfu_cache\b/g, replacement: 'from mastering_performant_code.chapter_15.lfu_cache' },
            { pattern: /from\s+\.real_world_applications\b/g, replacement: 'from mastering_performant_code.chapter_15.real_world_applications' },
            { pattern: /from\s+\.performance_analyzer\b/g, replacement: 'from mastering_performant_code.chapter_15.performance_analyzer' },

            // Chapter 16 imports
            { pattern: /from\s+memory_profiler\b/g, replacement: 'from mastering_performant_code.chapter_16.memory_profiler' },
            { pattern: /from\s+object_pool\b/g, replacement: 'from mastering_performant_code.chapter_16.object_pool' },
            { pattern: /from\s+integration_patterns\b/g, replacement: 'from mastering_performant_code.chapter_16.integration_patterns' },
            { pattern: /from\s+\.memory_profiler\b/g, replacement: 'from mastering_performant_code.chapter_16.memory_profiler' },
            { pattern: /from\s+\.object_pool\b/g, replacement: 'from mastering_performant_code.chapter_16.object_pool' },
            { pattern: /from\s+\.integration_patterns\b/g, replacement: 'from mastering_performant_code.chapter_16.integration_patterns' },

            // Additional module patterns for cross-chapter imports
            { pattern: /from\s+btree\b/g, replacement: 'from mastering_performant_code.chapter_09.btree' },
            { pattern: /from\s+\.btree\b/g, replacement: 'from mastering_performant_code.chapter_09.btree' },
            { pattern: /from\s+database_index\b/g, replacement: 'from mastering_performant_code.chapter_09.database_index' },
            { pattern: /from\s+\.database_index\b/g, replacement: 'from mastering_performant_code.chapter_09.database_index' },
            { pattern: /from\s+recursive_bst\b/g, replacement: 'from mastering_performant_code.chapter_06.recursive_bst' },
            { pattern: /from\s+\.recursive_bst\b/g, replacement: 'from mastering_performant_code.chapter_06.recursive_bst' }
        ];

        // Track transformation statistics
        this.stats = {
            totalTransformations: 0,
            successfulTransformations: 0,
            failedTransformations: 0,
            lastTransformation: null
        };
    }

    /**
     * Transform import statements in code
     */
    transformCode(code) {
        const diagnostics = {
            transformations: [],
            warnings: [],
            errors: []
        };

        let transformedCode = code;

        // Apply original src. transformations first
        for (const { pattern, replacement } of this.importTransformations) {
            const matches = transformedCode.match(pattern);

            if (matches) {
                transformedCode = transformedCode.replace(pattern, replacement);
                diagnostics.transformations.push({
                    pattern: pattern.toString(),
                    replacement,
                    count: matches.length,
                    type: 'src_transformation'
                });

                // Only log if there are actual transformations
                if (matches.length > 0) {
                    Logger.debug(`[ImportPathResolver] Replacing pattern: ${pattern} with '${replacement}' (${matches.length} matches)`);
                }
            }
        }

        // Apply relative import mappings only to lines that do not already contain mastering_performant_code on the left side
        let lines = transformedCode.split('\n');
        let totalRelTransformations = 0;
        lines = lines.map(line => {
            let changed = false;
            for (const { pattern, replacement } of this.relativeImportMappings) {
                // Only apply if the left side of the import does not already contain mastering_performant_code
                if (
                    pattern.test(line) &&
                    !/from\s+mastering_performant_code\./.test(line) &&
                    !/import\s+mastering_performant_code\./.test(line)
                ) {
                    const newLine = line.replace(pattern, replacement);
                    if (newLine !== line) {
                        changed = true;
                        totalRelTransformations++;
                        line = newLine;
                    }
                }
            }
            return line;
        });
        if (totalRelTransformations > 0) {
            diagnostics.transformations.push({
                pattern: 'relativeImportMappings',
                replacement: 'chapter-specific',
                count: totalRelTransformations,
                type: 'relative_import_mapping'
            });
        }
        transformedCode = lines.join('\n');

        // Validate the transformation
        const validation = this.validateTransformation(code, transformedCode);
        diagnostics.warnings.push(...validation.warnings);
        diagnostics.errors.push(...validation.errors);

        // Only log summary if there were transformations
        if (diagnostics.transformations.length > 0) {
            const totalTransformations = diagnostics.transformations.reduce((sum, t) => sum + t.count, 0);
            Logger.debug(`[ImportPathResolver] Applied ${totalTransformations} import transformations (${diagnostics.transformations.length} patterns)`);
        }

        return {
            transformedCode,
            diagnostics
        };
    }

    /**
     * Validate that the transformation is safe and correct
     */
    validateTransformation(originalCode, transformedCode) {
        const validation = {
            isValid: true,
            warnings: [],
            errors: []
        };

        // Check if transformation actually changed something
        if (originalCode === transformedCode) {
            validation.warnings.push('No transformations were applied');
        }

        // Check for potential issues
        const issues = this.detectPotentialIssues(transformedCode);
        validation.warnings.push(...issues.warnings);
        validation.errors.push(...issues.errors);

        // Check for syntax errors (basic validation)
        if (this.hasSyntaxErrors(transformedCode)) {
            validation.isValid = false;
            validation.errors.push('Transformed code contains syntax errors');
        }

        return validation;
    }

    /**
     * Detect potential issues in transformed code
     */
    detectPotentialIssues(code) {
        const issues = {
            warnings: [],
            errors: []
        };

        // Check for double transformations
        if (code.includes('mastering_performant_code.mastering_performant_code')) {
            issues.warnings.push('Potential double transformation detected');
        }

        // Check for incomplete transformations
        if (code.includes('src.') && code.includes('mastering_performant_code.')) {
            issues.warnings.push('Mixed import patterns detected - some imports may not be transformed');
        }

        // Check for common Python syntax issues
        if (code.includes('from mastering_performant_code. import')) {
            issues.errors.push('Invalid import statement: missing module name after dot');
        }

        return issues;
    }

    /**
     * Basic syntax validation
     */
    hasSyntaxErrors(code) {
        // Basic checks for common syntax issues
        const syntaxChecks = [
            /from\s+mastering_performant_code\.\s*import/, // from mastering_performant_code. import
            /import\s+mastering_performant_code\.\s*$/, // import mastering_performant_code. (at end)
            /from\s+mastering_performant_code\.\s*$/, // from mastering_performant_code. (at end)
        ];

        return syntaxChecks.some(pattern => pattern.test(code));
    }

    /**
     * Get import mapping information
     */
    getImportMapping() {
        return { ...this.importTransformations };
    }

    /**
     * Get transformation statistics
     */
    getStats() {
        return { ...this.stats };
    }

    /**
     * Reset statistics
     */
    resetStats() {
        this.stats = {
            totalTransformations: 0,
            successfulTransformations: 0,
            failedTransformations: 0,
            lastTransformation: null
        };
        Logger.info('Import path resolver statistics reset');
    }

    /**
     * Test the resolver with sample code
     */
    testTransformation() {
        const testCases = [
            {
                name: 'Basic from import',
                code: 'from src.chapter_01.dynamic_array import DynamicArray',
                expected: 'from mastering_performant_code.chapter_01.dynamic_array import DynamicArray'
            },
            {
                name: 'Basic import',
                code: 'import src.chapter_02.algorithms',
                expected: 'import mastering_performant_code.chapter_02.algorithms'
            },
            {
                name: 'Multiple imports',
                code: `from src.chapter_01 import dynamic_array
import src.chapter_02.algorithms as algo`,
                expected: `from mastering_performant_code.chapter_01 import dynamic_array
import mastering_performant_code.chapter_02.algorithms as algo`
            }
        ];

        const results = testCases.map(testCase => {
            const result = this.transformCode(testCase.code);
            const passed = result.transformedCode === testCase.expected;

            return {
                name: testCase.name,
                passed,
                original: testCase.code,
                transformed: result.transformedCode,
                expected: testCase.expected
            };
        });

        const passedCount = results.filter(r => r.passed).length;
        Logger.info(`Import path resolver test: ${passedCount}/${results.length} tests passed`);

        return results;
    }
}

export { ImportPathResolver }; 