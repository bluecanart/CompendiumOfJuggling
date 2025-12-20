<script lang="ts">
	import { base } from '$app/paths';
	import tricks from '$lib/data/tricks.json';
	
	let showDifficultyBreakdown = false;
	
	const stats = {
		totalTricks: tricks.length,
		twoBall: tricks.filter(t => t.numBalls === 2).length,
		threeBall: tricks.filter(t => t.numBalls === 3).length,
		fourBall: tricks.filter(t => t.numBalls === 4).length,
		fiveBall: tricks.filter(t => t.numBalls === 5).length,
		sixBall: tricks.filter(t => t.numBalls === 6).length,
		learnedTricks: tricks.filter(t => t.librarianLearned).length
	};
	
	const learningProgress = {
		learned: stats.learnedTricks,
		total: stats.totalTricks,
		percentage: Math.round((stats.learnedTricks / stats.totalTricks) * 100)
	};
	
	// Get unique difficulty levels and create progress for each
	const difficultyLevels = [...new Set(tricks.map(t => t.difficulty))].sort((a, b) => a - b);
	const difficultyProgress = difficultyLevels.map(level => {
		const tricksAtLevel = tricks.filter(t => t.difficulty === level);
		const learnedAtLevel = tricksAtLevel.filter(t => t.librarianLearned);
		return {
			level,
			learned: learnedAtLevel.length,
			total: tricksAtLevel.length,
			percentage: tricksAtLevel.length > 0 
				? Math.round((learnedAtLevel.length / tricksAtLevel.length) * 100)
				: 0
		};
	});
	
	function toggleDifficultyBreakdown() {
		showDifficultyBreakdown = !showDifficultyBreakdown;
	}
</script>

<svelte:head>
	<title>About | Compendium of Juggling</title>
	<meta name="description" content="Learn about the Compendium of Juggling - a comprehensive archive of juggling patterns and tricks for jugglers of all skill levels.">
</svelte:head>

