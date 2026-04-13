#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const Handlebars = require('handlebars');

// Helper function to extract content from minified blog HTML
function extractBlogContent(minifiedHtml) {
  try {
    // Extract h1 or h2 title
    let title = '';
    const titleMatch = minifiedHtml.match(/<h[12][^>]*>([^<]+)<\/h[12]>/);
    if (titleMatch) {
      title = titleMatch[1];
    }

    // Extract date from post-meta
    let date = 'April 6, 2026';
    const dateMatch = minifiedHtml.match(/<span[^>]*>([^<]*\d{4}[^<]*)<\/span>/);
    if (dateMatch && dateMatch[1].match(/\d{4}/)) {
      date = dateMatch[1];
    }

    // Extract all content between post-content divs
    let content = '';
    const contentMatch = minifiedHtml.match(/<div class="post-content">([^]*?)<\/div>\s*<div class="post-tags">/);
    if (contentMatch) {
      content = contentMatch[1].trim();
    }

    // Extract tags
    let tags = [];
    const tagsMatches = minifiedHtml.matchAll(/<a href="blogs\.html">([^<]+)<\/a>/g);
    for (const match of tagsMatches) {
      tags.push(match[1]);
    }

    return { title, date, content, tags };
  } catch (e) {
    console.error('Error extracting content:', e.message);
    return null;
  }
}

// Main build process
async function buildBlogs() {
  console.log('📦 FSC Blog Builder - Smart Mode\n');

  const baseDir = '/Users/mac/Documents/fsc/fsc-adrien.github.io';
  const blogDir = baseDir;
  const templateDir = path.join(baseDir, 'templates');

  // Read templates
  const layoutTemplate = fs.readFileSync(path.join(templateDir, 'layout.hbs'), 'utf8');
  const headerTemplate = fs.readFileSync(path.join(templateDir, '_header.hbs'), 'utf8');
  const pageHeaderTemplate = fs.readFileSync(path.join(templateDir, '_page-header.hbs'), 'utf8');
  const contentTemplate = fs.readFileSync(path.join(templateDir, '_blog-content.hbs'), 'utf8');
  const footerTemplate = fs.readFileSync(path.join(templateDir, '_footer.hbs'), 'utf8');

  // Register partials
  Handlebars.registerPartial('header', headerTemplate);
  Handlebars.registerPartial('page-header', pageHeaderTemplate);
  Handlebars.registerPartial('blog-content', contentTemplate);
  Handlebars.registerPartial('footer', footerTemplate);

  const layoutCompiled = Handlebars.compile(layoutTemplate);

  // Get all blog files
  const blogFiles = fs.readdirSync(blogDir)
    .filter(f => f.startsWith('blog-') && f.endsWith('.html') && f !== 'blogs.html')
    .sort();

  let successCount = 0;
  let failureCount = 0;

  for (const file of blogFiles) {
    try {
      const filePath = path.join(blogDir, file);
      const fileContent = fs.readFileSync(filePath, 'utf8');

      // Extract blog data from file
      const blogData = extractBlogContent(fileContent);

      if (!blogData || !blogData.content) {
        console.log(`⚠️  SKIP: ${file} - No content found`);
        continue;
      }

      // Prepare context for template
      const context = {
        title: blogData.title || file.replace('blog-', '').replace('.html', ''),
        date: blogData.date,
        content: blogData.content,
        tags: blogData.tags || []
      };

      // Compile and render
      const html = layoutCompiled(context);

      // Write output
      fs.writeFileSync(filePath, html, 'utf8');
      console.log(`✅ Built: ${file}`);
      successCount++;
    } catch (error) {
      console.log(`❌ Error: ${file} - ${error.message}`);
      failureCount++;
    }
  }

  console.log(`\n📊 Build Summary:`);
  console.log(`✅ Success: ${successCount} files`);
  console.log(`❌ Failures: ${failureCount} files`);
  console.log(`📁 Total: ${blogFiles.length} files`);

  if (successCount === blogFiles.length) {
    console.log(`\n🎉 Build completed successfully!`);
  }
}

buildBlogs().catch(console.error);
