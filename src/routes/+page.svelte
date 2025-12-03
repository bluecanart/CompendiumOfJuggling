<script lang="ts">
	import { base } from '$app/paths';
	import tricks from '$lib/data/tricks.json';
	
	const totalTricks = tricks.length;
	const categories = [...new Set(tricks.map(t => t.category))];
	const maxDifficulty = Math.max(...tricks.map(t => t.difficulty));
	
	// Get featured tricks (popular, varied difficulty)
	const featuredTricks = [
		tricks.find(t => t.slug === 'cascade'),
		tricks.find(t => t.slug === 'millsmess'),
		tricks.find(t => t.slug === 'box'),
		tricks.find(t => t.slug === 'fountain'),
		tricks.find(t => t.slug === 'five-ball-cascade') || tricks.find(t => t.slug === 'fiveballcascade'),
		tricks.find(t => t.slug === 'shower')
	].filter(Boolean).slice(0, 6);
	
	// Get beginner tricks
	const beginnerTricks = tricks.filter(t => t.difficulty <= 3).slice(0, 4);
</script>

<div class="home">
	<!-- Hero Section -->
	<section class="hero">
		<div class="hero-bg">
			<div class="hero-orb hero-orb-1"></div>
			<div class="hero-orb hero-orb-2"></div>
			<div class="hero-orb hero-orb-3"></div>
		</div>
		<div class="container hero-content">
			<div class="hero-badge">
				<span class="badge-dot"></span>
				<span>{totalTricks} Tricks & Growing</span>
			</div>
			<h1 class="hero-title">
				The Ultimate<br />
				<span class="gradient-text">Juggling</span> Database
			</h1>
			<p class="hero-description">
				Discover, learn, and master juggling patterns from basic cascades to advanced 
				manipulation. Animated tutorials, difficulty ratings, and siteswap notation 
				for every trick.
			</p>
			<div class="hero-actions">
				<a href="{base}/tricks" class="btn btn-primary">
					<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						<circle cx="11" cy="11" r="8"></circle>
						<path d="m21 21-4.35-4.35"></path>
					</svg>
					Browse All Tricks
				</a>
				<a href="{base}/difficulty" class="btn btn-secondary">
					By Difficulty
				</a>
			</div>
			<div class="hero-stats">
				<div class="stat">
					<span class="stat-value">{totalTricks}</span>
					<span class="stat-label">Tricks</span>
				</div>
				<div class="stat-divider"></div>
				<div class="stat">
					<span class="stat-value">{categories.length}</span>
					<span class="stat-label">Categories</span>
				</div>
				<div class="stat-divider"></div>
				<div class="stat">
					<span class="stat-value">3-6</span>
					<span class="stat-label">Ball Patterns</span>
				</div>
			</div>
		</div>
	</section>

	<!-- Featured Tricks Section -->
	<section class="section featured-section">
		<div class="container">
			<div class="section-header">
				<h2>Featured Patterns</h2>
				<p>Iconic juggling tricks every juggler should know</p>
			</div>
			<div class="tricks-grid">
				{#each featuredTricks as trick}
					{#if trick}
						<a href="{base}/tricks/{trick.slug}" class="trick-card card">
							<div class="trick-card-image">
								<img 
									src="{base}{trick.gifUrl}" 
									alt="{trick.name} animation" 
									loading="lazy"
								/>
							</div>
							<div class="trick-card-content">
								<div class="trick-card-badges">
									<span class="badge badge-category">{trick.category}</span>
									<span class="badge badge-difficulty" data-level={trick.difficulty}>
										Level {trick.difficulty}
									</span>
								</div>
								<h3 class="trick-card-title">{trick.name}</h3>
								{#if trick.siteswap}
									<p class="trick-card-siteswap">Siteswap: {trick.siteswap}</p>
								{/if}
							</div>
						</a>
					{/if}
				{/each}
			</div>
			<div class="section-footer">
				<a href="{base}/tricks" class="btn btn-secondary">View All {totalTricks} Tricks →</a>
			</div>
		</div>
	</section>

	<!-- Start Learning Section -->
	<section class="section learning-section">
		<div class="container">
			<div class="learning-grid">
				<div class="learning-content">
					<h2>New to Juggling?</h2>
					<p>
						Start your juggling journey with these beginner-friendly patterns. 
						Each trick includes animated demonstrations and step-by-step tutorials 
						to help you progress from zero to juggler.
					</p>
					<ul class="learning-features">
						<li>
							<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
								<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
								<polyline points="22 4 12 14.01 9 11.01"></polyline>
							</svg>
							Animated GIF demonstrations
						</li>
						<li>
							<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
								<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
								<polyline points="22 4 12 14.01 9 11.01"></polyline>
							</svg>
							Difficulty ratings (1-10)
						</li>
						<li>
							<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
								<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
								<polyline points="22 4 12 14.01 9 11.01"></polyline>
							</svg>
							Prerequisite trick guidance
						</li>
						<li>
							<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
								<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
								<polyline points="22 4 12 14.01 9 11.01"></polyline>
							</svg>
							Siteswap notation
						</li>
					</ul>
					<a href="{base}/tricks/cascade" class="btn btn-primary">
						Start with the Cascade
					</a>
				</div>
				<div class="beginner-tricks">
					{#each beginnerTricks as trick}
						<a href="{base}/tricks/{trick.slug}" class="beginner-trick-card">
							<div class="beginner-trick-preview">
								<img src="{base}{trick.gifUrl}" alt={trick.name} loading="lazy" />
							</div>
							<div class="beginner-trick-info">
								<h4>{trick.name}</h4>
								<span class="badge badge-difficulty" data-level={trick.difficulty}>
									Level {trick.difficulty}
								</span>
							</div>
						</a>
					{/each}
				</div>
			</div>
		</div>
	</section>

	<!-- Categories Section -->
	<section class="section categories-section">
		<div class="container">
			<div class="section-header">
				<h2>Browse by Ball Count</h2>
				<p>Find tricks organized by the number of props</p>
			</div>
			<div class="categories-grid">
				{#each categories as category}
					{@const count = tricks.filter(t => t.category === category).length}
					{@const numBalls = parseInt(category)}
					<a href="{base}/tricks?category={encodeURIComponent(category)}" class="category-card card">
						<div class="category-balls">
							{#each Array(numBalls) as _, i}
								<span class="ball" style="--delay: {i * 0.1}s"></span>
							{/each}
						</div>
						<h3>{category} Patterns</h3>
						<p>{count} tricks</p>
					</a>
				{/each}
			</div>
		</div>
	</section>

	<!-- About Section -->
	<section class="section about-section">
		<div class="container">
			<div class="about-card card">
				<div class="about-content">
					<h2>What is the Compendium of Juggling?</h2>
					<p>
						The Compendium of Juggling is a comprehensive archive of juggling patterns, 
						originally created to preserve and share the art of toss juggling. Despite 
						the growing popularity of juggling, few resources are dedicated to collecting 
						and cataloging the various patterns being performed around the world.
					</p>
					<p>
						From iconic tricks like the <a href="{base}/tricks/cascade">Cascade</a> and 
						<a href="{base}/tricks/shower">Shower</a> to advanced patterns like 
						<a href="{base}/tricks/rubenstein's-revenge" >Rubenstein's Revenge</a>, 
						our goal is to ensure that juggling knowledge is preserved and accessible 
						to jugglers everywhere.
					</p>
					<a href="{base}/about" class="btn btn-ghost">Learn More →</a>
				</div>
			</div>
		</div>
	</section>
</div>

<style>
	.home {
		overflow-x: hidden;
	}

	/* Hero Section */
	.hero {
		position: relative;
		min-height: calc(100vh - var(--header-height));
		display: flex;
		align-items: center;
		padding: var(--space-4xl) 0;
	}

	.hero-bg {
		position: absolute;
		inset: 0;
		overflow: hidden;
		pointer-events: none;
	}

	.hero-orb {
		position: absolute;
		border-radius: 50%;
		filter: blur(80px);
		opacity: 0.5;
	}

	.hero-orb-1 {
		width: 400px;
		height: 400px;
		background: var(--color-accent-red);
		top: 10%;
		right: 10%;
		animation: float 8s ease-in-out infinite;
	}

	.hero-orb-2 {
		width: 300px;
		height: 300px;
		background: var(--color-accent-blue);
		bottom: 20%;
		left: 5%;
		animation: float 10s ease-in-out infinite;
		animation-delay: -2s;
	}

	.hero-orb-3 {
		width: 250px;
		height: 250px;
		background: var(--color-accent-yellow);
		top: 40%;
		left: 30%;
		animation: float 12s ease-in-out infinite;
		animation-delay: -4s;
	}

	.hero-content {
		position: relative;
		text-align: center;
		max-width: 800px;
		margin: 0 auto;
	}

	.hero-badge {
		display: inline-flex;
		align-items: center;
		gap: var(--space-sm);
		padding: var(--space-sm) var(--space-md);
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: var(--radius-full);
		font-size: 0.875rem;
		color: var(--color-text-secondary);
		margin-bottom: var(--space-xl);
	}

	.badge-dot {
		width: 8px;
		height: 8px;
		background: var(--color-accent-green);
		border-radius: 50%;
		animation: pulse-glow 2s ease-in-out infinite;
	}

	.hero-title {
		font-size: clamp(3rem, 8vw, 5rem);
		margin-bottom: var(--space-lg);
		line-height: 1.1;
	}

	.gradient-text {
		background: var(--gradient-primary);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}

	.hero-description {
		font-size: 1.25rem;
		color: var(--color-text-secondary);
		max-width: 600px;
		margin: 0 auto var(--space-2xl);
	}

	.hero-actions {
		display: flex;
		gap: var(--space-md);
		justify-content: center;
		flex-wrap: wrap;
		margin-bottom: var(--space-3xl);
	}

	.hero-stats {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: var(--space-xl);
	}

	.stat {
		text-align: center;
	}

	.stat-value {
		display: block;
		font-family: var(--font-display);
		font-size: 2rem;
		font-weight: 700;
		color: var(--color-text-primary);
	}

	.stat-label {
		font-size: 0.875rem;
		color: var(--color-text-muted);
	}

	.stat-divider {
		width: 1px;
		height: 40px;
		background: rgba(255, 255, 255, 0.1);
	}

	/* Section Headers */
	.section-header {
		text-align: center;
		margin-bottom: var(--space-3xl);
	}

	.section-header h2 {
		margin-bottom: var(--space-sm);
	}

	.section-header p {
		color: var(--color-text-muted);
		margin: 0 auto;
	}

	.section-footer {
		text-align: center;
		margin-top: var(--space-2xl);
	}

	/* Tricks Grid */
	.tricks-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
		gap: var(--space-lg);
	}

	.trick-card {
		display: block;
	}

	.trick-card-image {
		aspect-ratio: 1;
		background: var(--color-bg-tertiary);
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
	}

	.trick-card-image img {
		width: 100%;
		height: 100%;
		object-fit: contain;
		transition: transform var(--transition-slow);
	}

	.trick-card:hover .trick-card-image img {
		transform: scale(1.05);
	}

	.trick-card-content {
		padding: var(--space-lg);
	}

	.trick-card-badges {
		display: flex;
		gap: var(--space-sm);
		margin-bottom: var(--space-sm);
	}

	.trick-card-title {
		font-family: var(--font-body);
		font-size: 1.125rem;
		font-weight: 600;
		margin-bottom: var(--space-xs);
	}

	.trick-card-siteswap {
		font-size: 0.875rem;
		color: var(--color-text-muted);
		font-family: 'Courier New', monospace;
	}

	/* Learning Section */
	.learning-section {
		background: var(--color-bg-secondary);
	}

	.learning-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--space-3xl);
		align-items: center;
	}

	.learning-content h2 {
		margin-bottom: var(--space-md);
	}

	.learning-content p {
		margin-bottom: var(--space-xl);
	}

	.learning-features {
		list-style: none;
		margin-bottom: var(--space-xl);
	}

	.learning-features li {
		display: flex;
		align-items: center;
		gap: var(--space-md);
		padding: var(--space-sm) 0;
		color: var(--color-text-secondary);
	}

	.learning-features svg {
		color: var(--color-accent-green);
		flex-shrink: 0;
	}

	.beginner-tricks {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: var(--space-md);
	}

	.beginner-trick-card {
		display: flex;
		flex-direction: column;
		background: var(--color-bg-card);
		border-radius: var(--radius-lg);
		overflow: hidden;
		border: 1px solid rgba(255, 255, 255, 0.05);
		transition: all var(--transition-normal);
	}

	.beginner-trick-card:hover {
		border-color: rgba(255, 255, 255, 0.1);
		transform: translateY(-2px);
	}

	.beginner-trick-preview {
		aspect-ratio: 1;
		background: var(--color-bg-tertiary);
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.beginner-trick-preview img {
		width: 100%;
		height: 100%;
		object-fit: contain;
	}

	.beginner-trick-info {
		padding: var(--space-md);
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.beginner-trick-info h4 {
		font-family: var(--font-body);
		font-size: 0.9375rem;
		font-weight: 600;
	}

	/* Categories Section */
	.categories-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: var(--space-lg);
	}

	.category-card {
		padding: var(--space-xl);
		text-align: center;
	}

	.category-balls {
		display: flex;
		justify-content: center;
		gap: var(--space-sm);
		margin-bottom: var(--space-lg);
	}

	.ball {
		width: 24px;
		height: 24px;
		border-radius: 50%;
		background: var(--gradient-primary);
		animation: float 3s ease-in-out infinite;
		animation-delay: var(--delay);
	}

	.category-card h3 {
		font-family: var(--font-body);
		font-size: 1.125rem;
		font-weight: 600;
		margin-bottom: var(--space-xs);
	}

	.category-card p {
		font-size: 0.875rem;
		color: var(--color-text-muted);
	}

	/* About Section */
	.about-card {
		padding: var(--space-3xl);
		background: linear-gradient(135deg, var(--color-bg-card) 0%, var(--color-bg-tertiary) 100%);
	}

	.about-content {
		max-width: 700px;
		margin: 0 auto;
		text-align: center;
	}

	.about-content h2 {
		margin-bottom: var(--space-lg);
	}

	.about-content p {
		margin: 0 auto var(--space-lg);
	}

	.about-content a:not(.btn) {
		color: var(--color-accent-yellow);
		text-decoration: underline;
	}

	/* Responsive */
	@media (max-width: 768px) {
		.hero {
			min-height: auto;
			padding: var(--space-3xl) 0;
		}

		.hero-orb {
			opacity: 0.3;
		}

		.hero-stats {
			flex-wrap: wrap;
			gap: var(--space-lg);
		}

		.stat-divider {
			display: none;
		}

		.learning-grid {
			grid-template-columns: 1fr;
			gap: var(--space-2xl);
		}

		.beginner-tricks {
			grid-template-columns: repeat(2, 1fr);
		}

		.about-card {
			padding: var(--space-xl);
		}
	}
</style>
