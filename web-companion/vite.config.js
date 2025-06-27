import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
    root: '.',
    publicDir: 'public',
    base: '/mastering-performant-code/',
    build: {
        outDir: 'dist',
        assetsDir: 'assets',
        sourcemap: true,
        rollupOptions: {
            input: {
                main: resolve(__dirname, 'index.html')
            }
        }
    },
    server: {
        port: 3000,
        host: true,
        open: true
    },
    resolve: {
        alias: {
            '@': resolve(__dirname, 'src'),
            '@components': resolve(__dirname, 'src/components'),
            '@services': resolve(__dirname, 'src/services'),
            '@utils': resolve(__dirname, 'src/utils'),
            '@data': resolve(__dirname, 'src/data'),
            '@styles': resolve(__dirname, 'src/styles')
        }
    },
    define: {
        'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV)
    }
}); 