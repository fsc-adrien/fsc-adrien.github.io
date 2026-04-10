#!/usr/bin/env python3
"""
Extract blog content from HTML files and rebuild them with proper template
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

def extract_content_from_html(html_content):
    """Extract main content from HTML file"""
    # Find post-content section
    match = re.search(r'<div class="post-content">(.*?)</div>\s*(?:<div class="post-tags">|</article>)', html_content, re.DOTALL)
    if match:
        content = match.group(1).strip()
        return content
    return None

def extract_title_from_html(html_content):
    """Extract title from HTML file"""
    # Try to find h2 in post-content first
    match = re.search(r'<title>(.*?)</title>', html_content)
    if match:
        title = match.group(1).strip()
        # Remove trailing " - FSC Software Blog" if present
        title = title.replace(' - FSC Software Blog', '')
        return title
    return "Untitled"

def main():
    base_dir = Path('/Users/mac/Documents/fsc/fsc-adrien.github.io')
    
    # Get list of all blog*.html files from git
    result = os.popen('cd /Users/mac/Documents/fsc/fsc-adrien.github.io && git ls-files "blog*.html" | grep -v blogs.html').read()
    blog_files = [line.strip() for line in result.strip().split('\n') if line.strip()]
    
    print(f"Found {len(blog_files)} blog files in git\n")
    
    for blog_file in blog_files:
        # Get content from git
        cmd = f'cd {base_dir} && git show HEAD:{blog_file}'
        git_content = os.popen(cmd).read()
        
        if not git_content:
            print(f"⚠️  {blog_file} - No content in git")
            continue
        
        # Extract data
        title = extract_title_from_html(git_content)
        content = extract_content_from_html(git_content)
        
        if not content:
            print(f"⚠️  {blog_file} - Could not extract content")
            continue
        
        # Extract date and author
        date_match = re.search(r'<span>(\w+\s+\d+,\s+\d+)</span>', git_content)
        date = date_match.group(1) if date_match else "October 5, 2023"
        
        author_match = re.search(r'<span>(?:January|February|March|April|May|June|July|August|September|October|November|December).*?</span>\s*<span>(.*?)</span>', git_content, re.DOTALL)
        author = author_match.group(1) if author_match else "FSC Software Team"
        
        # Extract tags
        tags = re.findall(r'<a href="blogs\.html">([^<]+)</a>', git_content)
        
        print(f"✓ {blog_file}")
        print(f"  Title: {title[:60]}...")
        print(f"  Content: {len(content)} chars")
        print(f"  Date: {date}")
        print(f"  Author: {author}")
        print(f"  Tags: {tags}\n")

if __name__ == '__main__':
    main()
