#!/usr/bin/env node

/**
 * Fix broken main blocks in Python source files
 * 
 * This script fixes main functions that were generated with undefined variables
 * like moduleName and className.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get current directory for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const SRC_DIR = path.join(__dirname, '../../src');
const EXCLUDED_FILES = ['__init__.py', 'demo.py'];
const EXCLUDED_DIRS = ['__pycache__', '.git'];

/**
 * Check if a main function has broken references
 */
function hasBrokenMainFunction(content) {
    const lines = content.split('\n');
    for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed.includes('moduleName') ||
            trimmed.includes('className') ||
            (trimmed.includes('print(f"Running') && !trimmed.includes('{moduleName}'))) {
            return true;
        }
    }
    return false;
}

/**
 * Generate a proper main function for a Python file
 */
function generateMainFunction(filePath, className = null) {
    const fileName = path.basename(filePath, '.py');
    const moduleName = fileName;

    let mainContent = '\n\ndef main():\n';
    mainContent += '    """Main function to demonstrate the module functionality."""\n';
    mainContent += `    print(f"Running ${moduleName} demonstration...")\n`;
    mainContent += '    print("=" * 50)\n\n';

    // If there's a main class, create an instance and demonstrate it
    if (className) {
        mainContent += `    # Create instance of ${className}\n`;
        mainContent += `    try:\n`;
        mainContent += `        instance = ${className}()\n`;
        mainContent += `        print(f"✓ Created ${className} instance successfully")\n`;
        mainContent += `        print(f"  Instance: {instance}")\n\n`;

        // Add some basic demonstration based on the class type
        if (className.includes('Array') || className.includes('List')) {
            mainContent += `        # Demonstrate basic operations\n`;
            mainContent += `        print("Testing basic operations...")\n`;
            mainContent += `        instance.append(1)\n`;
            mainContent += `        instance.append(2)\n`;
            mainContent += `        instance.append(3)\n`;
            mainContent += `        print(f"  After adding elements: {instance}")\n`;
            mainContent += `        print(f"  Length: {len(instance)}")\n`;
        } else if (className.includes('Hash') || className.includes('Table')) {
            mainContent += `        # Demonstrate basic operations\n`;
            mainContent += `        print("Testing basic operations...")\n`;
            mainContent += `        instance["key1"] = "value1"\n`;
            mainContent += `        instance["key2"] = "value2"\n`;
            mainContent += `        print(f"  After adding elements: {instance}")\n`;
            mainContent += `        print(f"  Size: {len(instance)}")\n`;
        } else if (className.includes('Tree') || className.includes('BST')) {
            mainContent += `        # Demonstrate basic operations\n`;
            mainContent += `        print("Testing basic operations...")\n`;
            mainContent += `        instance.insert(5)\n`;
            mainContent += `        instance.insert(3)\n`;
            mainContent += `        instance.insert(7)\n`;
            mainContent += `        print(f"  After inserting elements: {instance}")\n`;
        } else {
            mainContent += `        # Demonstrate basic functionality\n`;
            mainContent += `        print("Testing basic functionality...")\n`;
            mainContent += `        print(f"  Instance type: {type(instance)}")\n`;
        }

        mainContent += `    except Exception as e:\n`;
        mainContent += `        print(f"✗ Error creating ${className} instance: {e}")\n`;
        mainContent += `        return False\n\n`;
    } else {
        // For files without main classes, just show module info
        mainContent += '    # Module demonstration\n';
        mainContent += '    print("Module loaded successfully!")\n';
        mainContent += '    print("Available for import and interactive use.")\n\n';
    }

    // Add some basic demonstration
    mainContent += '    # Module status\n';
    mainContent += '    print("✓ Module loaded successfully!")\n';
    mainContent += '    print("✓ Ready for interactive use in Pyodide.")\n\n';

    mainContent += '    return True\n\n';

    return mainContent;
}

/**
 * Fix main block in a Python file
 */
