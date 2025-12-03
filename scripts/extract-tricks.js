/**
 * Script to extract trick data from the old Library of Juggling HTML files
 * Run with: node scripts/extract-tricks.js
 */

import { readFileSync, writeFileSync, readdirSync, existsSync } from 'fs';
import { join, basename } from 'path';

const OLD_SITE_PATH = '../old-site/libraryofjuggling.com';

function decodeHtmlEntities(text) {
  return text
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, ' ');
}

function extractText(html) {
  return decodeHtmlEntities(html.replace(/<[^>]+>/g, '').trim());
}

function normalizeGifPath(src) {
  // Remove relative path prefixes and normalize
  let path = src.replace(/\.\.\//g, '');
  if (!path.startsWith('/')) {
    path = '/' + path;
  }
  return path;
}

function extractTutorialContent(descriptionHtml, mainGifUrl) {
  const content = [];
  
  if (!descriptionHtml) return content;
  
  // Find all images and their positions
  const imgRegex = /<img[^>]+src="([^"]*JugglingGifs[^"]+\.gif)"[^>]*>/gi;
  const images = [];
  let match;
  
  while ((match = imgRegex.exec(descriptionHtml)) !== null) {
    const gifUrl = normalizeGifPath(match[1]);
    // Skip the main animation (it's displayed separately)
    if (gifUrl !== mainGifUrl) {
      images.push({
        fullMatch: match[0],
        url: gifUrl,
        index: match.index,
        endIndex: match.index + match[0].length
      });
    }
  }
  
  // Process content in order, splitting by images
  let lastIndex = 0;
  
  for (const img of images) {
    // Get text before this image
    const textBefore = descriptionHtml.slice(lastIndex, img.index);
    const cleanText = extractText(textBefore.replace(/<br\s*\/?>/gi, '\n')).replace(/\s+/g, ' ').trim();
    
    // Add text content if non-empty
    if (cleanText) {
      content.push({ type: 'text', content: cleanText });
    }
    
    // Add the GIF
    content.push({ type: 'gif', url: img.url });
    
    lastIndex = img.endIndex;
  }
  
  // Get any remaining text after the last image
  const remainingText = descriptionHtml.slice(lastIndex);
  const cleanRemaining = extractText(remainingText.replace(/<br\s*\/?>/gi, '\n')).replace(/\s+/g, ' ').trim();
  
  if (cleanRemaining) {
    content.push({ type: 'text', content: cleanRemaining });
  }
  
  return content;
}

function extractTrickData(htmlContent, filename, category) {
  const trick = {
    id: '',
    name: '',
    slug: '',
    difficulty: 0,
    numBalls: 0,
    category: category,
    siteswap: '',
    prerequisites: [],
    relatedTricks: [],
    gifUrl: '',
    description: '',
    tutorialContent: [],
    tutorialLinks: [],
    librarianLearned: false
  };

  // Extract name from h1#Trickname
  const nameMatch = htmlContent.match(/<h1 id="Trickname">([^<]+)<\/h1>/);
  if (nameMatch) {
    trick.name = decodeHtmlEntities(nameMatch[1].trim());
  }

  // Generate slug from filename
  trick.slug = basename(filename, '.html')
    .replace(/%27/g, '')
    .replace(/'/g, '')
    .replace(/\s+/g, '-')
    .replace(/[()]/g, '')
    .toLowerCase();
  
  trick.id = trick.slug;

  // Determine number of balls from category
  const ballMatch = category.match(/(\d+)/);
  trick.numBalls = ballMatch ? parseInt(ballMatch[1]) : 3;

  // Extract siteswap
  const siteswapMatch = htmlContent.match(/<a href="http:\/\/www\.siteswap\.org\/"[^>]*>Siteswap<\/a><\/strong>:?\s*([^<]+)/i) ||
                        htmlContent.match(/Siteswap<\/span><\/a><\/strong><span[^>]*>:\s*([^<]+)/i) ||
                        htmlContent.match(/Siteswap<\/a><\/strong>:\s*([^<]+)/i);
  if (siteswapMatch) {
    trick.siteswap = extractText(siteswapMatch[1]).trim();
  }

  // Extract difficulty
  const difficultyMatch = htmlContent.match(/Difficulty \(1-10\):<\/strong>\s*(\d+)/);
  if (difficultyMatch) {
    trick.difficulty = parseInt(difficultyMatch[1]);
  }

  // Extract prerequisites
  const prereqMatch = htmlContent.match(/Prerequisites:<\/strong>\s*(.*?)(?=<\/li>)/is);
  if (prereqMatch) {
    const prereqHtml = prereqMatch[1];
    const prereqLinks = prereqHtml.match(/<a[^>]+href="([^"]+)"[^>]*>([^<]+)<\/a>/g) || [];
    trick.prerequisites = prereqLinks.map(link => {
      const textMatch = link.match(/>([^<]+)</);
      return textMatch ? decodeHtmlEntities(textMatch[1]) : '';
    }).filter(Boolean);
    
    // Also get non-link prerequisites
    const textPrereqs = extractText(prereqHtml);
    if (textPrereqs && textPrereqs !== 'None' && trick.prerequisites.length === 0) {
      trick.prerequisites = textPrereqs.split(',').map(p => p.trim()).filter(p => p && p !== 'None');
    }
  }

  // Extract related tricks
  const relatedMatch = htmlContent.match(/Related Tricks:<\/strong><\/span>?\s*(.*?)(?=<\/li>)/is) ||
                       htmlContent.match(/Related Tricks:<\/strong>\s*(.*?)(?=<\/li>)/is);
  if (relatedMatch) {
    const relatedHtml = relatedMatch[1];
    const relatedLinks = relatedHtml.match(/<a[^>]+href="[^"]+"[^>]*>([^<]+)<\/a>/g) || [];
    trick.relatedTricks = relatedLinks.map(link => {
      const textMatch = link.match(/>([^<]+)</);
      return textMatch ? decodeHtmlEntities(textMatch[1]) : '';
    }).filter(Boolean);
  }

  // Extract main GIF URL (the one with id="jugglinganimation")
  const mainGifMatch = htmlContent.match(/<img[^>]+id="jugglinganimation"[^>]+src="([^"]+)"/i) ||
                       htmlContent.match(/<img[^>]+src="([^"]+)"[^>]+id="jugglinganimation"/i);
  if (mainGifMatch) {
    trick.gifUrl = normalizeGifPath(mainGifMatch[1]);
  } else {
    // Fallback to first GIF found
    const fallbackGif = htmlContent.match(/src="([^"]*JugglingGifs\/[^"]+\.gif)"/i);
    if (fallbackGif) {
      trick.gifUrl = normalizeGifPath(fallbackGif[1]);
    }
  }

  // Extract description HTML for processing
  const descMatch = htmlContent.match(/<p id="description"[^>]*>([\s\S]*?)<\/p>/i);
  if (descMatch) {
    const descHtml = descMatch[1];
    
    // Extract tutorial content (ordered array of text and GIFs)
    trick.tutorialContent = extractTutorialContent(descHtml, trick.gifUrl);
    
    // Also create plain text description (for search/preview)
    let desc = descHtml;
    desc = desc.replace(/<img[^>]+>/gi, '');
    desc = desc.replace(/<br\s*\/?>/gi, '\n');
    desc = extractText(desc);
    desc = desc.replace(/\s+/g, ' ').trim();
    trick.description = desc;
  }

  // Extract tutorial links
  const tutorialSection = htmlContent.match(/<p id="tutoriallist">([\s\S]*?)<\/p>/i);
  if (tutorialSection) {
    const links = tutorialSection[1].match(/<a[^>]+href="([^"]+)"[^>]*>[\s\S]*?<\/a>/gi) || [];
    trick.tutorialLinks = links.map(link => {
      const urlMatch = link.match(/href="([^"]+)"/);
      const textMatch = link.match(/>([^<]*(?:<[^>]*>[^<]*)*)</);
      if (urlMatch && textMatch) {
        return {
          url: urlMatch[1],
          title: extractText(textMatch[1]).replace(/\s+/g, ' ').trim()
        };
      }
      return null;
    }).filter(Boolean);
  }

  return trick;
}

