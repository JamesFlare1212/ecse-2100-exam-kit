import tailwindcss from '@tailwindcss/vite';
import adapter from '@sveltejs/adapter-static';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	// OneDrive/DrvFS mounts do not reliably forward filesystem events to Vite.
	server: {
		watch: {
			usePolling: true,
			interval: 700,
			ignored: ['**/.git/**', '**/.svelte-kit/**', '**/build/**', '**/static/**', '**/content/**', '**/.agents/**', '**/scripts/**', '**/design-system/**']
		}
	},
	plugins: [
		tailwindcss(),
		sveltekit({
			compilerOptions: {
				// Force runes mode for the project, except for libraries. Can be removed in svelte 6.
				runes: ({ filename }) =>
					filename.split(/[/\\]/).includes('node_modules') ? undefined : true
			},
			adapter: adapter()
		})
	]
});