<div class="about-page">
	<section class="page-header">
		<div class="container">
			<h1>About the Compendium</h1>
			<p>Preserving and sharing the art of toss juggling</p>
		</div>
	</section>

	<section class="about-content section">
		<div class="container">
			<div class="about-grid">
				<div class="about-main">
					<h2>What is it?</h2>
					<p>
						The Compendium of Juggling is an attempt to list all of the popular (and perhaps 
						not so popular) juggling tricks in one organized place. Despite the growing 
						popularity of juggling, few websites are dedicated to collecting and archiving 
						the various patterns that are being performed.
					</p>
					<p>
						Most jugglers are familiar with iconic tricks such as the 
						<a href="{base}/tricks/cascade">Cascade</a> and <a href="{base}/tricks/shower">Shower</a>, 
						but what about <a href="{base}/tricks/romeos-revenge">Romeo's Revenge</a> or the 
						<a href="{base}/tricks/531millsmess">531 Mills Mess</a>? The goal of this website is 
						to guarantee that the tricks currently circulating around the internet and at 
						juggling conventions are found, animated, and catalogued for the world to see.
					</p>

					<h2>What can I find here?</h2>
					<p>
						For every trick found in the Compendium, there is an animated representation of 
						the pattern created via <a href="https://jugglinglab.org/" target="_blank" rel="noopener">JugglingLab</a>, 
						in addition to general information about the trick (siteswap, difficulty level, 
						prerequisite tricks, etc.).
					</p>
					<p>
						Many tricks include detailed text-based tutorials with the help of animations, 
						along with links to other tutorials found online, ranging from YouTube videos 
						to private sites. If a tutorial isn't available, there will still be a short 
						description of the trick.
					</p>

					<h2>Where do I start?</h2>
					<p>
						If you have come to the Compendium looking to find out how to start juggling, 
						it would be best to begin with the <a href="{base}/tricks/cascade">Three Ball Cascade</a> 
						pattern. If you are a juggler who is already familiar with the basics, then 
						the various tricks included in the Compendium can be accessed via the 
						<a href="{base}/tricks">tricks browser</a>, or you can <a href="{base}/difficulty">view 
						all tricks by difficulty</a>.
					</p>

					<h2>About This Version</h2>
					<p>
						This is a modernized version of <a href="https://libraryofjuggling.com" target="_blank" rel="noopener">the original Library of Juggling website</a>. 
						The original site was created to preserve juggling knowledge, and this 
						redesign aims to make that content more accessible with a modern, 
						responsive interface while retaining all the valuable content from the 
						original archive.
					</p>
				</div>

				<aside class="about-sidebar">
					<div class="stats-card card">
						<h3>By the Numbers</h3>
						<div class="stats-list">
							<div class="stat-item">
								<span class="stat-value">{stats.totalTricks}</span>
								<span class="stat-label">Total Tricks</span>
							</div>
							<div class="stat-item">
								<span class="stat-value">{stats.twoBall}</span>
								<span class="stat-label">2 Ball Patterns</span>
							</div>
							<div class="stat-item">
								<span class="stat-value">{stats.threeBall}</span>
								<span class="stat-label">3 Ball Patterns</span>
							</div>
							<div class="stat-item">
								<span class="stat-value">{stats.fourBall}</span>
								<span class="stat-label">4 Ball Patterns</span>
							</div>
							<div class="stat-item">
								<span class="stat-value">{stats.fiveBall}</span>
								<span class="stat-label">5 Ball Patterns</span>
							</div>
							<div class="stat-item">
								<span class="stat-value">{stats.sixBall}</span>
								<span class="stat-label">6 Ball Patterns</span>
							</div>
						</div>
					</div>

					<div class="resources-card card">
						<h3>Resources</h3>
						<ul class="resources-list">
							<li>
								<a href="http://www.siteswap.org/" target="_blank" rel="noopener">
									<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
										<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
										<polyline points="15 3 21 3 21 9"></polyline>
										<line x1="10" y1="14" x2="21" y2="3"></line>
									</svg>
									Siteswap.org
								</a>
								<span>Learn siteswap notation</span>
							</li>
							<li>
								<a href="https://jugglinglab.org/" target="_blank" rel="noopener">
									<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
										<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
										<polyline points="15 3 21 3 21 9"></polyline>
										<line x1="10" y1="14" x2="21" y2="3"></line>
									</svg>
									Juggling Lab
								</a>
								<span>Animation software</span>
							</li>
							<li>
								<a href="https://libraryofjuggling.com/" target="_blank" rel="noopener">
									<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
										<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
										<polyline points="15 3 21 3 21 9"></polyline>
										<line x1="10" y1="14" x2="21" y2="3"></line>
									</svg>
									Library of Juggling
								</a>
								<span>The OG</span>
							</li>
							<li>
								<a href="https://www.jugglersguide.com/" target="_blank" rel="noopener">
									<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
										<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
										<polyline points="15 3 21 3 21 9"></polyline>
										<line x1="10" y1="14" x2="21" y2="3"></line>
									</svg>
									The Juggler's Guide
								</a>
								<span>Another great learning resource</span>
							</li>
							<li>
								<a href="https://skilldex.org/home" target="_blank" rel="noopener">
									<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
										<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
										<polyline points="15 3 21 3 21 9"></polyline>
										<line x1="10" y1="14" x2="21" y2="3"></line>
									</svg>
									Skilldex
								</a>
								<span>The ultimate trick database</span>
							</li>
							<li>
								<a href="https://www.juggle.org/" target="_blank" rel="noopener">
									<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
										<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
										<polyline points="15 3 21 3 21 9"></polyline>
										<line x1="10" y1="14" x2="21" y2="3"></line>
									</svg>
									IJA - International Jugglers' Association
								</a>
								<span>Juggling community</span>
							</li>
							<li>
								<a href="https://www.reddit.com/r/juggling/" target="_blank" rel="noopener">
									<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
										<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
										<polyline points="15 3 21 3 21 9"></polyline>
										<line x1="10" y1="14" x2="21" y2="3"></line>
									</svg>
									r/juggling
								</a>
								<span>Reddit community</span>
							</li>
						</ul>
					</div>

					<div class="start-card card">
						<h3>Ready to Start?</h3>
						<p>Begin your juggling journey with the basics.</p>
						<a href="{base}/tricks/cascade" class="btn btn-primary">Learn the Cascade</a>
					</div>

					<div class="progress-card card">
						<h3>Site Admin Learning Progress</h3>
						<div class="progress-stats">
							<div class="progress-numbers">
								<span class="progress-value">{learningProgress.learned} / {learningProgress.total}</span>
								<span class="progress-label">tricks learned</span>
							</div>
							<div class="progress-percentage">{learningProgress.percentage}%</div>
						</div>
						<div class="progress-bar-container">
							<div class="progress-bar-fill" style="width: {learningProgress.percentage}%"></div>
						</div>
						
						<button class="see-more-btn" on:click={toggleDifficultyBreakdown}>
							<span>{showDifficultyBreakdown ? 'Hide Details' : 'Details'}</span>
							<svg 
								width="16" 
								height="16" 
								viewBox="0 0 24 24" 
								fill="none" 
								stroke="currentColor" 
								stroke-width="2"
								class:rotated={showDifficultyBreakdown}
							>
								<polyline points="6 9 12 15 18 9"></polyline>
							</svg>
						</button>
						
						{#if showDifficultyBreakdown}
							<div class="difficulty-breakdown">
								<div class="breakdown-title">By Difficulty Level</div>
								{#each difficultyProgress as diff}
									<div class="difficulty-progress-item">
										<div class="difficulty-header">
											<span class="difficulty-label">Level {diff.level}</span>
											<span class="difficulty-stat">{diff.learned} / {diff.total}</span>
											<span class="difficulty-percentage">{diff.percentage}%</span>
										</div>
										<div class="mini-progress-bar-container">
											<div class="mini-progress-bar-fill" style="width: {diff.percentage}%"></div>
										</div>
									</div>
								{/each}
							</div>
						{/if}
					</div>
				</aside>
			</div>
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

	.about-grid {
		display: grid;
		grid-template-columns: 1fr 320px;
		gap: var(--space-3xl);
		align-items: start;
	}

	.about-main h2 {
		font-family: var(--font-body);
		font-size: 1.5rem;
		margin-top: var(--space-2xl);
		margin-bottom: var(--space-md);
	}

	.about-main h2:first-child {
		margin-top: 0;
	}

	.about-main p {
		font-size: 1.0625rem;
		line-height: 1.8;
		margin-bottom: var(--space-lg);
	}

	.about-main a {
		color: var(--color-accent-yellow);
		text-decoration: underline;
	}

	.about-sidebar {
		position: sticky;
		top: calc(var(--header-height) + var(--space-xl));
		display: flex;
		flex-direction: column;
		gap: var(--space-lg);
	}

	.stats-card,
	.resources-card,
	.start-card,
	.progress-card {
		padding: var(--space-xl);
	}

	.stats-card h3,
	.resources-card h3,
	.start-card h3,
	.progress-card h3 {
		font-family: var(--font-body);
		font-size: 1rem;
		font-weight: 600;
		margin-bottom: var(--space-lg);
	}

	.progress-stats {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: var(--space-md);
	}

	.progress-numbers {
		display: flex;
		flex-direction: column;
		gap: var(--space-xs);
	}

	.progress-value {
		font-family: var(--font-display);
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--color-accent-yellow);
	}

	.progress-label {
		font-size: 0.875rem;
		color: var(--color-text-muted);
	}

	.progress-percentage {
		font-family: var(--font-display);
		font-size: 2rem;
		font-weight: 700;
		color: var(--color-accent-yellow);
	}

	.progress-bar-container {
		width: 100%;
		height: 12px;
		background: rgba(255, 255, 255, 0.05);
		border-radius: 6px;
		overflow: hidden;
		position: relative;
	}

	.progress-bar-fill {
		height: 100%;
		background: linear-gradient(90deg, var(--color-accent-yellow), var(--color-accent-purple));
		border-radius: 6px;
		transition: width 0.6s ease-out;
		box-shadow: 0 0 10px rgba(255, 206, 84, 0.5);
	}

	.see-more-btn {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: var(--space-xs);
		width: 100%;
		margin-top: var(--space-lg);
		padding: var(--space-sm) var(--space-md);
		background: rgba(255, 255, 255, 0.03);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 6px;
		color: var(--color-text-muted);
		font-size: 0.875rem;
		font-weight: 500;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.see-more-btn:hover {
		background: rgba(255, 255, 255, 0.05);
		border-color: rgba(255, 255, 255, 0.2);
		color: var(--color-text-primary);
	}

	.see-more-btn svg {
		transition: transform 0.3s ease;
	}

	.see-more-btn svg.rotated {
		transform: rotate(180deg);
	}

	.difficulty-breakdown {
		margin-top: var(--space-lg);
		padding-top: var(--space-lg);
		border-top: 1px solid rgba(255, 255, 255, 0.1);
		animation: slideDown 0.3s ease-out;
	}

	@keyframes slideDown {
		from {
			opacity: 0;
			transform: translateY(-10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.breakdown-title {
		font-size: 0.875rem;
		font-weight: 600;
		color: var(--color-text-muted);
		margin-bottom: var(--space-md);
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.difficulty-progress-item {
		margin-bottom: var(--space-md);
	}

	.difficulty-progress-item:last-child {
		margin-bottom: 0;
	}

	.difficulty-header {
		display: flex;
		align-items: center;
		gap: var(--space-sm);
		margin-bottom: var(--space-xs);
		font-size: 0.8125rem;
	}

	.difficulty-label {
		font-weight: 500;
		color: var(--color-text-primary);
		flex-shrink: 0;
	}

	.difficulty-stat {
		color: var(--color-text-muted);
		font-size: 0.75rem;
		flex-grow: 1;
	}

	.difficulty-percentage {
		font-weight: 600;
		color: var(--color-accent-yellow);
		font-size: 0.75rem;
		flex-shrink: 0;
	}

	.mini-progress-bar-container {
		width: 100%;
		height: 6px;
		background: rgba(255, 255, 255, 0.05);
		border-radius: 3px;
		overflow: hidden;
	}

	.mini-progress-bar-fill {
		height: 100%;
		background: linear-gradient(90deg, var(--color-accent-yellow), var(--color-accent-purple));
		border-radius: 3px;
		transition: width 0.6s ease-out;
	}

	.stats-list {
		display: flex;
		flex-direction: column;
		gap: var(--space-md);
	}

	.stat-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: var(--space-sm) 0;
		border-bottom: 1px solid rgba(255, 255, 255, 0.05);
	}

	.stat-item:last-child {
		border-bottom: none;
	}

	.stat-value {
		font-family: var(--font-display);
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--color-accent-yellow);
	}

	.stat-label {
		font-size: 0.875rem;
		color: var(--color-text-muted);
	}

	.resources-list {
		list-style: none;
		display: flex;
		flex-direction: column;
		gap: var(--space-md);
	}

	.resources-list li a {
		display: flex;
		align-items: center;
		gap: var(--space-sm);
		font-weight: 500;
		color: var(--color-text-primary);
	}

	.resources-list li a:hover {
		color: var(--color-accent-yellow);
	}

	.resources-list li span {
		display: block;
		font-size: 0.8125rem;
		color: var(--color-text-muted);
		margin-left: calc(16px + var(--space-sm));
	}

	.start-card p {
		font-size: 0.9375rem;
		margin-bottom: var(--space-lg);
	}

	.start-card .btn {
		width: 100%;
	}

	@media (max-width: 900px) {
		.about-grid {
			grid-template-columns: 1fr;
		}

		.about-sidebar {
			position: static;
			display: grid;
			grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
		}
	}
</style>