function processDirectory(dirName, category) {
  const dirPath = join(OLD_SITE_PATH, 'Tricks', dirName);
  const tricks = [];

  if (!existsSync(dirPath)) {
    console.log(`Directory not found: ${dirPath}`);
    return tricks;
  }

  const files = readdirSync(dirPath).filter(f => f.endsWith('.html'));
  
  for (const file of files) {
    try {
      const filePath = join(dirPath, file);
      const content = readFileSync(filePath, 'utf-8');
      const trick = extractTrickData(content, file, category);
      if (trick.name) {
        tricks.push(trick);
        const gifCount = trick.tutorialContent.filter(c => c.type === 'gif').length;
        console.log(`Extracted: ${trick.name}${gifCount > 0 ? ` (${gifCount} tutorial GIFs)` : ''}`);
      }
    } catch (err) {
      console.error(`Error processing ${file}:`, err.message);
    }
  }

  return tricks;
}

// Main execution
const allTricks = [];

const categories = [
  { dir: '3balltricks', name: '3 Ball' },
  { dir: '4balltricks', name: '4 Ball' },
  { dir: '5balltricks', name: '5 Ball' },
  { dir: '6balltricks', name: '6 Ball' }
];

for (const cat of categories) {
  console.log(`\nProcessing ${cat.name} tricks...`);
  const tricks = processDirectory(cat.dir, cat.name);
  allTricks.push(...tricks);
}

// Sort by difficulty, then by name
allTricks.sort((a, b) => {
  if (a.difficulty !== b.difficulty) return a.difficulty - b.difficulty;
  return a.name.localeCompare(b.name);
});

// Write to JSON file
const outputPath = join('src', 'lib', 'data', 'tricks.json');
writeFileSync(outputPath, JSON.stringify(allTricks, null, 2));

console.log(`\n✓ Extracted ${allTricks.length} tricks to ${outputPath}`);

// Summary with tutorial content stats
const summary = {
  total: allTricks.length,
  withTutorialGifs: allTricks.filter(t => t.tutorialContent.some(c => c.type === 'gif')).length,
  totalTutorialGifs: allTricks.reduce((sum, t) => sum + t.tutorialContent.filter(c => c.type === 'gif').length, 0),
  byCategory: {},
  byDifficulty: {}
};

for (const trick of allTricks) {
  summary.byCategory[trick.category] = (summary.byCategory[trick.category] || 0) + 1;
  summary.byDifficulty[trick.difficulty] = (summary.byDifficulty[trick.difficulty] || 0) + 1;
}

console.log('\nSummary:');
console.log('By Category:', summary.byCategory);
console.log('By Difficulty:', summary.byDifficulty);
console.log(`Tricks with tutorial GIFs: ${summary.withTutorialGifs}`);
console.log(`Total tutorial GIFs: ${summary.totalTutorialGifs}`);
