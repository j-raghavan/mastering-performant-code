#!/usr/bin/env node

/**
 * Prepare deployment script for GitHub Pages
 * This script ensures all necessary files are in place for deployment
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rootDir = path.resolve(__dirname, '../..');
const webCompanionDir = path.resolve(__dirname, '..');
const publicDir = path.resolve(webCompanionDir, 'public');
const assetsDir = path.resolve(publicDir, 'assets');

console.log('🚀 Preparing deployment for GitHub Pages...');

// Ensure public directory exists
if (!fs.existsSync(publicDir)) {
    fs.mkdirSync(publicDir, { recursive: true });
    console.log('✅ Created public directory');
}

// Ensure assets directory exists
if (!fs.existsSync(assetsDir)) {
    fs.mkdirSync(assetsDir, { recursive: true });
    console.log('✅ Created assets directory');
}

// Create package metadata for the web app
const packageMetadata = {
    package: {
        name: "mastering_performant_code",
        version: "1.0.0",
        release_version: "v0.1.2",
        wheel_url: "/mastering-performant-code/assets/mastering_performant_code-1.0.0-py3-none-any.whl"
    },
    github: {
        repository: "j-raghavan/mastering-performant-code",
        release_tag: "v0.1.2"
    },
    deployment: {
        url: "https://j-raghavan.github.io/mastering-performant-code/",
        last_updated: new Date().toISOString()
    }
};

// Write package metadata
const metadataPath = path.join(publicDir, 'package-metadata.json');
fs.writeFileSync(metadataPath, JSON.stringify(packageMetadata, null, 2));
console.log('✅ Created package-metadata.json');

// Copy wheel package to assets directory
const wheelPath = path.join(rootDir, 'dist', 'mastering_performant_code-1.0.0-py3-none-any.whl');
const publicWheelPath = path.join(assetsDir, 'mastering_performant_code-1.0.0-py3-none-any.whl');

if (fs.existsSync(wheelPath)) {
    fs.copyFileSync(wheelPath, publicWheelPath);
    console.log('✅ Copied wheel package to assets directory');
} else {
    console.log('⚠️  Wheel package not found in dist directory');
    console.log('   Please build the wheel package first: python -m build --wheel');
}

// Create a simple health check file
const healthCheck = {
    status: "healthy",
    timestamp: new Date().toISOString(),
    version: "1.0.0",
    deployment: "github-pages",
    wheel_available: fs.existsSync(publicWheelPath)
};

const healthCheckPath = path.join(publicDir, 'health.json');
fs.writeFileSync(healthCheckPath, JSON.stringify(healthCheck, null, 2));
console.log('✅ Created health.json');

console.log('🎉 Deployment preparation complete!');
console.log('');
console.log('Next steps:');
console.log('1. Commit and push your changes');
console.log('2. The GitHub Actions workflow will automatically deploy to GitHub Pages');
console.log('3. Your app will be available at: https://j-raghavan.github.io/mastering-performant-code/'); 