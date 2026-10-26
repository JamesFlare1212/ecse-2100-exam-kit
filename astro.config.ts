import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';
import tailwindcss from '@tailwindcss/vite';
import { papersPlugin } from './scripts/papers-plugin';

export default defineConfig({
  output: 'static',
  outDir: './build',
  publicDir: './static',
  trailingSlash: 'always',
  server: { host: '127.0.0.1', port: 5173 },
  integrations: [svelte()],
  vite: {
    plugins: [tailwindcss(), papersPlugin()],
    server: { watch: {
      usePolling: true, interval: 700,
      // Vite must observe staged paper additions/removals to update its public-file cache.
      ignored: ['**/.git/**', '**/.astro/**', '**/build/**', '**/content/**/extracted/**', '**/.agents/**', '**/scripts/**', '**/design-system/**'],
    } },
  },
});
