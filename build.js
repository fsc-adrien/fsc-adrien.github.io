#!/usr/bin/env node

/**
 * Blog Builder - Compile Handlebars templates with blog content
 * 
 * Process:
 * 1. Extract blog metadata (title, description, keywords, date, tags) from existing HTML files
 * 2. Extract blog content section
 * 3. Compile with Handlebars templates
 * 4. Generate production-ready HTML files
 * 
 * Features:
 * - Clean code architecture
 * - SEO-optimized (canonical URLs, proper meta tags, structured data)
 * - Consistent styling
 * - Easy maintenance (change template = update all 78 files)
 */

const fs = require('fs');
const path = require('path');
const Handlebars = require('handlebars');

// ============================================================================
// CONFIGURATION
// ============================================================================

const BLOG_DIR = __dirname;
const TEMPLATE_DIR = path.join(__dirname, 'templates');
const OUTPUT_DIR = __dirname;

// Blog files to process
const BLOG_FILES = fs.readdirSync(BLOG_DIR)
  .filter(f => f.startsWith('blog-') && f.endsWith('.html'))
  .sort();

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Extract text between HTML tags
 */
function extractBetween(html, startTag, endTag) {
  const startIdx = html.indexOf(startTag);
  if (startIdx === -1) return '';
  const contentStart = startIdx + startTag.length;
  const endIdx = html.indexOf(endTag, contentStart);
  if (endIdx === -1) return '';
  return html.substring(contentStart, endIdx).trim();
}

/**
 * Extract title from <title> tag
 */
function extractTitle(html) {
  const match = html.match(/<title>([^<]+)<\/title>/i);
  return match ? match[1].replace(' - FSC Software Blog', '').trim() : 'Blog Post';
}

/**
 * Extract meta description
 */
function extractDescription(html) {
  const match = html.match(/<meta\s+name=["']description["']\s+content=["']([^"']+)["']/i);
  return match ? match[1] : 'Read our latest tech blog post';
}

/**
 * Extract meta keywords
 */
function extractKeywords(html) {
  const match = html.match(/<meta\s+name=["']keywords["']\s+content=["']([^"']+)["']/i);
  return match ? match[1] : 'blog, technology, software';
}

/**
 * Extract breadcrumb text (first 40 chars of title)
 */
function extractBreadcrumb(title) {
  return title.length > 40 ? title.substring(0, 40) + '...' : title;
}

/**
 * Extract date from post-meta
 */
function extractDate(html) {
  // Look for date in format: "April 7, 2026" or similar
  const match = html.match(/<div\s+class=["']post-meta["']>[\s\S]*?<span>([A-Za-z]+\s+\d+,\s+\d{4})/);
  return match ? match[1] : new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

/**
 * Extract post tags
 */
function extractTags(html) {
  const match = html.match(/<div\s+class=["']post-tags["']>([\s\S]*?)<\/div>/);
  if (!match) return [];

  const tagsHtml = match[1];
  const tags = [];
  const tagMatches = tagsHtml.matchAll(/<a[^>]*>([^<]+)<\/a>/g);

  for (const tagMatch of tagMatches) {
    const tag = tagMatch[1].trim();
    if (tag && tag !== '#') {
      tags.push(tag);
    }
  }

  return tags;
}

/**
 * Extract blog content from post-content div
 */
function extractContent(html) {
  // Find post-content section
  const match = html.match(/<div\s+class=["']post-content["']>([\s\S]*?)<\/div>\s*<div\s+class=["']post-tags["']/);
  if (!match) return '<p>Content not found</p>';

  let content = match[1].trim();

  // Remove sidebar references (col-lg-4)
  content = content.replace(/<div\s+class=["']col-lg-\d+["'][^>]*>[\s\S]*?<\/div>/g, '');

  // Remove aside tags
  content = content.replace(/<aside[^>]*>[\s\S]*?<\/aside>/g, '');

  // Remove icon spans from post-meta styling (keep text)
  content = content.replace(/<span><i\s+class=["']fa[^"']*["'][^>]*><\/i>\s*/g, '<span>');

  // Clean up extra whitespace
  content = content.replace(/\n\s*\n/g, '\n');

  return content.trim();
}

/**
 * Get filename from path
 */
function getFilename(filepath) {
  return path.basename(filepath);
}

// ============================================================================
// HANDLEBARS SETUP
// ============================================================================

// Register partials
function registerPartials() {
  const partialFiles = ['_header.hbs', '_footer.hbs', '_page-header.hbs', '_blog-content.hbs'];

  for (const partialFile of partialFiles) {
    const partialPath = path.join(TEMPLATE_DIR, partialFile);
    if (fs.existsSync(partialPath)) {
      const partialName = partialFile.replace('.hbs', '');
      const partialContent = fs.readFileSync(partialPath, 'utf-8');
      Handlebars.registerPartial(partialName, partialContent);
    }
  }
}

// ============================================================================
// MAIN BUILD FUNCTION
// ============================================================================

function buildBlog(filename) {
  try {
    const filepath = path.join(BLOG_DIR, filename);
    const html = fs.readFileSync(filepath, 'utf-8');

    // Extract metadata
    const title = extractTitle(html);
    const description = extractDescription(html);
    const keywords = extractKeywords(html);
    const breadcrumb = extractBreadcrumb(title);
    const date = extractDate(html);
    const tags = extractTags(html);
    const content = extractContent(html);

    // Load template
    const layoutPath = path.join(TEMPLATE_DIR, 'layout.hbs');
    const layoutTemplate = fs.readFileSync(layoutPath, 'utf-8');
    const compiled = Handlebars.compile(layoutTemplate);

    // Render with data
    const output = compiled({
      title,
      description,
      keywords,
      breadcrumb,
      date,
      tags,
      content,
      filename
    });

    // Write output
    const outputPath = path.join(OUTPUT_DIR, filename);
    fs.writeFileSync(outputPath, output, 'utf-8');

    console.log(`✅ Built: ${filename}`);
    return true;
  } catch (error) {
    console.error(`❌ Error building ${filename}:`, error.message);
    return false;
  }
}

// ============================================================================
// EXECUTION
// ============================================================================

function main() {
  console.log('📦 FSC Blog Builder - Starting...\n');

  // Register partials
  registerPartials();

  // Build all blogs
  let successCount = 0;
  let failureCount = 0;

  for (const filename of BLOG_FILES) {
    if (buildBlog(filename)) {
      successCount++;
    } else {
      failureCount++;
    }
  }

  // Summary
  console.log(`\n📊 Build Summary:`);
  console.log(`✅ Success: ${successCount} files`);
  console.log(`❌ Failures: ${failureCount} files`);
  console.log(`📁 Total: ${BLOG_FILES.length} files`);

  if (failureCount === 0) {
    console.log('\n🎉 Build completed successfully!');
    process.exit(0);
  } else {
    console.log('\n⚠️ Build completed with errors');
    process.exit(1);
  }
}

main();
