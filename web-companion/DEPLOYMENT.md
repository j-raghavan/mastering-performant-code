# Deployment Guide - GitHub Pages

This guide explains how to deploy the Mastering Performant Code Interactive Companion to GitHub Pages.

## Overview

The web companion will be deployed to: `https://j-raghavan.github.io/mastering-performant-code/`

## Prerequisites

1. **GitHub Pages enabled** on your repository
2. **GitHub Actions permissions** configured
3. **Wheel package built** and available as a GitHub release

## Deployment Process

### 1. Enable GitHub Pages

1. Go to your repository settings
2. Navigate to "Pages" in the left sidebar
3. Under "Source", select "GitHub Actions"
4. This will allow the workflow to deploy automatically

### 2. Build and Release Wheel Package

Before deploying the web companion, ensure your Python wheel package is built and released:

```bash
# Build the wheel package
python -m build --wheel

# Create a new release on GitHub with the wheel file
# Tag: v0.1.2
# Release: https://github.com/j-raghavan/mastering-performant-code/releases/download/v0.1.2/mastering_performant_code-1.0.0-py3-none-any.whl
```

### 3. Deploy Web Companion

The deployment happens automatically when you push to the main branch:

```bash
# Commit your changes
git add .
git commit -m "Deploy web companion to GitHub Pages"
git push origin main
```

### 4. Manual Deployment

To trigger deployment manually:

1. Go to your repository on GitHub
2. Navigate to "Actions" tab
3. Select "Deploy to GitHub Pages" workflow
4. Click "Run workflow"

## Configuration Files

### Vite Configuration (`vite.config.js`)

```javascript
export default defineConfig({
    base: '/mastering-performant-code/', // GitHub Pages subdirectory
    // ... other config
});
```

### Package Manager (`src/services/PackageManager.js`)

```javascript
this.packageUrl = 'https://github.com/j-raghavan/mastering-performant-code/releases/download/v0.1.2/mastering_performant_code-1.0.0-py3-none-any.whl';
```

### GitHub Workflow (`.github/workflows/deploy-gh-pages.yml`)

The workflow:
1. Sets up Node.js environment
2. Installs dependencies
3. Prepares deployment files
4. Builds the application
5. Deploys to GitHub Pages

## Local Development

For local development, the app runs on `http://localhost:3000`:

```bash
cd web-companion
npm run dev
```

## Troubleshooting

### Common Issues

1. **404 Errors**: Ensure the `base` path in `vite.config.js` matches your repository name
2. **Package Not Found**: Verify the wheel package URL in `PackageManager.js` is correct
3. **Build Failures**: Check that all dependencies are properly installed

### Debugging

1. Check GitHub Actions logs for build errors
2. Verify the wheel package is accessible at the specified URL
3. Test the application locally before deploying

## File Structure

```
web-companion/
├── dist/                    # Built files (generated)
├── public/                  # Static assets
│   ├── package-metadata.json
│   └── health.json
├── src/                     # Source code
├── scripts/
│   └── prepare-deployment.js
├── vite.config.js          # Build configuration
└── package.json            # Dependencies and scripts
```

## Monitoring

After deployment, you can monitor the application:

- **Health Check**: `https://j-raghavan.github.io/mastering-performant-code/health.json`
- **Package Metadata**: `https://j-raghavan.github.io/mastering-performant-code/package-metadata.json`

## Security

- The web companion runs entirely in the browser
- No server-side code is executed
- All Python code runs in Pyodide (WebAssembly)
- Wheel package is downloaded from GitHub releases (trusted source) 