<script lang="ts">
	import { base } from '$app/paths';
	import tricks from '$lib/data/tricks.json';
	
	// Group tricks by difficulty
	const tricksByDifficulty = $derived.by(() => {
		const grouped: Record<number, typeof tricks> = {};
		
		for (const trick of tricks) {
			if (!grouped[trick.difficulty]) {
				grouped[trick.difficulty] = [];
			}
			grouped[trick.difficulty].push(trick);
		}
		
		// Sort each group alphabetically
		for (const level of Object.keys(grouped)) {
			grouped[parseInt(level)].sort((a, b) => a.name.localeCompare(b.name));
		}
		
		return grouped;
	});
	
	const difficultyLevels = Object.keys(tricksByDifficulty)
		.map(Number)
		.sort((a, b) => a - b);
	
	function getDifficultyLabel(level: number): string {
		if (level <= 2) return 'Beginner';
		if (level <= 4) return 'Intermediate';
		if (level <= 6) return 'Advanced';
		if (level <= 8) return 'Expert';
		return 'Master';
	}
	
	function getDifficultyColor(level: number): string {
		if (level <= 3) return 'green';
		if (level <= 6) return 'yellow';
		if (level <= 8) return 'red';
		return 'purple';
	}
</script>

<svelte:head>
	<title>Tricks by Difficulty | Compendium of Juggling</title>
	<meta name="description" content="Browse juggling tricks organized by difficulty level, from beginner-friendly patterns to expert-level challenges.">
</svelte:head>

