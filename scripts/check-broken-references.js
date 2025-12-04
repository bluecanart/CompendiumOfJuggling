const fs = require('fs');
const tricks = JSON.parse(fs.readFileSync('./src/lib/data/tricks.json', 'utf8'));

// Create a set of all trick names (case-insensitive for matching)
const trickNames = new Set();
const trickNamesLower = new Map(); // lowercase -> original case

tricks.forEach(t => {
  trickNames.add(t.name);
  trickNamesLower.set(t.name.toLowerCase(), t.name);
});

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
        const lowerPrereq = prereq.toLowerCase();
        if (!trickNamesLower.has(lowerPrereq)) {
          brokenPrereqs.push({
            trick: trick.name,
            prereq: prereq
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
        const lowerRelated = related.toLowerCase();
        if (!trickNamesLower.has(lowerRelated)) {
          brokenRelated.push({
            trick: trick.name,
            related: related
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
    console.log(`  ${b.trick} -> ${b.prereq}`);
  });
}

console.log('\n=== Broken Related Tricks ===');
if (brokenRelated.length === 0) {
  console.log('None found!');
} else {
  brokenRelated.forEach(b => {
    console.log(`  ${b.trick} -> ${b.related}`);
  });
}

console.log(`\nTotal: ${brokenPrereqs.length} broken prerequisites, ${brokenRelated.length} broken related tricks`);

