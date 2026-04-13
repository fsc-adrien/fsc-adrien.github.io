#!/bin/bash
# Sync all blog files with standard structure

cd /Users/mac/Documents/fsc/fsc-adrien.github.io

# Counter
count=0
total=$(ls blog-*.html 2>/dev/null | wc -l)

echo "Starting sync of $total blog files..."

for file in blog-*.html; do
    if [ -f "$file" ]; then
        # Check if file has favicon links
        if ! grep -q 'favicon_fsc' "$file"; then
            echo "⚠️  $file: Missing favicon tags"
        fi
        
        # Check if file has post-tags
        if ! grep -q 'post-tags' "$file"; then
            echo "⚠️  $file: Missing post-tags"
        fi
        
        # Check if file has full header (search-box)
        if ! grep -q 'search-box' "$file"; then
            echo "⚠️  $file: Missing search-box"
        fi
        
        count=$((count + 1))
    fi
done

echo "Checked $count files"
echo "Done!"
