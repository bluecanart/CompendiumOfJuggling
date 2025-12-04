<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { parseGIF, decompressFrames } from 'gifuct-js';
	
	interface Props {
		src: string;
		alt?: string;
	}
	
	let { src, alt = 'Animation' }: Props = $props();
	
	let canvas: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D | null = null;
	let frames: any[] = [];
	let frameIndex = $state(0);
	let isPlaying = $state(true);
	let speed = $state(1);
	let isLoading = $state(true);
	let loadError = $state(false);
	let animationId: number | null = null;
	let lastFrameTime = 0;
	let tempCanvas: HTMLCanvasElement;
	let tempCtx: CanvasRenderingContext2D | null = null;
	let gifWidth = $state(0);
	let gifHeight = $state(0);
	
	const speeds = [0.25, 0.5, 1, 1.5, 2];
	
	let isMounted = $state(false);
	let currentLoadedSrc = '';
	
	onMount(() => {
		ctx = canvas.getContext('2d');
		
		// Create temp canvas for frame composition
		tempCanvas = document.createElement('canvas');
		tempCtx = tempCanvas.getContext('2d');
		
		isMounted = true;
	});
	
	onDestroy(() => {
		if (animationId) {
			cancelAnimationFrame(animationId);
		}
	});
	
	// Watch for src changes and reload the GIF
	$effect(() => {
		// Track src dependency
		const currentSrc = src;
		
		// Only load if mounted and src has changed
		if (isMounted && currentSrc && currentSrc !== currentLoadedSrc) {
			// Cancel any existing animation
			if (animationId) {
				cancelAnimationFrame(animationId);
				animationId = null;
			}
			
			// Reset state
			frameIndex = 0;
			frames = [];
			isPlaying = true;
			speed = 1;
			currentLoadedSrc = currentSrc;
			
			loadGif();
		}
	});
	
	async function loadGif() {
		isLoading = true;
		loadError = false;
		
		try {
			const response = await fetch(src);
			const buffer = await response.arrayBuffer();
			const gif = parseGIF(buffer);
			frames = decompressFrames(gif, true);
			
			if (frames.length > 0) {
				gifWidth = frames[0].dims.width;
				gifHeight = frames[0].dims.height;
				canvas.width = gifWidth;
				canvas.height = gifHeight;
				tempCanvas.width = gifWidth;
				tempCanvas.height = gifHeight;
				
				isLoading = false;
				startAnimation();
			}
		} catch (err) {
			console.error('Failed to load GIF:', err);
			loadError = true;
			isLoading = false;
		}
	}
	
	function startAnimation() {
		if (!isPlaying || frames.length === 0) return;
		
		lastFrameTime = performance.now();
		animate();
	}
	
	function animate() {
		if (!isPlaying || !ctx || !tempCtx) return;
		
		const now = performance.now();
		const frame = frames[frameIndex];
		const frameDelay = (frame.delay || 100) / speed;
		
		if (now - lastFrameTime >= frameDelay) {
			renderFrame(frameIndex);
			frameIndex = (frameIndex + 1) % frames.length;
			lastFrameTime = now;
		}
		
		animationId = requestAnimationFrame(animate);
	}
	
	function renderFrame(index: number) {
		if (!ctx || !tempCtx) return;
		
		const frame = frames[index];
		const dims = frame.dims;
		
		// Handle disposal method from previous frame
		if (index > 0) {
			const prevFrame = frames[index - 1];
			if (prevFrame.disposalType === 2) {
				// Restore to background
				ctx.clearRect(0, 0, canvas.width, canvas.height);
			}
		}
		
		// Create ImageData from frame
		const imageData = new ImageData(
			new Uint8ClampedArray(frame.patch),
			dims.width,
			dims.height
		);
		
		// Draw frame patch to temp canvas
		tempCtx.putImageData(imageData, 0, 0);
		
		// Draw to main canvas at correct position
		ctx.drawImage(
			tempCanvas,
			0, 0, dims.width, dims.height,
			dims.left, dims.top, dims.width, dims.height
		);
	}
	
	function togglePlay() {
		isPlaying = !isPlaying;
		if (isPlaying) {
			startAnimation();
		} else if (animationId) {
			cancelAnimationFrame(animationId);
		}
	}
	
	function setSpeed(newSpeed: number) {
		speed = newSpeed;
	}
	
	function stepFrame(direction: number) {
		if (isPlaying) {
			isPlaying = false;
			if (animationId) cancelAnimationFrame(animationId);
		}
		frameIndex = (frameIndex + direction + frames.length) % frames.length;
		renderFrame(frameIndex);
	}
	
	// Re-render current frame when speed changes while paused
	$effect(() => {
		if (!isPlaying && frames.length > 0 && ctx) {
			renderFrame(frameIndex);
		}
	});
