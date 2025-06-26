/**
 * Test Runner Service
 * 
 * Handles test execution using pytest in Pyodide environment
 */

import { Logger } from '../utils/Logger.js';

class TestRunner {
    constructor(pyodideExecutor) {
        this.pyodideExecutor = pyodideExecutor;
        this.testResults = new Map();
        this.isRunning = false;
    }

    /**
     * Initialize the test runner
     */
    async initialize() {
        try {
            Logger.info('🧪 Initializing TestRunner...');

            // Ensure Pyodide is ready
            if (!this.pyodideExecutor.isReady()) {
                await this.pyodideExecutor.initialize();
            }

            // Set up pytest environment
            await this.setupPytestEnvironment();

            Logger.info('✅ TestRunner initialized successfully');
        } catch (error) {
            Logger.error('❌ Failed to initialize TestRunner:', error);
            throw error;
        }
    }

    /**
     * Set up pytest environment
     */
    async setupPytestEnvironment() {
        try {
            // Configure pytest for Pyodide environment
            await this.pyodideExecutor.execute(`
import sys
import os

# Configure pytest for Pyodide
os.environ['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] = '1'
os.environ['PYTEST_ADDOPTS'] = '--tb=short --quiet'

# Add our content directory to Python path
if '/generated/content' not in sys.path:
    sys.path.insert(0, '/generated/content')
            `, {
                measurePerformance: false // Disable performance measurement during setup
            });

            Logger.info('✅ Pytest environment configured');
        } catch (error) {
            Logger.error('❌ Failed to setup pytest environment:', error);
            throw error;
        }
    }

    /**
     * Run tests for a specific chapter
     */
    async runChapterTests(chapterId) {
        if (this.isRunning) {
            throw new Error('Test execution already in progress');
        }

        this.isRunning = true;

        try {
            Logger.info(`🧪 Running tests for chapter: ${chapterId}`);

            const results = [];
            const testFiles = await this.getTestFiles(chapterId);

            for (const testFile of testFiles) {
                try {
                    const fileResults = await this.runTestFile(testFile);
                    results.push(...fileResults);
                } catch (error) {
                    Logger.error(`Failed to run test file ${testFile.name}:`, error);
                    results.push({
                        name: testFile.name,
                        status: 'error',
                        duration: 0,
                        output: '',
                        error: error.message,
                        file: testFile.name
                    });
                }
            }

            // Store results
            this.testResults.set(chapterId, results);

            Logger.info(`✅ Chapter tests completed: ${results.length} tests`);
            return results;

        } catch (error) {
            Logger.error('❌ Failed to run chapter tests:', error);
            throw error;
        } finally {
            this.isRunning = false;
        }
    }

    /**
     * Run a single test file
     */
    async runTestFile(testFile) {
        try {
            Logger.info(`🧪 Running test file: ${testFile.name}`);

            // Create test runner script
            const testScript = this.createTestScript(testFile);

            // Execute test
            const result = await this.pyodideExecutor.execute(testScript, {
                timeout: 60000, // 60 seconds for tests
                captureOutput: true
            });

            // Parse test results
            const testResults = this.parseTestResults(result.output, testFile.name);

            Logger.info(`✅ Test file completed: ${testResults.length} tests`);
            return testResults;

        } catch (error) {
            Logger.error(`❌ Failed to run test file ${testFile.name}:`, error);
            throw error;
        }
    }

    /**
     * Run a single test by name
     */
    async runSingleTest(chapterId, testName) {
        try {
            Logger.info(`🧪 Running single test: ${testName}`);

            const testScript = `
import pytest
import sys
import os

# Add our content directory to Python path
if '/generated/content' not in sys.path:
    sys.path.insert(0, '/generated/content')

# Run specific test
pytest.main(['-v', '-k', '${testName}', '--tb=short'])
            `;

            const result = await this.pyodideExecutor.execute(testScript, {
                timeout: 30000,
                captureOutput: true
            });

            const testResults = this.parseTestResults(result.output, 'single_test');
            return testResults[0] || null;

        } catch (error) {
            Logger.error(`❌ Failed to run single test ${testName}:`, error);
            throw error;
        }
    }

    /**
     * Get test files for a chapter
     */
    async getTestFiles(chapterId) {
        try {
            // This would typically come from the ContentSyncService
            // For now, we'll use a simple approach
            const testFiles = [
                { name: 'test_analyzer.py', path: `${chapterId}/tests/test_analyzer.py` },
                { name: 'test_dynamic_array.py', path: `${chapterId}/tests/test_dynamic_array.py` },
                { name: 'test_hash_table.py', path: `${chapterId}/tests/test_hash_table.py` }
            ];

            return testFiles;
        } catch (error) {
            Logger.error(`Failed to get test files for chapter ${chapterId}:`, error);
            return [];
        }
    }

