#!/bin/bash
# Fix remaining blog files: blog-microservices.html, blog-cloud-computing-new.html, blog-devops-new.html, blog-microservices-new.html

cd /Users/mac/Documents/fsc/fsc-adrien.github.io

# Function to fix a blog file
fix_blog() {
    local file=$1
    if [ -f "$file" ]; then
        echo "Fixing $file..."
        
        # Replace latest-news with blog
        sed -i '' 's/class="latest-news"/class="blog"/g' "$file"
        
        # Remove wow fadeIn from col-lg-8
        sed -i '' 's/<div class="col-lg-8 wow fadeIn">/<div class="col-lg-8">/g' "$file"
        
        # Remove <span><strong>Tags:</strong></span>
        sed -i '' 's/<span><strong>Tags:<\/strong><\/span>//g' "$file"
        
        # Remove # from tags
        sed -i '' 's/<a href="blogs\.html">#/<a href="blogs.html">/g' "$file"
        
        # Remove end latest-news comments
        sed -i '' 's/<!-- end latest-news -->/<!-- end blog -->/g' "$file"
        
        echo "✅ Fixed $file"
    fi
}

fix_blog "blog-microservices.html"
fix_blog "blog-cloud-computing-new.html"
fix_blog "blog-devops-new.html"
fix_blog "blog-microservices-new.html"

echo "Done!"
