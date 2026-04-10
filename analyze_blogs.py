#!/usr/bin/env python3
"""
Apply proper header and footer templates to all restored blog files
while preserving their original content
"""

import os
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

def extract_blog_data(html_content):
    """Extract blog metadata and content from HTML"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract title
        title_tag = soup.find('title')
        title = title_tag.text if title_tag else "Untitled"
        
        # Extract content
        post_content = soup.find('div', class_='post-content')
        if post_content:
            content = str(post_content.decode_contents()) if hasattr(post_content, 'decode_contents') else post_content.get_text()
        else:
            content = ""
        
        # Extract metadata
        post_meta = soup.find('div', class_='post-meta')
        date = ""
        author = ""
        if post_meta:
            spans = post_meta.find_all('span')
            if len(spans) >= 2:
                date = spans[0].text.strip()
                author = spans[1].text.strip()
        
        # Extract tags
        post_tags = soup.find('div', class_='post-tags')
        tags = []
        if post_tags:
            links = post_tags.find_all('a')
            tags = [a.text.strip() for a in links]
        
        # Extract metadata for SEO
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '') if meta_desc else ""
        
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        keywords = meta_keywords.get('content', '') if meta_keywords else ""
        
        return {
            'title': title,
            'content': content,
            'date': date,
            'author': author,
            'tags': tags,
            'description': description,
            'keywords': keywords
        }
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return None

def main():
    base_dir = Path('/Users/mac/Documents/fsc/fsc-adrien.github.io')
    blog_files = sorted(base_dir.glob('blog-*.html'))
    
    # Filter out blogs.html
    blog_files = [f for f in blog_files if 'blogs.html' not in f.name]
    
    print(f"Analyzing {len(blog_files)} blog files...\n")
    
    for blog_file in blog_files[:5]:  # Just test first 5
        with open(blog_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        data = extract_blog_data(html_content)
        
        if data:
            print(f"✓ {blog_file.name}")
            print(f"  Title: {data['title'][:60]}")
            print(f"  Content length: {len(data['content'])} chars")
            print(f"  Date: {data['date']}")
            print(f"  Author: {data['author']}")
            print(f"  Tags: {data['tags']}")
            print()

if __name__ == '__main__':
    main()
