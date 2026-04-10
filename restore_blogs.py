#!/usr/bin/env python3
"""
Restore all blog files from git with proper content
"""

import os
import subprocess
from pathlib import Path

def restore_file_from_git(file_path):
    """Restore file from git"""
    try:
        result = subprocess.run(
            ['git', 'checkout', 'HEAD', '--', file_path],
            cwd='/Users/mac/Documents/fsc/fsc-adrien.github.io',
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    base_dir = Path('/Users/mac/Documents/fsc/fsc-adrien.github.io')
    
    # Get all blog files
    result = subprocess.run(
        ['git', 'ls-files', 'blog*.html'],
        cwd=str(base_dir),
        capture_output=True,
        text=True
    )
    
    blog_files = [line.strip() for line in result.stdout.strip().split('\n') if line.strip() and 'blogs.html' not in line]
    
    print(f"Restoring {len(blog_files)} blog files from git...\n")
    
    restored = 0
    failed = 0
    
    for blog_file in blog_files:
        file_path = f'{blog_file}'
        if restore_file_from_git(file_path):
            print(f"✓ {blog_file}")
            restored += 1
        else:
            print(f"✗ {blog_file} - FAILED")
            failed += 1
    
    print(f"\n{'='*70}")
    print(f"✓ Restored: {restored} files")
    print(f"✗ Failed: {failed} files")
    print(f"\nAll blog files restored from git!")

if __name__ == '__main__':
    main()
