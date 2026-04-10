#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const glob = require('glob');

function fixBlogFile(filepath) {
  try {
    let content = fs.readFileSync(filepath, 'utf8');
    const original = content;
    const changes = [];

    // Fix 1: Replace .latest-news with .blog
    if (content.includes('class="latest-news"')) {
      content = content.replace(/class="latest-news"/g, 'class="blog"');
      changes.push('section');
    }

    // Fix 2: Remove wow fadeIn from col-lg-8
    content = content.replace(/<div class="col-lg-8\s+wow\s+fadeIn"/g, '<div class="col-lg-8"');

    // Fix 3: Remove sidebar and row divs
    content = content.replace(
      /<\/article>\s*<\/div>\s*\n\s*<div class="col-lg-4[^>]*>[\s\S]*?<\/div>\s*<\/div>\s*<\/div>\s*<\/section>/g,
      '</article>\n    </div>\n  </section>'
    );
    changes.push('sidebar');

    // Fix 4: Clean up post-tags
    content = content.replace(/<span><strong>Tags:<\/strong><\/span>\s*/g, '');
    content = content.replace(/<a href="blogs\.html">#([^<]+)<\/a>/g, '<a href="blogs.html">$1</a>');
    changes.push('tags');

    if (content !== original) {
      fs.writeFileSync(filepath, content, 'utf8');
      const filename = path.basename(filepath);
      console.log(`✅ ${filename}: fixed ${[...new Set(changes)].join(', ')}`);
      return true;
    } else {
      console.log(`⏭️  ${path.basename(filepath)}: already ok`);
      return false;
    }
  } catch (e) {
    console.log(`❌ ${path.basename(filepath)}: ${e.message}`);
    return false;
  }
}

const baseDir = '/Users/mac/Documents/fsc/fsc-adrien.github.io';
const blogFiles = glob.sync('blog-*.html', { cwd: baseDir }).sort();

console.log(`Fixing ${blogFiles.length} blog files...\n`);

let count = 0;
for (const file of blogFiles) {
  if (fixBlogFile(path.join(baseDir, file))) {
    count++;
  }
}

console.log(`\n✅ Done: ${count} files fixed`);
