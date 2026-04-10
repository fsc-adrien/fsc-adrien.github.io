#!/usr/bin/env python3
"""
Clean all blog HTML files by removing duplicate/extra content after closing </html> tag
"""

import os
import re
from pathlib import Path

def clean_blog_file(file_path):
    """
    Remove any content that appears after the closing </html> tag
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the first occurrence of closing </html>
    html_close_pos = content.find('</html>')
    
    if html_close_pos == -1:
        return False, "No closing </html> tag found"
    
    # Get everything up to and including the closing </html> tag
    html_close_end = html_close_pos + len('</html>')
    
    # Check if there's content after </html>
    remaining_content = content[html_close_end:].strip()
    
    if remaining_content:
        # There's extra content after </html>
        cleaned_content = content[:html_close_end]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        return True, f"Removed {len(remaining_content)} characters of duplicate content"
    
    return False, "No duplicate content found"

def main():
    base_dir = Path('/Users/mac/Documents/fsc/fsc-adrien.github.io')
    
    # Find all blog*.html files
    blog_files = sorted(base_dir.glob('blog*.html'))
    
    print(f"Found {len(blog_files)} blog files to clean\n")
    
    cleaned_count = 0
    errors = []
    
    for blog_file in blog_files:
        try:
            was_cleaned, message = clean_blog_file(str(blog_file))
            
            status = "✓ CLEANED" if was_cleaned else "  OK"
            print(f"{status}: {blog_file.name} - {message}")
            
            if was_cleaned:
                cleaned_count += 1
                
        except Exception as e:
            error_msg = f"ERROR: {blog_file.name} - {str(e)}"
            print(f"✗ {error_msg}")
            errors.append(error_msg)
    
    print(f"\n{'='*70}")
    print(f"Summary: {cleaned_count} files cleaned out of {len(blog_files)} total")
    
    if errors:
        print(f"\nErrors encountered ({len(errors)}):")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✓ All files processed successfully!")

if __name__ == '__main__':
    main()
