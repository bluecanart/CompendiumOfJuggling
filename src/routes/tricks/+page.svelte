<script lang="ts">
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';
	import { base } from '$app/paths';
	import tricks from '$lib/data/tricks.json';
	
	// Get URL params (only in browser, not during prerendering)
	let searchQuery = $state('');
	let selectedCategory = $state('');
	let selectedDifficulty = $state('');
	let sortBy = $state('name');
	
	// Initialize from URL params in browser
	$effect(() => {
		if (browser) {
			searchQuery = $page.url.searchParams.get('q') || '';
			selectedCategory = $page.url.searchParams.get('category') || '';
			selectedDifficulty = $page.url.searchParams.get('difficulty') || '';
			sortBy = $page.url.searchParams.get('sort') || 'name';
		}
	});
	
	// Get unique categories and difficulties
	const categories = [...new Set(tricks.map(t => t.category))].sort((a, b) => {
		const numA = parseInt(a);
		const numB = parseInt(b);
		return numA - numB;
	});
	
	const difficulties = [...new Set(tricks.map(t => t.difficulty))].sort((a, b) => a - b);
	
	// Filter and sort tricks
	let filteredTricks = $derived.by(() => {
		let result = [...tricks];
		
		// Filter by search query
		if (searchQuery) {
			const query = searchQuery.toLowerCase();
			result = result.filter(t => 
				t.name.toLowerCase().includes(query) ||
				t.siteswap?.toLowerCase().includes(query) ||
				t.description?.toLowerCase().includes(query)
			);
		}
		
		// Filter by category
		if (selectedCategory) {
			result = result.filter(t => t.category === selectedCategory);
		}
		
		// Filter by difficulty
		if (selectedDifficulty) {
			result = result.filter(t => t.difficulty === parseInt(selectedDifficulty));
		}
		
		// Sort
		switch (sortBy) {
			case 'name':
				result.sort((a, b) => a.name.localeCompare(b.name));
				break;
			case 'difficulty-asc':
				result.sort((a, b) => a.difficulty - b.difficulty || a.name.localeCompare(b.name));
				break;
			case 'difficulty-desc':
				result.sort((a, b) => b.difficulty - a.difficulty || a.name.localeCompare(b.name));
				break;
		}
		
		return result;
	});
	
	// Update URL when filters change
	function updateUrl() {
		const params = new URLSearchParams();
		if (searchQuery) params.set('q', searchQuery);
		if (selectedCategory) params.set('category', selectedCategory);
		if (selectedDifficulty) params.set('difficulty', selectedDifficulty);
		if (sortBy !== 'name') params.set('sort', sortBy);
		
		const newUrl = params.toString() ? `?${params.toString()}` : '/tricks';
		goto(newUrl, { replaceState: true, noScroll: true, keepFocus: true });
	}
	
	function clearFilters() {
		searchQuery = '';
		selectedCategory = '';
		selectedDifficulty = '';
		sortBy = 'name';
		goto('/tricks', { replaceState: true });
	}
	
	let hasActiveFilters = $derived(searchQuery || selectedCategory || selectedDifficulty);
</script>

<svelte:head>
	<title>Browse Tricks | Compendium of Juggling</title>
	<meta name="description" content="Browse {tricks.length} juggling tricks. Filter by ball count, difficulty, and search by name or siteswap.">
</svelte:head>

