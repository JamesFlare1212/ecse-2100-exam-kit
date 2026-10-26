<script lang="ts">
	import { onMount, tick } from 'svelte';
	import './layout.css';
	import favicon from '#lib/assets/favicon.svg';
	import type { LayoutProps } from './$types';

	let { children }: LayoutProps = $props();

	onMount(() => {
		// Child pages restore their locale on mount; reveal after their DOM updates.
		void tick().then(() => delete document.documentElement.dataset.localePending);
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{@render children()}