    /**
     * Create test execution script
     */
    createTestScript(testFile) {
        return `
import pytest
import sys
import os
import json
import time

# Add our content directory to Python path
if '/generated/content' not in sys.path:
    sys.path.insert(0, '/generated/content')

# Configure pytest output
class TestResultCollector:
    def __init__(self):
        self.results = []
        self.current_test = None
    
    def pytest_runtest_logreport(self, report):
        if report.when == 'call':
            result = {
                'name': report.nodeid,
                'status': report.outcome,
                'duration': report.duration,
                'output': str(report.longrepr) if report.longrepr else '',
                'file': report.fspath.basename if hasattr(report, 'fspath') else 'unknown'
            }
            self.results.append(result)

# Run tests
collector = TestResultCollector()
pytest.main(['-v', '--tb=short', '--quiet'], plugins=[collector])

# Output results as JSON
print("TEST_RESULTS_START")
print(json.dumps(collector.results))
print("TEST_RESULTS_END")
        `;
    }

    /**
     * Parse test results from output
     */
    parseTestResults(output, fileName) {
        try {
            const results = [];
            const lines = output.split('\n');
            let inResults = false;
            let jsonData = '';

            for (const line of lines) {
                if (line === 'TEST_RESULTS_START') {
                    inResults = true;
                    continue;
                }
                if (line === 'TEST_RESULTS_END') {
                    break;
                }
                if (inResults) {
                    jsonData += line;
                }
            }

            if (jsonData) {
                const parsed = JSON.parse(jsonData);
                return parsed.map(result => ({
                    ...result,
                    file: fileName
                }));
            }

            // Fallback parsing for non-JSON output
            return this.parseFallbackResults(output, fileName);

        } catch (error) {
            Logger.error('Failed to parse test results:', error);
            return [{
                name: 'parse_error',
                status: 'error',
                duration: 0,
                output: output,
                error: 'Failed to parse test results',
                file: fileName
            }];
        }
    }

    /**
     * Fallback parsing for test results
     */
    parseFallbackResults(output, fileName) {
        const results = [];
        const lines = output.split('\n');

        for (const line of lines) {
            if (line.includes('::') && (line.includes('PASSED') || line.includes('FAILED') || line.includes('ERROR'))) {
                const parts = line.split('::');
                const testName = parts[parts.length - 1].split(' ')[0];
                const status = line.includes('PASSED') ? 'passed' :
                    line.includes('FAILED') ? 'failed' : 'error';

                results.push({
                    name: testName,
                    status: status,
                    duration: 0,
                    output: line,
                    error: status !== 'passed' ? line : null,
                    file: fileName
                });
            }
        }

        return results;
    }

    /**
     * Discover available tests
     */
    async discoverTests(chapterId) {
        try {
            const testFiles = await this.getTestFiles(chapterId);
            const tests = [];

            for (const testFile of testFiles) {
                const discoveryScript = `
import pytest
import sys
import os

# Add our content directory to Python path
if '/generated/content' not in sys.path:
    sys.path.insert(0, '/generated/content')

# Discover tests
collector = pytest.main(['--collect-only', '-q'])
            `;

                try {
                    await this.pyodideExecutor.execute(discoveryScript);
                    tests.push({
                        file: testFile.name,
                        path: testFile.path
                    });
                } catch (error) {
                    Logger.warn(`Failed to discover tests in ${testFile.name}:`, error);
                }
            }

            return tests;
        } catch (error) {
            Logger.error(`Failed to discover tests for chapter ${chapterId}:`, error);
            return [];
        }
    }

    /**
     * Get test results for a chapter
     */
    getTestResults(chapterId) {
        return this.testResults.get(chapterId) || [];
    }

    /**
     * Get all test results
     */
    getAllTestResults() {
        const allResults = [];
        for (const [chapterId, results] of this.testResults) {
            allResults.push({
                chapterId,
                results
            });
        }
        return allResults;
    }

    /**
     * Clear test results
     */
    clearResults(chapterId = null) {
        if (chapterId) {
            this.testResults.delete(chapterId);
        } else {
            this.testResults.clear();
        }
    }

    /**
     * Get test statistics
     */
    getTestStats(chapterId = null) {
        const results = chapterId ?
            this.testResults.get(chapterId) || [] :
            this.getAllTestResults().flatMap(r => r.results);

        const stats = {
            total: results.length,
            passed: 0,
            failed: 0,
            error: 0,
            skipped: 0
        };

        results.forEach(result => {
            if (result.status === 'passed') stats.passed++;
            else if (result.status === 'failed') stats.failed++;
            else if (result.status === 'error') stats.error++;
            else if (result.status === 'skipped') stats.skipped++;
        });

        return stats;
    }

    /**
     * Check if tests are running
     */
    isTestRunning() {
        return this.isRunning;
    }
}

export { TestRunner }; 