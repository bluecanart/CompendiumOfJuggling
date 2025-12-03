import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),

	kit: {
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: '404.html',
			precompress: false,
			strict: true
		}),
		// Change this to your repository name if deploying to github.io/repo-name
		// Leave empty if deploying to username.github.io
		paths: {
			base: process.env.NODE_ENV === 'production' ? '/juggling-site' : ''
		},
		prerender: {
			handleHttpError: ({ path, referrer, message }) => {
				// Ignore 404s for external media files (AVI, etc.) referenced in old content
				if (path.endsWith('.AVI') || path.endsWith('.avi')) {
					console.warn(`Ignoring missing AVI file: ${path}`);
					return;
				}
				// Throw on all other errors
				throw new Error(message);
			}
		}
	}
};

export default config;
