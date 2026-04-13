#!/bin/bash
# Restore blog files from git history

cd /Users/mac/Documents/fsc/fsc-adrien.github.io

echo "🔄 Restoring blog files from git..."

# Get list of blog files
blog_files=$(git ls-files | grep "^blog-.*\.html$" | grep -v "^blogs\.html$")

restored=0
skipped=0

for file in $blog_files; do
    if [ -f "$file" ]; then
        # Check if file is empty or has issues
        file_size=$(wc -c < "$file")
        
        if [ "$file_size" -lt 5000 ]; then
            echo "📥 Restoring: $file (size: $file_size bytes)"
            git checkout HEAD -- "$file"
            restored=$((restored + 1))
        else
            skipped=$((skipped + 1))
        fi
    fi
done

echo ""
echo "✅ Restored: $restored files"
echo "⏭️  Skipped: $skipped files (OK)"