</script>

<div class="gif-player">
	<div class="gif-container" class:loading={isLoading}>
		{#if isLoading}
			<div class="gif-loading">
				<div class="spinner"></div>
				<span>Loading...</span>
			</div>
		{/if}
		
		{#if loadError}
			<div class="gif-error">
				<img {src} {alt} class="fallback-img" />
			</div>
		{:else}
			<canvas 
				bind:this={canvas} 
				class="gif-canvas"
				class:hidden={isLoading}
			></canvas>
		{/if}
	</div>
	
	{#if !loadError && !isLoading}
		<div class="gif-controls">
			<div class="controls-row">
				<button 
					class="control-btn" 
					onclick={() => stepFrame(-1)}
					title="Previous frame"
				>
					<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
						<path d="M6 6h2v12H6zm3.5 6l8.5 6V6z"/>
					</svg>
				</button>
				
				<button 
					class="control-btn play-btn" 
					onclick={togglePlay}
					title={isPlaying ? 'Pause' : 'Play'}
				>
					{#if isPlaying}
						<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
							<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
						</svg>
					{:else}
						<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
							<path d="M8 5v14l11-7z"/>
						</svg>
					{/if}
				</button>
				
				<button 
					class="control-btn" 
					onclick={() => stepFrame(1)}
					title="Next frame"
				>
					<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
						<path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z"/>
					</svg>
				</button>
			</div>
			
			<div class="speed-controls">
				<span class="speed-label">Speed:</span>
				<div class="speed-buttons">
					{#each speeds as s}
						<button 
							class="speed-btn"
							class:active={speed === s}
							onclick={() => setSpeed(s)}
						>
							{s}x
						</button>
					{/each}
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.gif-player {
		display: flex;
		flex-direction: column;
		gap: var(--space-md);
	}
	
	.gif-container {
		position: relative;
		background: var(--color-bg-tertiary);
		border-radius: var(--radius-lg);
		overflow: hidden;
		aspect-ratio: 1;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	
	.gif-canvas {
		max-width: 100%;
		max-height: 100%;
		object-fit: contain;
	}
	
	.gif-canvas.hidden {
		opacity: 0;
	}
	
	.gif-loading {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: var(--space-sm);
		color: var(--color-text-muted);
		font-size: 0.875rem;
	}
	
	.spinner {
		width: 32px;
		height: 32px;
		border: 3px solid var(--color-bg-hover);
		border-top-color: var(--color-accent-yellow);
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}
	
	@keyframes spin {
		to { transform: rotate(360deg); }
	}
	
	.gif-error {
		width: 100%;
		height: 100%;
	}
	
	.fallback-img {
		width: 100%;
		height: 100%;
		object-fit: contain;
	}
	
	.gif-controls {
		display: flex;
		flex-direction: column;
		gap: var(--space-sm);
		padding: var(--space-sm);
		background: var(--color-bg-tertiary);
		border-radius: var(--radius-md);
	}
	
	.controls-row {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: var(--space-sm);
	}
	
	.control-btn {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 36px;
		height: 36px;
		background: var(--color-bg-hover);
		border: none;
		border-radius: var(--radius-md);
		color: var(--color-text-secondary);
		cursor: pointer;
		transition: all var(--transition-fast);
	}
	
	.control-btn:hover {
		background: var(--color-bg-card);
		color: var(--color-text-primary);
	}
	
	.play-btn {
		width: 44px;
		height: 44px;
		background: var(--color-accent-yellow);
		color: var(--color-bg-primary);
	}
	
	.play-btn:hover {
		background: var(--color-accent-yellow);
		filter: brightness(1.1);
		color: var(--color-bg-primary);
	}
	
	.speed-controls {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: var(--space-sm);
	}
	
	.speed-label {
		font-size: 0.75rem;
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}
	
	.speed-buttons {
		display: flex;
		gap: 2px;
		background: var(--color-bg-hover);
		border-radius: var(--radius-sm);
		padding: 2px;
	}
	
	.speed-btn {
		padding: var(--space-xs) var(--space-sm);
		font-size: 0.75rem;
		font-weight: 600;
		background: transparent;
		border: none;
		border-radius: var(--radius-sm);
		color: var(--color-text-muted);
		cursor: pointer;
		transition: all var(--transition-fast);
	}
	
	.speed-btn:hover {
		color: var(--color-text-primary);
	}
	
	.speed-btn.active {
		background: var(--color-bg-card);
		color: var(--color-accent-yellow);
	}
</style>

