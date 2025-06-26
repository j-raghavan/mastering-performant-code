/**
 * Type definitions for the Pyodide Interactive Companion
 */

// Chapter and Content Types
export interface Chapter {
    id: string;
    number: number;
    title: string;
    description: string;
    sourceFiles: SourceFile[];
    testFiles: TestFile[];
    demoFile: string | null;
    benchmarkFiles: string[];
    dependencies: string[];
    estimatedTime: number;
    complexity: 'beginner' | 'intermediate' | 'advanced';
    order: number;
}

export interface SourceFile {
    name: string;
    path: string;
    content: string;
    size: number;
    lines: number;
    type: 'demo' | 'implementation' | 'analyzer' | 'benchmark' | 'config' | 'test';
    dependencies: string[];
    docstring: string | null;
    classes: ClassInfo[];
    functions: FunctionInfo[];
    imports: string[];
}

export interface TestFile extends SourceFile {
    type: 'test';
}

export interface ClassInfo {
    name: string;
    line: number;
    docstring: string | null;
}

export interface FunctionInfo {
    name: string;
    line: number;
    docstring: string | null;
}

// Application State Types
export interface ApplicationState {
    currentChapter: Chapter | null;
    currentFile: SourceFile | null;
    userCode: Record<string, string>;
    executionResults: ExecutionResult[];
    testResults: TestResult[];
    performanceMetrics: PerformanceMetrics[];
    isLoading: boolean;
    error: string | null;
    theme: 'light' | 'dark';
}

// Execution Types
export interface ExecutionResult {
    id: string;
    timestamp: number;
    code: string;
    output: string;
    error: string | null;
    executionTime: number;
    memoryUsage: MemoryInfo;
    warnings: string[];
    success: boolean;
}

export interface ExecutionOptions {
    timeout?: number;
    captureOutput?: boolean;
    measurePerformance?: boolean;
}

export interface MemoryInfo {
    used: number;
    total: number;
    peak: number;
}

// Test Types
export interface TestResult {
    id: string;
    name: string;
    status: 'passed' | 'failed' | 'skipped' | 'running';
    duration: number;
    output: string;
    error: string | null;
    assertions: AssertionResult[];
    timestamp: number;
}

export interface AssertionResult {
    name: string;
    status: 'passed' | 'failed';
    message: string;
}

// Performance Types
export interface PerformanceMetrics {
    id: string;
    algorithm: string;
    inputSize: number;
    executionTime: number;
    memoryUsage: MemoryInfo;
    complexity: string;
    timestamp: number;
}

export interface ComparisonResult {
    algorithms: string[];
    metrics: PerformanceMetrics[];
    chartData: ChartData;
}

export interface ChartData {
    labels: string[];
    datasets: ChartDataset[];
}

export interface ChartDataset {
    label: string;
    data: number[];
    borderColor: string;
    backgroundColor: string;
}

// Service Interfaces
export interface IAppController {
    initialize(): Promise<void>;
    loadChapter(chapterId: string): Promise<void>;
    getCurrentState(): ApplicationState;
    subscribe(event: string, callback: Function): void;
    unsubscribe(event: string, callback: Function): void;
}

export interface IChapterManager {
    getChapter(id: string): Promise<Chapter>;
    getAllChapters(): Chapter[];
    getNextChapter(currentId: string): Chapter | null;
    getPreviousChapter(currentId: string): Chapter | null;
    markAsCompleted(chapterId: string): void;
}

export interface ICodeEditor {
    setValue(code: string): void;
    getValue(): string;
    insertText(text: string, position?: Position): void;
    format(): void;
    focus(): void;
    markError(line: number, message: string): void;
    clearErrors(): void;
    onCodeChange(callback: (code: string) => void): void;
}

export interface IPythonExecutor {
    execute(code: string, options?: ExecutionOptions): Promise<ExecutionResult>;
    installPackage(packageName: string): Promise<void>;
    getMemoryUsage(): MemoryInfo;
    interrupt(): void;
    reset(): Promise<void>;
}

export interface ITestRunner {
    runTests(testPath: string): Promise<TestResult[]>;
    runSingleTest(testPath: string, testName: string): Promise<TestResult>;
    discoverTests(path: string): string[];
    getBenchmarkResults(): PerformanceMetrics[];
}

export interface IPerformanceAnalyzer {
    analyzeExecution(result: ExecutionResult): PerformanceMetrics;
    compareAlgorithms(results: ExecutionResult[]): ComparisonResult;
    generateComplexityChart(data: PerformanceMetrics[]): ChartData;
    trackMemoryUsage(callback: (usage: MemoryInfo) => void): void;
}

export interface IStorageService {
    saveUserCode(chapterId: string, fileId: string, code: string): Promise<void>;
    getUserCode(chapterId: string, fileId: string): Promise<string | null>;
    saveProgress(chapterId: string, progress: Progress): Promise<void>;
    getProgress(chapterId: string): Promise<Progress | null>;
    clearUserData(): Promise<void>;
}

export interface IContentSyncService {
    syncChapterContent(chapterId: string): Promise<Chapter>;
    parseSourceFiles(chapterPath: string): Promise<SourceFile[]>;
    extractTestFiles(testPath: string): Promise<TestFile[]>;
    generateChapterMetadata(): Promise<Chapter[]>;
    watchForChanges(callback: (changes: ContentChange[]) => void): void;
}

// Utility Types
export interface Position {
    line: number;
    column: number;
}

export interface Progress {
    chapterId: string;
    completedFiles: string[];
    lastAccessed: number;
    timeSpent: number;
}

export interface ContentChange {
    type: 'added' | 'modified' | 'deleted';
    path: string;
    timestamp: number;
}

// Event Types
export interface AppEvents {
    'chapter:loaded': Chapter;
    'code:executed': ExecutionResult;
    'tests:completed': TestResult[];
    'performance:analyzed': PerformanceMetrics;
    'error:occurred': Error;
    'state:changed': ApplicationState;
}

// Configuration Types
export interface AppConfig {
    pyodideVersion: string;
    defaultTimeout: number;
    maxMemoryUsage: number;
    enableAnalytics: boolean;
    theme: 'light' | 'dark';
    autoSave: boolean;
}

// Error Types
export interface AppError extends Error {
    code: string;
    context?: any;
    recoverable: boolean;
}

// Chart Configuration
export interface ChartConfig {
    type: 'line' | 'bar' | 'scatter';
    data: ChartData;
    options: {
        responsive: boolean;
        maintainAspectRatio: boolean;
        plugins: {
            title: {
                display: boolean;
                text: string;
            };
            legend: {
                display: boolean;
            };
        };
        scales?: {
            x?: {
                title: {
                    display: boolean;
                    text: string;
                };
            };
            y?: {
                title: {
                    display: boolean;
                    text: string;
                };
            };
        };
    };
} 