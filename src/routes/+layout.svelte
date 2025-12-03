<script lang="ts">
	import '../app.css';
	import { page } from '$app/stores';
	import { base } from '$app/paths';
	
	let { children } = $props();
	
	let mobileMenuOpen = $state(false);
	
	const navLinks = [
		{ href: `${base}/`, label: 'Home' },
		{ href: `${base}/tricks`, label: 'Browse Tricks' },
		{ href: `${base}/difficulty`, label: 'By Difficulty' },
		{ href: `${base}/about`, label: 'About' }
	];
	
	function closeMobileMenu() {
		mobileMenuOpen = false;
	}
</script>

<svelte:head>
	<title>Compendium of Juggling</title>
	<meta name="description" content="A comprehensive database of juggling tricks with animations, tutorials, and difficulty ratings. Learn patterns from basic cascades to advanced ball manipulation.">
	<link rel="icon" href="{base}/favicon.svg" />
</svelte:head>

<a href="#main" class="skip-link">Skip to main content</a>

<header class="header">
	<div class="header-inner container">
		<a href="{base}/" class="logo">
			<span class="logo-icon">🤹</span>
			<span class="logo-text">Compendium of <span class="logo-highlight">Juggling</span></span>
		</a>
		
		<nav class="nav-desktop">
			{#each navLinks as link}
				<a 
					href={link.href} 
					class="nav-link" 
					class:active={$page.url.pathname === link.href || ($page.url.pathname.startsWith(link.href) && link.href !== '/')}
				>
					{link.label}
				</a>
			{/each}
		</nav>
		
		<button 
			class="mobile-menu-btn" 
			onclick={() => mobileMenuOpen = !mobileMenuOpen}
			aria-label="Toggle menu"
			aria-expanded={mobileMenuOpen}
		>
			<span class="hamburger" class:open={mobileMenuOpen}></span>
		</button>
	</div>
</header>

{#if mobileMenuOpen}
	<div class="mobile-nav-overlay" onclick={closeMobileMenu} role="presentation"></div>
	<nav class="mobile-nav">
		{#each navLinks as link}
			<a 
				href={link.href} 
				class="mobile-nav-link" 
				class:active={$page.url.pathname === link.href}
				onclick={closeMobileMenu}
			>
				{link.label}
			</a>
		{/each}
	</nav>
{/if}

<main id="main">
	{@render children()}
</main>

<footer class="footer">
	<div class="container">
		<div class="footer-content">
			<div class="footer-brand">
				<span class="logo-icon">🤹</span>
				<p>The Compendium of Juggling is a comprehensive archive of juggling patterns and tricks for jugglers of all skill levels.</p>
			</div>
			<div class="footer-links">
				<div class="footer-section">
					<h4>Navigation</h4>
					<a href="{base}/">Home</a>
					<a href="{base}/tricks">Browse Tricks</a>
					<a href="{base}/difficulty">By Difficulty</a>
				</div>
				<div class="footer-section">
					<h4>Resources</h4>
					<a href="{base}/about">About</a>
					<a href="http://www.siteswap.org/" target="_blank" rel="noopener">Siteswap Notation</a>
					<a href="https://jugglinglab.org/" target="_blank" rel="noopener">Juggling Lab</a>
				</div>
			</div>
		</div>
		<div class="footer-bottom">
			<p>Originally content from <a href="https://libraryofjuggling.com/" target="_blank" rel="noopener">the Library of Juggling</a>. Modernized with ❤️</p>
		</div>
	</div>
</footer>

<style>
	.header {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		height: var(--header-height);
		background: rgba(15, 15, 18, 0.85);
		backdrop-filter: blur(12px);
		border-bottom: 1px solid rgba(255, 255, 255, 0.05);
		z-index: 100;
	}
	
	.header-inner {
		display: flex;
		align-items: center;
		justify-content: space-between;
		height: 100%;
	}
	
	.logo {
		display: flex;
		align-items: center;
		gap: var(--space-sm);
		font-family: var(--font-display);
		font-size: 1.25rem;
		font-weight: 700;
		color: var(--color-text-primary);
	}
	
	.logo:hover {
		color: var(--color-text-primary);
	}
	
	.logo-icon {
		font-size: 1.5rem;
	}
	
	.logo-highlight {
		background: var(--gradient-primary);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}
	
	.nav-desktop {
		display: flex;
		align-items: center;
		gap: var(--space-xl);
	}
	
	.nav-link {
		font-size: 0.9375rem;
		font-weight: 500;
		color: var(--color-text-secondary);
		transition: color var(--transition-fast);
		position: relative;
	}
	
	.nav-link:hover,
	.nav-link.active {
		color: var(--color-text-primary);
	}
	
	.nav-link.active::after {
		content: '';
		position: absolute;
		bottom: -4px;
		left: 0;
		right: 0;
		height: 2px;
		background: var(--gradient-primary);
		border-radius: var(--radius-full);
	}
	
	.mobile-menu-btn {
		display: none;
		background: none;
		border: none;
		cursor: pointer;
		padding: var(--space-sm);
	}
	
	.hamburger {
		display: block;
		width: 24px;
		height: 2px;
		background: var(--color-text-primary);
		position: relative;
		transition: background var(--transition-fast);
	}
	
	.hamburger::before,
	.hamburger::after {
		content: '';
		position: absolute;
		left: 0;
		width: 100%;
		height: 2px;
		background: var(--color-text-primary);
		transition: transform var(--transition-fast);
	}
	
	.hamburger::before { top: -8px; }
	.hamburger::after { bottom: -8px; }
	
	.hamburger.open {
		background: transparent;
	}
	
	.hamburger.open::before {
		transform: translateY(8px) rotate(45deg);
	}
	
	.hamburger.open::after {
		transform: translateY(-8px) rotate(-45deg);
	}
	
	.mobile-nav-overlay {
		display: none;
		position: fixed;
		inset: 0;
		background: rgba(0, 0, 0, 0.5);
		z-index: 90;
	}
	
	.mobile-nav {
		display: none;
		position: fixed;
		top: var(--header-height);
		left: 0;
		right: 0;
		background: var(--color-bg-secondary);
		border-bottom: 1px solid rgba(255, 255, 255, 0.05);
		padding: var(--space-lg);
		z-index: 95;
		flex-direction: column;
		gap: var(--space-sm);
	}
	
	.mobile-nav-link {
		display: block;
		padding: var(--space-md);
		font-size: 1rem;
		font-weight: 500;
		color: var(--color-text-secondary);
		border-radius: var(--radius-md);
		transition: all var(--transition-fast);
	}
	
	.mobile-nav-link:hover,
	.mobile-nav-link.active {
		background: var(--color-bg-hover);
		color: var(--color-text-primary);
	}
	
	main {
		min-height: calc(100vh - var(--header-height));
		padding-top: var(--header-height);
	}
	
	.footer {
		background: var(--color-bg-secondary);
		border-top: 1px solid rgba(255, 255, 255, 0.05);
		padding: var(--space-3xl) 0 var(--space-xl);
	}
	
	.footer-content {
		display: grid;
		grid-template-columns: 1fr auto;
		gap: var(--space-3xl);
		margin-bottom: var(--space-2xl);
	}
	
	.footer-brand {
		max-width: 320px;
	}
	
	.footer-brand .logo-icon {
		font-size: 2rem;
		display: block;
		margin-bottom: var(--space-md);
	}
	
	.footer-brand p {
		font-size: 0.875rem;
		color: var(--color-text-muted);
	}
	
	.footer-links {
		display: flex;
		gap: var(--space-3xl);
	}
	
	.footer-section h4 {
		font-family: var(--font-body);
		font-size: 0.8125rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		color: var(--color-text-muted);
		margin-bottom: var(--space-md);
	}
	
	.footer-section a {
		display: block;
		font-size: 0.9375rem;
		color: var(--color-text-secondary);
		padding: var(--space-xs) 0;
	}
	
	.footer-section a:hover {
		color: var(--color-text-primary);
	}
	
	.footer-bottom {
		padding-top: var(--space-xl);
		border-top: 1px solid rgba(255, 255, 255, 0.05);
	}
	
	.footer-bottom p {
		font-size: 0.875rem;
		color: var(--color-text-muted);
		text-align: center;
	}
	
	@media (max-width: 768px) {
		.nav-desktop {
			display: none;
		}
		
		.mobile-menu-btn {
			display: block;
		}
		
		.mobile-nav-overlay,
		.mobile-nav {
			display: flex;
		}
		
		.footer-content {
			grid-template-columns: 1fr;
			gap: var(--space-2xl);
		}
		
		.footer-links {
			flex-direction: column;
			gap: var(--space-xl);
		}
	}
</style>
