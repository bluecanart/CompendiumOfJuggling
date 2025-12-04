const fs = require('fs');
const tricks = JSON.parse(fs.readFileSync('./src/lib/data/tricks.json', 'utf8'));

// Create a set of all trick names (case-insensitive for matching)
const trickNames = new Set();
const trickNamesLower = new Map(); // lowercase -> original case

tricks.forEach(t => {
  trickNames.add(t.name);
  trickNamesLower.set(t.name.toLowerCase(), t.name);
});

// Helper function to find close matches
function findCloseMatches(searchTerm, maxResults = 3) {
  const lowerSearch = searchTerm.toLowerCase().trim();
  const matches = [];
  
  tricks.forEach(t => {
    const lowerName = t.name.toLowerCase();
    // Check if search term is contained in name or vice versa
    if (lowerName.includes(lowerSearch) || lowerSearch.includes(lowerName)) {
      matches.push(t.name);
    }
  });
  
  return matches.slice(0, maxResults);
}

// Find broken references
const brokenPrereqs = [];
const brokenRelated = [];

tricks.forEach(trick => {
  // Check prerequisites
  if (trick.prerequisites && Array.isArray(trick.prerequisites)) {
    trick.prerequisites.forEach(prereq => {
      if (!prereq || !prereq.trim()) return;
      
      // Try exact match first
      if (!trickNames.has(prereq)) {
        // Try case-insensitive match
        const lowerPrereq = prereq.toLowerCase().trim();
        let found = false;
        for (const [lower, original] of trickNamesLower.entries()) {
          if (lower === lowerPrereq) {
            found = true;
            break;
          }
        }
        
        if (!found) {
          const closeMatches = findCloseMatches(prereq);
          brokenPrereqs.push({
            trick: trick.name,
            prereq: prereq,
            closeMatches: closeMatches
          });
        }
      }
    });
  }
  
  // Check related tricks
  if (trick.relatedTricks && Array.isArray(trick.relatedTricks)) {
    trick.relatedTricks.forEach(related => {
      if (!related || !related.trim()) return;
      
      // Try exact match first
      if (!trickNames.has(related)) {
        // Try case-insensitive match
        const lowerRelated = related.toLowerCase().trim();
        let found = false;
        for (const [lower, original] of trickNamesLower.entries()) {
          if (lower === lowerRelated) {
            found = true;
            break;
          }
        }
        
        if (!found) {
          const closeMatches = findCloseMatches(related);
          brokenRelated.push({
            trick: trick.name,
            related: related,
            closeMatches: closeMatches
          });
        }
      }
    });
  }
});

console.log('=== Broken Prerequisites ===');
if (brokenPrereqs.length === 0) {
  console.log('None found!');
} else {
  brokenPrereqs.forEach(b => {
    console.log(`\n${b.trick} -> "${b.prereq}"`);
    if (b.closeMatches.length > 0) {
      console.log(`  Possible matches: ${b.closeMatches.join(', ')}`);
    } else {
      console.log(`  No close matches found`);
    }
  });
}

console.log('\n\n=== Broken Related Tricks ===');
if (brokenRelated.length === 0) {
  console.log('None found!');
} else {
  brokenRelated.forEach(b => {
    console.log(`\n${b.trick} -> "${b.related}"`);
    if (b.closeMatches.length > 0) {
      console.log(`  Possible matches: ${b.closeMatches.join(', ')}`);
    } else {
      console.log(`  No close matches found`);
    }
  });
}

console.log(`\n\n=== Summary ===`);
console.log(`Total: ${brokenPrereqs.length} broken prerequisites, ${brokenRelated.length} broken related tricks`);

