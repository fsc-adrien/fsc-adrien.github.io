#!/usr/bin/env python3
"""
Fix all blog files to use standard .blog section and remove sidebars
"""

import os
import re
from pathlib import Path

def fix_blog_file(filepath):
    """Fix a single blog file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original = f.read()
        
        content = original
        changes = []
        
        # Fix 1: Replace .latest-news with .blog
        if 'class="latest-news"' in content:
            content = content.replace('class="latest-news"', 'class="blog"')
            changes.append("section")
        
        # Fix 2: Remove wow fadeIn from col-lg-8
        content = re.sub(
            r'<div class="col-lg-8\s+wow\s+fadeIn"',
            '<div class="col-lg-8"',
            content
        )
        
        # Fix 3: Remove sidebar/col-lg-4 and wrapping divs
        # Pattern: </article></div> then <div class="col-lg-4"> ... lots of content ... </div></div></section>
        sidebar_pattern = r'(</article>\s*</div>\s*)\n\s*<div class="col-lg-4[^>]*>.*?</div>\s*</div>\s*</div>\s*(</section>)'
        content = re.sub(sidebar_pattern, r'\1\2', content, flags=re.DOTALL)
        changes.append("sidebar")
        
        # Fix 4: Clean up post-tags - remove # prefix and <span><strong>Tags:</strong></span>
        content = re.sub(
            r'<span><strong>Tags:</strong></span>\s*',
            '',
            content
        )
        content = re.sub(
            r'<a href="blogs\.html">#([^<]+)</a>',
            r'<a href="blogs.html">\1</a>',
            content
        )
        changes.append("tags")
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            filename = os.path.basename(filepath)
            print(f"✅ {filename}: fixed {', '.join(set(changes))}")
            return True
        else:
            print(f"⏭️  {os.path.basename(filepath)}: already ok")
            return False
    
    except Exception as e:
        print(f"❌ {os.path.basename(filepath)}: {str(e)}")
        return False

def main():
    """Main"""
    base_dir = '/Users/mac/Documents/fsc/fsc-adrien.github.io'
    blog_files = sorted(Path(base_dir).glob('blog-*.html'))
    
    print(f"Fixing {len(blog_files)} blog files...\n")
    
    count = 0
    for blog_file in blog_files:
        if fix_blog_file(str(blog_file)):
            count += 1
    
    print(f"\n✅ Done: {count} files fixed")

if __name__ == '__main__':
    main()
