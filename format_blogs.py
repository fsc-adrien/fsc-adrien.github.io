#!/usr/bin/env python3
"""
Format all minified blog HTML files and restore them properly
"""

import os
import re
from pathlib import Path

def format_html(content):
    """Format minified HTML to be readable"""
    # Add newlines after common tags
    content = re.sub(r'(</(div|section|article|header|footer|aside|nav|ul|ol|li|p|h[1-6]|span)>)', r'\1\n', content)
    content = re.sub(r'(</head>)', r'\1\n', content)
    content = re.sub(r'(<body)', r'\n\1', content)
    content = re.sub(r'(</body>)', r'\n\1', content)
    content = re.sub(r'(</html>)', r'\1\n', content)
    
    # Add indentation
    lines = content.split('\n')
    formatted_lines = []
    indent_level = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Decrease indent for closing tags
        if re.match(r'^</', line):
            indent_level = max(0, indent_level - 1)
        
        # Add indentation
        formatted_lines.append('  ' * indent_level + line)
        
        # Increase indent for opening tags (but not self-closing)
        if re.match(r'^<[^/]', line) and not re.search(r'/>\s*$', line) and not re.search(r'</.*>\s*$', line):
            indent_level += 1
    
    return '\n'.join(formatted_lines)

def restore_blog_file(file_path):
    """Restore a blog file with proper structure"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file is minified (very long single line)
    lines = content.split('\n')
    if len(lines) < 50 and len(content) > 5000:
        print(f"  Formatting minified: {Path(file_path).name}")
        
        # Format the HTML
        formatted = format_html(content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(formatted)
        
        return True, "Formatted minified HTML"
    elif len(lines) < 50 and len(content) < 1000:
        print(f"  ⚠️  Very short file: {Path(file_path).name}")
        return False, "File too short (possibly broken)"
    else:
        return False, "Already formatted"

def main():
    base_dir = Path('/Users/mac/Documents/fsc/fsc-adrien.github.io')
    
    # Find all blog*.html files
    blog_files = sorted(base_dir.glob('blog*.html'))
    
    print(f"📋 Processing {len(blog_files)} blog files...\n")
    
    formatted_count = 0
    short_files = []
    
    for blog_file in blog_files:
        try:
            was_formatted, message = restore_blog_file(str(blog_file))
            
            if was_formatted:
                formatted_count += 1
            elif "short" in message.lower():
                short_files.append(blog_file.name)
                
        except Exception as e:
            print(f"❌ Error processing {blog_file.name}: {str(e)}")
    
    print(f"\n{'='*70}")
    print(f"📊 Summary:")
    print(f"  ✅ Formatted: {formatted_count} files")
    print(f"  ⚠️  Potentially broken: {len(short_files)} files")
    
    if short_files:
        print(f"\n  Potentially broken files:")
        for f in short_files:
            print(f"    - {f}")

if __name__ == '__main__':
    main()
