<script lang="ts">
	import { page } from '$app/stores';
	import { base } from '$app/paths';
	import tricks from '$lib/data/tricks.json';
	import GifPlayer from '$lib/components/GifPlayer.svelte';
	
	// Make slug and trick reactive so they update on navigation
	let slug = $derived($page.params.slug);
	let trick = $derived(tricks.find(t => t.slug === slug));
	
	// Find more tricks - prioritize prerequisites/related, then same family, then same category
	let relatedTricks = $derived.by(() => {
		if (!trick) return [];
		
		const priorityTricks: typeof tricks = [];
		const familyTricks: typeof tricks = [];
		const categoryTricks: typeof tricks = [];
		
		for (const t of tricks) {
			if (t.slug === slug) continue;
			
			// Priority 1: prerequisite or explicitly related (exact name match only)
			const isPrereq = trick.prerequisites?.some(p => 
				t.name.toLowerCase() === p.toLowerCase()
			);
			const isRelated = trick.relatedTricks?.some(r =>
				t.name.toLowerCase() === r.toLowerCase()
			);
			
			if (isPrereq || isRelated) {
				priorityTricks.push(t);
			} else if (trick.trickFamily && t.trickFamily === trick.trickFamily) {
				// Priority 2: same family
				familyTricks.push(t);
			} else if (t.category === trick.category) {
				// Priority 3: same category
				categoryTricks.push(t);
			}
		}
		
		// Return priority tricks first, then family, then category
		return [...priorityTricks, ...familyTricks, ...categoryTricks].slice(0, 6);
	});
	
	// Find prerequisite tricks (with links)
	let prereqTricks = $derived.by(() => {
		if (!trick?.prerequisites) return [];
		return trick.prerequisites.map(prereqName => {
			const found = tricks.find(t => 
				t.name.toLowerCase() === prereqName.toLowerCase() ||
				t.name.toLowerCase().includes(prereqName.toLowerCase())
			);
			return {
				name: prereqName,
				slug: found?.slug || null
			};
		});
	});
</script>