<div class="difficulty-page">
	<section class="page-header">
		<div class="container">
			<h1>Tricks by Difficulty</h1>
			<p>Progress through {tricks.length} patterns from beginner to master level</p>
		</div>
	</section>

	<section class="difficulty-content">
		<div class="container">
			<!-- Quick Jump Navigation -->
			<nav class="level-nav">
				{#each difficultyLevels as level}
					<a href="#level-{level}" class="level-nav-item {getDifficultyColor(level)}">
						<span class="level-num">{level}</span>
						<span class="level-count">{tricksByDifficulty[level].length}</span>
					</a>
				{/each}
			</nav>

			<!-- Difficulty Sections -->
			{#each difficultyLevels as level}
				{@const levelTricks = tricksByDifficulty[level]}
				<section id="level-{level}" class="difficulty-section">
					<div class="difficulty-header">
						<div class="difficulty-info">
							<span class="difficulty-badge {getDifficultyColor(level)}">Level {level}</span>
							<h2>{getDifficultyLabel(level)}</h2>
							<p>{levelTricks.length} tricks</p>
						</div>
						<div class="difficulty-bar-large">
							{#each Array(10) as _, i}
								<span 
									class="bar-segment" 
									class:filled={i < level}
									class:green={i < 3}
									class:yellow={i >= 3 && i < 6}
									class:red={i >= 6 && i < 8}
									class:purple={i >= 8}
								></span>
							{/each}
						</div>
					</div>
					
					<div class="tricks-grid">
						{#each levelTricks as trick}
							<a href="{base}/tricks/{trick.slug}" class="trick-item">
								<div class="trick-item-preview">
									<img 
										src="{base}{trick.gifUrl}" 
										alt="{trick.name}" 
										loading="lazy"
									/>
								</div>
								<div class="trick-item-info">
									<span class="trick-item-category">{trick.category}</span>
									<h3 class="trick-item-name">{trick.name}</h3>
									{#if trick.siteswap}
										<span class="trick-item-siteswap">{trick.siteswap}</span>
									{/if}
								</div>
							</a>
						{/each}
					</div>
				</section>
			{/each}
		</div>
	</section>
</div>

<style>
	.page-header {
		padding: var(--space-3xl) 0 var(--space-2xl);
		text-align: center;
		background: linear-gradient(to bottom, var(--color-bg-secondary), var(--color-bg-primary));
	}

	.page-header h1 {
		margin-bottom: var(--space-sm);
	}

	.page-header p {
		color: var(--color-text-muted);
		margin: 0 auto;
	}

	.difficulty-content {
		padding: var(--space-2xl) 0 var(--space-4xl);
	}

	.level-nav {
		display: flex;
		justify-content: center;
		flex-wrap: wrap;
		gap: var(--space-sm);
		margin-bottom: var(--space-3xl);
		padding: var(--space-lg);
		background: var(--color-bg-card);
		border-radius: var(--radius-xl);
		border: 1px solid rgba(255, 255, 255, 0.05);
		position: sticky;
		top: calc(var(--header-height) + var(--space-md));
		z-index: 40;
	}

	.level-nav-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: var(--space-sm) var(--space-md);
		border-radius: var(--radius-md);
		background: var(--color-bg-tertiary);
		transition: all var(--transition-fast);
		min-width: 60px;
	}

	.level-nav-item:hover {
		transform: translateY(-2px);
	}

	.level-nav-item.green:hover {
		background: rgba(77, 255, 136, 0.15);
		color: var(--color-accent-green);
	}

	.level-nav-item.yellow:hover {
		background: rgba(255, 216, 77, 0.15);
		color: var(--color-accent-yellow);
	}

	.level-nav-item.red:hover {
		background: rgba(255, 77, 77, 0.15);
		color: var(--color-accent-red);
	}

	.level-nav-item.purple:hover {
		background: rgba(168, 85, 247, 0.15);
		color: var(--color-accent-purple);
	}

	.level-num {
		font-family: var(--font-display);
		font-size: 1.25rem;
		font-weight: 700;
	}

	.level-count {
		font-size: 0.75rem;
		color: var(--color-text-muted);
	}

	.difficulty-section {
		margin-bottom: var(--space-4xl);
		scroll-margin-top: calc(var(--header-height) + 100px);
	}

	.difficulty-header {
		display: flex;
		justify-content: space-between;
		align-items: flex-end;
		margin-bottom: var(--space-xl);
		padding-bottom: var(--space-lg);
		border-bottom: 1px solid rgba(255, 255, 255, 0.05);
	}

	.difficulty-badge {
		display: inline-block;
		padding: var(--space-xs) var(--space-md);
		border-radius: var(--radius-full);
		font-size: 0.75rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		margin-bottom: var(--space-sm);
	}

	.difficulty-badge.green {
		background: rgba(77, 255, 136, 0.15);
		color: var(--color-accent-green);
	}

	.difficulty-badge.yellow {
		background: rgba(255, 216, 77, 0.15);
		color: var(--color-accent-yellow);
	}

	.difficulty-badge.red {
		background: rgba(255, 77, 77, 0.15);
		color: var(--color-accent-red);
	}

	.difficulty-badge.purple {
		background: rgba(168, 85, 247, 0.15);
		color: var(--color-accent-purple);
	}

	.difficulty-info h2 {
		font-family: var(--font-body);
		font-size: 1.5rem;
		margin-bottom: var(--space-xs);
	}

	.difficulty-info p {
		font-size: 0.875rem;
		color: var(--color-text-muted);
	}

	.difficulty-bar-large {
		display: flex;
		gap: 4px;
	}

	.bar-segment {
		width: 24px;
		height: 12px;
		background: rgba(255, 255, 255, 0.1);
		border-radius: 3px;
	}

	.bar-segment.filled.green {
		background: var(--color-accent-green);
	}

	.bar-segment.filled.yellow {
		background: var(--color-accent-yellow);
	}

	.bar-segment.filled.red {
		background: var(--color-accent-red);
	}

	.bar-segment.filled.purple {
		background: var(--color-accent-purple);
	}

	.tricks-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
		gap: var(--space-md);
	}

	.trick-item {
		display: flex;
		gap: var(--space-md);
		padding: var(--space-md);
		background: var(--color-bg-card);
		border-radius: var(--radius-lg);
		border: 1px solid rgba(255, 255, 255, 0.05);
		transition: all var(--transition-normal);
	}

	.trick-item:hover {
		border-color: rgba(255, 255, 255, 0.1);
		background: var(--color-bg-hover);
		transform: translateY(-2px);
	}

	.trick-item-preview {
		width: 64px;
		height: 64px;
		flex-shrink: 0;
		background: var(--color-bg-tertiary);
		border-radius: var(--radius-md);
		overflow: hidden;
	}

	.trick-item-preview img {
		width: 100%;
		height: 100%;
		object-fit: contain;
	}

	.trick-item-info {
		flex: 1;
		min-width: 0;
		display: flex;
		flex-direction: column;
		justify-content: center;
	}

	.trick-item-category {
		font-size: 0.6875rem;
		color: var(--color-accent-blue);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		margin-bottom: var(--space-xs);
	}

	.trick-item-name {
		font-family: var(--font-body);
		font-size: 0.9375rem;
		font-weight: 600;
		line-height: 1.3;
		margin-bottom: var(--space-xs);
	}

	.trick-item-siteswap {
		font-size: 0.75rem;
		font-family: 'Courier New', monospace;
		color: var(--color-text-muted);
	}

	@media (max-width: 768px) {
		.level-nav {
			position: static;
			gap: var(--space-xs);
			padding: var(--space-md);
		}

		.level-nav-item {
			padding: var(--space-xs) var(--space-sm);
			min-width: 50px;
		}

		.level-num {
			font-size: 1rem;
		}

		.difficulty-header {
			flex-direction: column;
			align-items: flex-start;
			gap: var(--space-md);
		}

		.tricks-grid {
			grid-template-columns: 1fr;
		}
	}
</style>

