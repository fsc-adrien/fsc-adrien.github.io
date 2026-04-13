#!/usr/bin/env python3
"""Generate individual file fixes"""
import re
from pathlib import Path

files_to_fix = [
    'blog-ar-vr.html',
    'blog-5g-technology.html',
    'blog-ruby-rails.html',
    'blog-lowcode-nocode.html',
]

for file in files_to_fix:
    filepath = Path(f'/Users/mac/Documents/fsc/fsc-adrien.github.io/{file}')
    if not filepath.exists():
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get metadata
    title_m = re.search(r'<title>([^<]+)</title>', content, re.I)
    title = title_m.group(1) if title_m else 'Blog'
    
    desc_m = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', content, re.I)
    desc = desc_m.group(1) if desc_m else ''
    
    kw_m = re.search(r'<meta[^>]*name="keywords"[^>]*content="([^"]*)"', content, re.I)
    keywords = kw_m.group(1) if kw_m else ''
    
    # Get blog content
    blog_m = re.search(r'<section[^>]*class="blog"[^>]*>.*?</section>', content, re.I | re.DOTALL)
    if not blog_m:
        blog_m = re.search(r'<section[^>]*class="latest-news"[^>]*>.*?</section>', content, re.I | re.DOTALL)
    
    blog_content = blog_m.group(0) if blog_m else '<section class="blog"><div class="container"></div></section>'
    blog_content = blog_content.replace('class="latest-news"', 'class="blog"')
    
    h2_m = re.search(r'<h2[^>]*>([^<]+)</h2>', blog_content, re.I)
    breadcrumb = h2_m.group(1).strip()[:50] if h2_m else 'Blog'
    
    print(f'File: {file}')
    print(f'  Title: {title[:60]}...')
    print()