<svelte:head>
	{#if trick}
		<title>{trick.name} | Compendium of Juggling</title>
		<meta name="description" content="{trick.name} - A {trick.category.toLowerCase()} juggling pattern. Difficulty: {trick.difficulty}/10. {trick.siteswap ? `Siteswap: ${trick.siteswap}` : ''}">
	{:else}
		<title>Trick Not Found | Compendium of Juggling</title>
	{/if}
</svelte:head>

{#if trick}
	<article class="trick-detail">
		<!-- Breadcrumb -->
		<nav class="breadcrumb">
			<div class="container">
				<a href="{base}/tricks">← All Tricks</a>
				<span class="separator">/</span>
				<a href="{base}/tricks?category={encodeURIComponent(trick.category)}">{trick.category}</a>
				<span class="separator">/</span>
				<span class="current">{trick.name}</span>
			</div>
		</nav>

		<!-- Hero Section -->
		<section class="trick-hero">
			<div class="container">
				<div class="trick-hero-grid">
					<div class="trick-animation">
						<div class="animation-container">
							<GifPlayer src="{base}{trick.gifUrl}" alt="{trick.name} animation" />
						</div>
					</div>
					
					<div class="trick-info">
						<div class="trick-badges">
							<span class="badge badge-category">{trick.category}</span>
							<span class="badge badge-difficulty" data-level={trick.difficulty}>
								Level {trick.difficulty}
							</span>
							{#if trick.trickFamily}
								<span class="badge badge-family">{trick.trickFamily}</span>
							{/if}
							{#if trick.librarianLearned}
								<span class="badge badge-learned" title="Librarian's Pick">C</span>
							{/if}
						</div>
						
						{#if trick.tags && trick.tags.length > 0}
							<div class="trick-tags">
								{#each trick.tags as tag}
									<span class="badge badge-tag">{tag}</span>
								{/each}
							</div>
						{/if}
						
						<h1 class="trick-name">{trick.name}</h1>
						
						<div class="trick-meta">
							{#if trick.siteswap}
								<div class="meta-item">
									<span class="meta-label">Siteswap</span>
									<span class="meta-value siteswap">{trick.siteswap}</span>
								</div>
							{/if}
							
							<div class="meta-item">
								<span class="meta-label">Difficulty</span>
								<div class="difficulty-bar">
									{#each Array(10) as _, i}
										<span 
											class="difficulty-segment" 
											class:filled={i < trick.difficulty}
											class:green={i < 3}
											class:yellow={i >= 3 && i < 6}
											class:red={i >= 6 && i < 8}
											class:purple={i >= 8}
										></span>
									{/each}
								</div>
								<span class="meta-value">{trick.difficulty}/10</span>
							</div>
							
							<div class="meta-item">
								<span class="meta-label">Ball Count</span>
								<span class="meta-value">{trick.numBalls} balls</span>
							</div>
						</div>
						
						{#if prereqTricks.length > 0}
							<div class="prerequisites">
								<h3>Prerequisites</h3>
								<div class="prereq-list">
									{#each prereqTricks as prereq}
										{#if prereq.slug}
											<a href="{base}/tricks/{prereq.slug}" class="prereq-link">
												{prereq.name}
											</a>
										{:else}
											<span class="prereq-text">{prereq.name}</span>
										{/if}
									{/each}
								</div>
							</div>
						{/if}
						
						{#if trick.relatedTricks && trick.relatedTricks.length > 0}
							<div class="related-inline">
								<span class="related-label">Related:</span>
								{#each trick.relatedTricks as related, i}
									{@const relatedTrick = tricks.find(t => t.name === related)}
									{#if relatedTrick}
										<a href="{base}/tricks/{relatedTrick.slug}">{related}</a>
									{:else}
										<span>{related}</span>
									{/if}
									{#if i < trick.relatedTricks.length - 1}
										<span class="comma">,</span>
									{/if}
								{/each}
							</div>
						{/if}
					</div>
				</div>
			</div>
		</section>

		<!-- Tutorial Section -->
		{#if trick.tutorialContent && trick.tutorialContent.length > 0}
			<section class="tutorial-section section">
				<div class="container">
					<div class="tutorial-content">
						<h2>How to Learn</h2>
						<div class="tutorial-items">
							{#each trick.tutorialContent as item}
								{#if item.type === 'text'}
									<p class="tutorial-text">{item.content}</p>
								{:else if item.type === 'gif'}
									<div class="tutorial-gif">
										<img 
											src="{base}{item.url}" 
											alt="Tutorial animation" 
											loading="lazy"
										/>
									</div>
								{/if}
							{/each}
						</div>
					</div>
				</div>
			</section>
		{:else if trick.description}
			<!-- Fallback to plain description if no tutorial content -->
			<section class="trick-description section">
				<div class="container">
					<div class="description-content">
						<h2>How to Learn</h2>
						<div class="description-text">
							{trick.description}
						</div>
					</div>
				</div>
			</section>
		{/if}

		<!-- Tutorials Section -->
		{#if trick.tutorialLinks && trick.tutorialLinks.length > 0}
			<section class="tutorials-section">
				<div class="container">
					<h2>External Tutorials</h2>
					<div class="tutorials-grid">
						{#each trick.tutorialLinks as tutorial}
							<a 
								href={tutorial.url} 
								class="tutorial-card card"
								target="_blank"
								rel="noopener noreferrer"
							>
								<div class="tutorial-icon">
									{#if tutorial.url.includes('youtube')}
										<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
											<path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/>
										</svg>
									{:else}
										<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
											<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
											<polyline points="15 3 21 3 21 9"></polyline>
											<line x1="10" y1="14" x2="21" y2="3"></line>
										</svg>
									{/if}
								</div>
								<div class="tutorial-info">
									<span class="tutorial-title">{tutorial.title}</span>
									<span class="tutorial-type">
										{tutorial.url.includes('youtube') ? 'Video Tutorial' : 'External Link'}
									</span>
								</div>
								<svg class="tutorial-arrow" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
									<line x1="5" y1="12" x2="19" y2="12"></line>
									<polyline points="12 5 19 12 12 19"></polyline>
								</svg>
							</a>
						{/each}
					</div>
				</div>
			</section>
		{/if}

		<!-- More Tricks Section -->
		{#if relatedTricks.length > 0}
			<section class="related-section section">
				<div class="container">
					<h2>More Tricks</h2>
					<div class="related-grid">
						{#each relatedTricks as relatedTrick}
							<a href="{base}/tricks/{relatedTrick.slug}" class="related-card card">
								<div class="related-card-image">
									<img 
										src="{base}{relatedTrick.gifUrl}" 
										alt="{relatedTrick.name} animation" 
										loading="lazy"
									/>
								</div>
								<div class="related-card-content">
									<span class="badge badge-difficulty" data-level={relatedTrick.difficulty}>
										Level {relatedTrick.difficulty}
									</span>
									<h4>{relatedTrick.name}</h4>
								</div>
							</a>
						{/each}
					</div>
				</div>
			</section>
		{/if}
	</article>
{:else}
	<div class="not-found">
		<div class="container">
			<h1>Trick Not Found</h1>
			<p>The trick you're looking for doesn't exist in our database.</p>
			<a href="{base}/tricks" class="btn btn-primary">Browse All Tricks</a>
		</div>
	</div>
{/if}

<style>
	.breadcrumb {
		padding: var(--space-lg) 0;
		font-size: 0.875rem;
		color: var(--color-text-muted);
	}

	.breadcrumb a {
		color: var(--color-text-secondary);
	}

	.breadcrumb a:hover {
		color: var(--color-accent-yellow);
	}

	.breadcrumb .separator {
		margin: 0 var(--space-sm);
		opacity: 0.5;
	}

	.breadcrumb .current {
		color: var(--color-text-primary);
	}

	.trick-hero {
		padding-bottom: var(--space-3xl);
		background: linear-gradient(to bottom, var(--color-bg-secondary), var(--color-bg-primary));
	}

	.trick-hero-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--space-3xl);
		align-items: start;
	}

	.trick-animation {
		position: sticky;
		top: calc(var(--header-height) + var(--space-xl));
	}

	.animation-container {
		background: var(--color-bg-card);
		border-radius: var(--radius-xl);
		border: 1px solid rgba(255, 255, 255, 0.05);
		padding: var(--space-md);
		overflow: hidden;
	}

	.trick-badges {
		display: flex;
		gap: var(--space-sm);
		margin-bottom: var(--space-md);
		flex-wrap: wrap;
	}

	.trick-tags {
		display: flex;
		gap: var(--space-xs);
		margin-bottom: var(--space-lg);
		flex-wrap: wrap;
	}

	.trick-name {
		font-size: clamp(2rem, 5vw, 3rem);
		margin-bottom: var(--space-xl);
	}

	.trick-meta {
		display: flex;
		flex-direction: column;
		gap: var(--space-lg);
		margin-bottom: var(--space-xl);
		padding: var(--space-lg);
		background: var(--color-bg-card);
		border-radius: var(--radius-lg);
		border: 1px solid rgba(255, 255, 255, 0.05);
	}

	.meta-item {
		display: flex;
		align-items: center;
		gap: var(--space-md);
	}

	.meta-label {
		font-size: 0.875rem;
		color: var(--color-text-muted);
		min-width: 80px;
	}

	.meta-value {
		font-weight: 600;
	}

	.meta-value.siteswap {
		font-family: 'Courier New', monospace;
		font-size: 1.25rem;
		color: var(--color-accent-yellow);
	}

	.difficulty-bar {
		display: flex;
		gap: 3px;
		margin-right: var(--space-md);
	}

	.difficulty-segment {
		width: 16px;
		height: 8px;
		background: rgba(255, 255, 255, 0.1);
		border-radius: 2px;
	}

	.difficulty-segment.filled.green {
		background: var(--color-accent-green);
	}

	.difficulty-segment.filled.yellow {
		background: var(--color-accent-yellow);
	}

	.difficulty-segment.filled.red {
		background: var(--color-accent-red);
	}

	.difficulty-segment.filled.purple {
		background: var(--color-accent-purple);
	}

	.prerequisites h3 {
		font-family: var(--font-body);
		font-size: 0.875rem;
		font-weight: 600;
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		margin-bottom: var(--space-sm);
	}

	.prereq-list {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-sm);
	}

	.prereq-link,
	.prereq-text {
		display: inline-block;
		padding: var(--space-xs) var(--space-md);
		background: var(--color-bg-tertiary);
		border-radius: var(--radius-full);
		font-size: 0.875rem;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.prereq-link:hover {
		background: var(--color-bg-hover);
		border-color: var(--color-accent-yellow);
		color: var(--color-accent-yellow);
	}

	.related-inline {
		margin-top: var(--space-lg);
		font-size: 0.875rem;
		color: var(--color-text-secondary);
	}

	.related-label {
		color: var(--color-text-muted);
		margin-right: var(--space-sm);
	}

	.related-inline a {
		color: var(--color-accent-blue);
	}

	.related-inline a:hover {
		text-decoration: underline;
	}

	.related-inline .comma {
		margin-right: var(--space-xs);
	}

	/* Tutorial Section */
	.tutorial-section {
		background: var(--color-bg-secondary);
	}

	.tutorial-content {
		max-width: 800px;
		margin: 0 auto;
	}

	.tutorial-content h2 {
		margin-bottom: var(--space-xl);
	}

	.tutorial-items {
		display: flex;
		flex-direction: column;
		gap: var(--space-lg);
	}

	.tutorial-text {
		font-size: 1.0625rem;
		line-height: 1.8;
		color: var(--color-text-secondary);
		max-width: none;
	}

	.tutorial-gif {
		display: flex;
		justify-content: center;
		margin: var(--space-md) 0;
	}

	.tutorial-gif img {
		max-width: 200px;
		height: auto;
		background: var(--color-bg-card);
		border-radius: var(--radius-lg);
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	/* Plain description fallback */
	.trick-description {
		background: var(--color-bg-secondary);
	}

	.description-content {
		max-width: 800px;
		margin: 0 auto;
	}

	.description-content h2 {
		margin-bottom: var(--space-xl);
	}

	.description-text {
		font-size: 1.0625rem;
		line-height: 1.8;
		color: var(--color-text-secondary);
	}

	.tutorials-section {
		padding: var(--space-3xl) 0;
	}

	.tutorials-section h2 {
		margin-bottom: var(--space-xl);
	}

	.tutorials-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
		gap: var(--space-md);
	}

	.tutorial-card {
		display: flex;
		align-items: center;
		gap: var(--space-md);
		padding: var(--space-lg);
	}

	.tutorial-icon {
		width: 48px;
		height: 48px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: rgba(255, 77, 77, 0.1);
		border-radius: var(--radius-md);
		color: var(--color-accent-red);
		flex-shrink: 0;
	}

	.tutorial-info {
		flex: 1;
		min-width: 0;
	}

	.tutorial-title {
		display: block;
		font-weight: 600;
		margin-bottom: var(--space-xs);
	}

	.tutorial-type {
		font-size: 0.8125rem;
		color: var(--color-text-muted);
	}

	.tutorial-arrow {
		color: var(--color-text-muted);
		transition: transform var(--transition-fast);
	}

	.tutorial-card:hover .tutorial-arrow {
		transform: translateX(4px);
	}

	.related-section {
		background: var(--color-bg-secondary);
	}

	.related-section h2 {
		margin-bottom: var(--space-xl);
	}

	.related-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
		gap: var(--space-md);
	}

	.related-card {
		display: block;
	}

	.related-card-image {
		aspect-ratio: 1;
		background: var(--color-bg-tertiary);
		overflow: hidden;
	}

	.related-card-image img {
		width: 100%;
		height: 100%;
		object-fit: contain;
		transition: transform var(--transition-slow);
	}

	.related-card:hover .related-card-image img {
		transform: scale(1.05);
	}

	.related-card-content {
		padding: var(--space-md);
	}

	.related-card-content h4 {
		font-family: var(--font-body);
		font-size: 0.9375rem;
		font-weight: 600;
		margin-top: var(--space-sm);
	}

	.not-found {
		padding: var(--space-4xl) 0;
		text-align: center;
	}

	.not-found h1 {
		margin-bottom: var(--space-md);
	}

	.not-found p {
		color: var(--color-text-muted);
		margin: 0 auto var(--space-xl);
	}

	@media (max-width: 900px) {
		.trick-hero-grid {
			grid-template-columns: 1fr;
			gap: var(--space-xl);
		}

		.trick-animation {
			position: static;
		}

		.animation-container {
			max-width: 400px;
			margin: 0 auto;
		}
	}

	@media (max-width: 768px) {
		.tutorial-gif img {
			max-width: 160px;
		}
	}

	@media (max-width: 600px) {
		.meta-item {
			flex-direction: column;
			align-items: flex-start;
			gap: var(--space-xs);
		}

		.difficulty-bar {
			margin-right: 0;
		}

		.tutorials-grid {
			grid-template-columns: 1fr;
		}

		.related-grid {
			grid-template-columns: repeat(2, 1fr);
		}
	}
</style>

