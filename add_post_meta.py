#!/usr/bin/env python3
"""
Add post-meta to all blog files if missing
"""

import os
import re
from pathlib import Path

def add_post_meta_if_missing(file_path):
    """Add post-meta section if it's missing from blog file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if post-meta already exists
    if '<div class="post-meta">' in content or 'post-date' in content:
        return False, "Already has post-meta"
    
    # Find the post-single article start
    pattern = r'(<article class="post-single">)\s*(<div class="post-content">)'
    
    if not re.search(pattern, content):
        return False, "No post-single article found"
    
    # Create post-meta HTML
    post_meta = '''<div class="post-meta">
              <span class="post-date"><i class="fa fa-calendar"></i> April 6, 2026</span>
              <span class="post-author"><i class="fa fa-user"></i> FSC Software Team</span>
              <span class="post-category"><i class="fa fa-tag"></i> Technology</span>
            </div>

            '''
    
    # Insert post-meta before post-content
    new_content = re.sub(
        pattern,
        r'\1\n            ' + post_meta + r'\2',
        content
    )
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "Added post-meta"
    
    return False, "Pattern not found"

def main():
    base_dir = Path('/Users/mac/Documents/fsc/fsc-adrien.github.io')
    
    # Find all blog*.html files
    blog_files = sorted(base_dir.glob('blog-*.html'))
    
    print(f"Checking {len(blog_files)} blog files...\n")
    
    added_count = 0
    already_has = 0
    errors = []
    
    for blog_file in blog_files:
        try:
            was_added, message = add_post_meta_if_missing(str(blog_file))
            
            if was_added:
                print(f"✓ ADDED: {blog_file.name} - {message}")
                added_count += 1
            else:
                print(f"  OK: {blog_file.name} - {message}")
                already_has += 1
                
        except Exception as e:
            error_msg = f"ERROR: {blog_file.name} - {str(e)}"
            print(f"✗ {error_msg}")
            errors.append(error_msg)
    
    print(f"\n{'='*70}")
    print(f"Summary:")
    print(f"✓ Added post-meta: {added_count} files")
    print(f"  Already has: {already_has} files")
    
    if errors:
        print(f"\n✗ Errors: {len(errors)}")
        for error in errors:
            print(f"  - {error}")

if __name__ == '__main__':
    main()
