import tailwindcss from '@tailwindcss/vite';
import adapter from '@sveltejs/adapter-static';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { papersPlugin } from './scripts/papers-plugin.ts';

export default defineConfig({
	// OneDrive/DrvFS mounts do not reliably forward filesystem events to Vite.
	server: {
		watch: {
			usePolling: true,
			interval: 700,
			ignored: ['**/.git/**', '**/.svelte-kit/**', '**/build/**', '**/static/**', '**/content/**/extracted/**', '**/.agents/**', '**/scripts/**', '**/design-system/**']
		}
	},
	plugins: [
		papersPlugin(),
		tailwindcss(),
		sveltekit({
			compilerOptions: {
				// Force runes mode for the project, except for libraries. Can be removed in svelte 6.
				runes: ({ filename }) =>
					filename.split(/[/\\]/).includes('node_modules') ? undefined : true
			},
			adapter: adapter({ fallback: '404.html' })
		})
	]
});