function fixMainBlock(filePath) {
    try {
        const content = fs.readFileSync(filePath, 'utf8');

        // Check if file has a broken main function
        if (!hasBrokenMainFunction(content)) {
            console.log(`✓ ${filePath} has valid main function`);
            return false;
        }

        // Find the main class if any
        const lines = content.split('\n');
        let mainClass = null;
        const classes = [];

        for (const line of lines) {
            const trimmed = line.trim();
            if (trimmed.startsWith('class ') && trimmed.includes(':')) {
                const classMatch = trimmed.match(/class\s+(\w+)/);
                if (classMatch) {
                    const className = classMatch[1];
                    classes.push(className);

                    // Prioritize classes that are likely to be the main implementation
                    if (!className.includes('Node') &&
                        !className.includes('Iterator') &&
                        !className.includes('Memory') &&
                        !className.includes('Info') &&
                        !className.includes('Result') &&
                        !className.includes('Config')) {
                        mainClass = className;
                        break;
                    }
                }
            }
        }

        // If no main class found, use the first class
        if (!mainClass && classes.length > 0) {
            mainClass = classes[0];
        }

        // Remove the broken main function and main block
        const linesArray = content.split('\n');
        let newLines = [];
        let inMainFunction = false;
        let inMainBlock = false;

        for (const line of linesArray) {
            if (line.trim().startsWith('def main()')) {
                inMainFunction = true;
                continue;
            }

            if (inMainFunction) {
                if (line.trim() === 'if __name__ == "__main__":') {
                    inMainFunction = false;
                    inMainBlock = true;
                    continue;
                }
                if (line.trim() === '    main()') {
                    inMainBlock = false;
                    continue;
                }
                if (inMainBlock) {
                    continue;
                }
            }

            if (!inMainFunction && !inMainBlock) {
                newLines.push(line);
            }
        }

        // Generate new main function
        const mainFunction = generateMainFunction(filePath, mainClass);

        // Add new main block
        const newContent = newLines.join('\n') + mainFunction + 'if __name__ == "__main__":\n    main()\n';

        // Write back to file
        fs.writeFileSync(filePath, newContent, 'utf8');

        const classInfo = mainClass ? ` (with ${mainClass} demo)` : '';
        console.log(`✓ Fixed main block in ${filePath}${classInfo}`);
        return true;

    } catch (error) {
        console.error(`✗ Error processing ${filePath}:`, error.message);
        return false;
    }
}

/**
 * Recursively scan directory for Python files
 */
function scanDirectory(dirPath, relativePath = '') {
    const items = fs.readdirSync(dirPath);
    let filesProcessed = 0;
    let filesFixed = 0;

    for (const item of items) {
        const fullPath = path.join(dirPath, item);
        const itemRelativePath = path.join(relativePath, item);

        // Skip excluded directories
        if (fs.statSync(fullPath).isDirectory()) {
            if (EXCLUDED_DIRS.includes(item)) {
                continue;
            }

            // Recursively scan subdirectories
            const subResult = scanDirectory(fullPath, itemRelativePath);
            filesProcessed += subResult.processed;
            filesFixed += subResult.fixed;
        } else if (item.endsWith('.py') && !EXCLUDED_FILES.includes(item)) {
            // Process Python files
            filesProcessed++;
            if (fixMainBlock(fullPath)) {
                filesFixed++;
            }
        }
    }

    return { processed: filesProcessed, fixed: filesFixed };
}

/**
 * Main function
 */
function main() {
    console.log('🔧 Fixing broken main blocks in Python source files...\n');

    if (!fs.existsSync(SRC_DIR)) {
        console.error(`✗ Source directory not found: ${SRC_DIR}`);
        process.exit(1);
    }

    const result = scanDirectory(SRC_DIR);

    console.log('\n📊 Summary:');
    console.log(`   Files processed: ${result.processed}`);
    console.log(`   Files fixed: ${result.fixed}`);
    console.log(`   Files already valid: ${result.processed - result.fixed}`);

    if (result.fixed > 0) {
        console.log('\n✅ Successfully fixed main blocks in Python source files!');
        console.log('   These files can now be executed directly via Pyodide.');
    } else {
        console.log('\nℹ️  No files needed fixing - all main blocks are valid!');
    }
}

// Run the script
main(); 