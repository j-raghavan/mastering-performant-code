#!/usr/bin/env node

/**
 * Add main blocks to Python source files
 * 
 * This script scans Python source files and adds `if __name__ == "__main__": main()` 
 * blocks to files that don't have them, making them executable via Pyodide.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get current directory for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const SRC_DIR = path.join(__dirname, '../../src');
const EXCLUDED_FILES = ['__init__.py', 'demo.py']; // demo.py already has main blocks
const EXCLUDED_DIRS = ['__pycache__', '.git'];

/**
 * Check if a Python file already has a main block
 */
function hasMainBlock(content) {
    const lines = content.split('\n');
    for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed === 'if __name__ == "__main__":' ||
            trimmed.startsWith('if __name__ == "__main__"')) {
            return true;
        }
    }
    return false;
}

/**
 * Generate a main function for a Python file
 */
function generateMainFunction(filePath, className = null) {
    const fileName = path.basename(filePath, '.py');
    const moduleName = fileName;

    let mainContent = '\n\ndef main():\n';
    mainContent += '    """Main function to demonstrate the module functionality."""\n';
    mainContent += `    print(f"Running {moduleName} demonstration...")\n`;
    mainContent += '    print("=" * 50)\n\n';

    // If there's a main class, create an instance and demonstrate it
    if (className) {
        mainContent += `    # Create instance of ${className}\n`;
        mainContent += `    try:\n`;
        mainContent += `        instance = ${className}()\n`;
        mainContent += `        print(f"✓ Created {className} instance successfully")\n`;
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
        mainContent += `        print(f"✗ Error creating {className} instance: {e}")\n`;
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
 * Add main block to a Python file
 */
function addMainBlock(filePath) {
    try {
        const content = fs.readFileSync(filePath, 'utf8');

        // Check if file already has a main block
        if (hasMainBlock(content)) {
            console.log(`✓ ${filePath} already has main block`);
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
                    // Skip classes that are clearly utilities or helpers
                    if (!className.includes('Node') &&
                        !className.includes('Iterator') &&
                        !className.includes('Memory') &&
                        !className.includes('Info') &&
                        !className.includes('Result') &&
                        !className.includes('Config')) {
                        mainClass = className;
                        break; // Use the first non-utility class
                    }
                }
            }
        }

        // If no main class found, use the first class
        if (!mainClass && classes.length > 0) {
            mainClass = classes[0];
        }

        // Generate main function
        const mainFunction = generateMainFunction(filePath, mainClass);

        // Add main block
        const newContent = content + mainFunction + 'if __name__ == "__main__":\n    main()\n';

        // Write back to file
        fs.writeFileSync(filePath, newContent, 'utf8');

        const classInfo = mainClass ? ` (with ${mainClass} demo)` : '';
        console.log(`✓ Added main block to ${filePath}${classInfo}`);
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
    let filesModified = 0;

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
            filesModified += subResult.modified;
        } else if (item.endsWith('.py') && !EXCLUDED_FILES.includes(item)) {
            // Process Python files
            filesProcessed++;
            if (addMainBlock(fullPath)) {
                filesModified++;
            }
        }
    }

    return { processed: filesProcessed, modified: filesModified };
}

/**
 * Main function
 */
function main() {
    console.log('🔧 Adding main blocks to Python source files...\n');

    if (!fs.existsSync(SRC_DIR)) {
        console.error(`✗ Source directory not found: ${SRC_DIR}`);
        process.exit(1);
    }

    const result = scanDirectory(SRC_DIR);

    console.log('\n📊 Summary:');
    console.log(`   Files processed: ${result.processed}`);
    console.log(`   Files modified: ${result.modified}`);
    console.log(`   Files already had main blocks: ${result.processed - result.modified}`);

    if (result.modified > 0) {
        console.log('\n✅ Successfully added main blocks to Python source files!');
        console.log('   These files can now be executed directly via Pyodide.');
    } else {
        console.log('\nℹ️  No files needed modification - all already have main blocks!');
    }
}

// Run the script
main();

export { addMainBlock, hasMainBlock, generateMainFunction }; 