<div class="tricks-page">
	<section class="page-header">
		<div class="container">
			<h1>Browse Tricks</h1>
			<p>Explore {tricks.length} juggling patterns with animations and tutorials</p>
		</div>
	</section>

	<section class="filters-section">
		<div class="container">
			<div class="filters-bar">
				<div class="search-box">
					<svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
						<circle cx="11" cy="11" r="8"></circle>
						<path d="m21 21-4.35-4.35"></path>
					</svg>
					<input 
						type="text" 
						placeholder="Search tricks, siteswaps..." 
						bind:value={searchQuery}
						oninput={updateUrl}
					/>
				</div>
				
				<div class="filter-group">
					<select bind:value={selectedCategory} onchange={updateUrl}>
						<option value="">All Categories</option>
						{#each categories as cat}
							<option value={cat}>{cat}</option>
						{/each}
					</select>
					
					<select bind:value={selectedDifficulty} onchange={updateUrl}>
						<option value="">All Difficulties</option>
						{#each difficulties as diff}
							<option value={diff}>Level {diff}</option>
						{/each}
					</select>
					
					<select bind:value={sortBy} onchange={updateUrl}>
						<option value="name">Sort: A-Z</option>
						<option value="difficulty-asc">Difficulty: Low to High</option>
						<option value="difficulty-desc">Difficulty: High to Low</option>
					</select>
				</div>
				
				{#if hasActiveFilters}
					<button class="clear-filters btn btn-ghost" onclick={clearFilters}>
						<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
							<line x1="18" y1="6" x2="6" y2="18"></line>
							<line x1="6" y1="6" x2="18" y2="18"></line>
						</svg>
						Clear Filters
					</button>
				{/if}
			</div>
			
			<div class="results-info">
				<span class="results-count">
					Showing {filteredTricks.length} of {tricks.length} tricks
				</span>
			</div>
		</div>
	</section>

	<section class="tricks-list-section">
		<div class="container">
			{#if filteredTricks.length === 0}
				<div class="no-results">
					<div class="no-results-icon">🔍</div>
					<h3>No tricks found</h3>
					<p>Try adjusting your search or filters</p>
					<button class="btn btn-secondary" onclick={clearFilters}>Clear All Filters</button>
				</div>
			{:else}
				<div class="tricks-grid">
					{#each filteredTricks as trick (trick.id)}
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
									{#if trick.librarianLearned}
										<span class="badge badge-learned" title="Librarian's Pick">C</span>
									{/if}
								</div>
								<h3 class="trick-card-title">{trick.name}</h3>
								{#if trick.siteswap}
									<p class="trick-card-siteswap">{trick.siteswap}</p>
								{/if}
							</div>
						</a>
					{/each}
				</div>
			{/if}
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

	.filters-section {
		padding: var(--space-xl) 0;
		background: var(--color-bg-primary);
		border-bottom: 1px solid rgba(255, 255, 255, 0.05);
		position: sticky;
		top: var(--header-height);
		z-index: 50;
	}

	.filters-bar {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-md);
		align-items: center;
	}

	.search-box {
		flex: 1;
		min-width: 250px;
		position: relative;
	}

	.search-icon {
		position: absolute;
		left: var(--space-md);
		top: 50%;
		transform: translateY(-50%);
		color: var(--color-text-muted);
		pointer-events: none;
	}

	.search-box input {
		width: 100%;
		padding-left: calc(var(--space-md) + 24px + var(--space-sm));
	}

	.filter-group {
		display: flex;
		gap: var(--space-sm);
		flex-wrap: wrap;
	}

	.filter-group select {
		min-width: 150px;
	}

	.clear-filters {
		margin-left: auto;
	}

	.results-info {
		margin-top: var(--space-md);
	}

	.results-count {
		font-size: 0.875rem;
		color: var(--color-text-muted);
	}

	.tricks-list-section {
		padding: var(--space-2xl) 0 var(--space-4xl);
	}

	.tricks-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
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
		padding: var(--space-md);
	}

	.trick-card-badges {
		display: flex;
		gap: var(--space-sm);
		margin-bottom: var(--space-sm);
		flex-wrap: wrap;
	}

	.trick-card-title {
		font-family: var(--font-body);
		font-size: 1rem;
		font-weight: 600;
		margin-bottom: var(--space-xs);
	}

	.trick-card-siteswap {
		font-size: 0.8125rem;
		color: var(--color-text-muted);
		font-family: 'Courier New', monospace;
	}

	.no-results {
		text-align: center;
		padding: var(--space-4xl) 0;
	}

	.no-results-icon {
		font-size: 4rem;
		margin-bottom: var(--space-lg);
	}

	.no-results h3 {
		font-family: var(--font-body);
		margin-bottom: var(--space-sm);
	}

	.no-results p {
		color: var(--color-text-muted);
		margin: 0 auto var(--space-xl);
	}

	@media (max-width: 768px) {
		.filters-bar {
			flex-direction: column;
			align-items: stretch;
		}

		.search-box {
			width: 100%;
		}

		.filter-group {
			width: 100%;
		}

		.filter-group select {
			flex: 1;
			min-width: 0;
		}

		.clear-filters {
			margin-left: 0;
		}

		.tricks-grid {
			grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
			gap: var(--space-md);
		}

		.trick-card-content {
			padding: var(--space-sm);
		}

		.trick-card-badges {
			flex-direction: column;
			gap: var(--space-xs);
		}

		.trick-card-title {
			font-size: 0.9375rem;
		}
	}
</style>
