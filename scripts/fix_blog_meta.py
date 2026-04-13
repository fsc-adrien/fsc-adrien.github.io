#!/usr/bin/env python3
"""
Fix blog files: format, add icons to post-meta, ensure content
"""

import os
import re
from pathlib import Path
from html.parser import HTMLParser

class BlogContentExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_post_content = False
        self.content = ""
        
    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for attr, val in attrs:
                if attr == "class" and "post-content" in val:
                    self.in_post_content = True
                elif attr == "class" and "post-tags" in val:
                    self.in_post_content = False
        if self.in_post_content:
            self.content += f"<{tag}>"
            
    def handle_endtag(self, tag):
        if self.in_post_content and tag == "div":
            self.in_post_content = False
        elif self.in_post_content:
            self.content += f"</{tag}>"
            
    def handle_data(self, data):
        if self.in_post_content:
            self.content += data

def fix_blog_file(file_path):
    """Fix a blog file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if post-meta already has icons
    has_icons = '<i class="fa fa-calendar">' in content or 'fa-calendar' in content
    
    if not has_icons:
        # Add icons to post-meta
        # Pattern: <span>DATE</span><span>AUTHOR</span>
        pattern = r'<div class="post-meta">\s*<span>([^<]+)</span>\s*<span>([^<]+)</span>\s*</div>'
        
        replacement = '''<div class="post-meta">
          <span class="post-date"><i class="fa fa-calendar"></i> \\1</span>
          <span class="post-author"><i class="fa fa-user"></i> \\2</span>
        </div>'''
        
        new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, "Added icons to post-meta"
    
    return False, "Already has icons"

def main():
    base_dir = Path('/Users/mac/Documents/fsc/fsc-adrien.github.io')
    blog_files = sorted(base_dir.glob('blog-*.html'))
    
    print("🔧 Fixing blog files...\n")
    
    fixed_count = 0
    
    for file in blog_files:
        try:
            was_fixed, msg = fix_blog_file(str(file))
            if was_fixed:
                print(f"✅ FIXED: {file.name} - {msg}")
                fixed_count += 1
            else:
                print(f"  OK: {file.name} - {msg}")
        except Exception as e:
            print(f"❌ ERROR: {file.name} - {str(e)}")
    
    print(f"\n{'='*70}")
    print(f"Fixed: {fixed_count} files")

if __name__ == '__main__':
    main()
