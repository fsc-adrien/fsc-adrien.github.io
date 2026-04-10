#!/bin/bash
# Sync all blog files one by one

cd /Users/mac/Documents/fsc/fsc-adrien.github.io

# Count
total=$(ls blog-*.html 2>/dev/null | wc -l)
count=1

for file in blog-*.html; do
    echo "[$count/$total] Processing $file..."
    ((count++))
done

echo "Total blog files: $total"
