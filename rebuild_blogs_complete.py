#!/usr/bin/env python3
"""
Complete blog standardization - Extract content and rebuild with proper structure
"""

import os
import re
from pathlib import Path
from html.parser import HTMLParser
from html import unescape

class ContentExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_article = False
        self.article_content = []
        self.title = None
        
    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            pass
        elif tag == 'article' and any(k == 'class' and 'post-single' in v for k, v in attrs):
            self.in_article = True
            
    def handle_endtag(self, tag):
        if tag == 'article':
            self.in_article = False
    
    def handle_data(self, data):
        if self.in_article:
            self.article_content.append(data)

def extract_title(html_content):
    """Extract title from HTML"""
    match = re.search(r'<title>([^<]+)</title>', html_content, re.IGNORECASE)
    return match.group(1) if match else "Blog Post"

def extract_article_content(html_content):
    """Extract article HTML content"""
    # Find article tag and everything after it until /article
    match = re.search(r'(<article[^>]*>.*?</article>)', html_content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)
    
    # Fallback: look for common blog structure
    match = re.search(r'(<section class="blog">.*?</section>)', html_content, re.DOTALL)
    if match:
        return match.group(1)
    
    return None

def format_html(html_str):
    """Basic HTML formatting"""
    # Add newlines after common closing tags
    html_str = re.sub(r'(</div>|</section>|</article>|</p>|</h[1-6]>)', r'\1\n', html_str)
    html_str = re.sub(r'(>\s+)<', r'>\n<', html_str)  # Add newlines before opening tags
    
    # Add indentation (basic)
    lines = html_str.split('\n')
    formatted = []
    indent_level = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Decrease indent for closing tags
        if line.startswith('</'):
            indent_level = max(0, indent_level - 1)
        
        formatted.append('  ' * indent_level + line)
        
        # Increase indent for opening tags (but not self-closing or closing tags)
        if line.startswith('<') and not line.startswith('</') and not line.endswith('/>'):
            if not any(tag in line for tag in ['<meta', '<link', '<br', '<img', '<input', '<hr']):
                indent_level += 1
    
    return '\n'.join(formatted)

def rebuild_blog(file_path):
    """Rebuild blog with proper structure"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = Path(file_path).name
    title = extract_title(content)
    article_html = extract_article_content(content)
    
    if not article_html:
        return False, "No article content found"
    
    # Build proper HTML
    new_html = f'''<!doctype html>
<html lang="en">

<head>
  <!-- META TAGS - SEO CRITICAL -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="author" content="FSC Software">
  <meta name="description" content="Read our latest blog post about technology, software development, and digital solutions.">
  <meta name="keywords" content="technology, software, blog, development">
  
  <!-- PAGE TITLE -->
  <title>{title}</title>

  <!-- OPEN GRAPH TAGS - Social Media Sharing -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="Read our latest blog post about technology and software development.">
  <meta property="og:image" content="https://fsc-software.com/ico/preview.png">
  <meta property="og:site_name" content="FSC Software Blog">
  <meta property="og:url" content="https://fsc-software.com/{filename}">

  <!-- TWITTER CARD TAGS -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@fsc-software">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="Read our latest blog post about technology and software development.">
  <meta name="twitter:image" content="https://fsc-software.com/ico/preview.png">

  <!-- CANONICAL URL -->
  <link rel="canonical" href="https://fsc-software.com/{filename}">

  <!-- FAVICON FILES -->
  <link href="ico/favicon_fsc_144.png" rel="apple-touch-icon" sizes="144x144">
  <link href="ico/favicon_fsc_114.png" rel="apple-touch-icon" sizes="114x114">
  <link href="ico/favicon_fsc_72.png" rel="apple-touch-icon" sizes="72x72">
  <link href="ico/favicon_fsc_57.png" rel="apple-touch-icon">
  <link href="ico/favicon_fsc.png" rel="shortcut icon">

  <!-- CSS STYLESHEETS -->
  <link rel="stylesheet" href="css/animate.min.css">
  <link rel="stylesheet" href="css/font-awesome.min.css">
  <link rel="stylesheet" href="css/flipbox.min.css">
  <link rel="stylesheet" href="css/timeline.css">
  <link rel="stylesheet" href="css/odometer.min.css">
  <link rel="stylesheet" href="css/fancybox.min.css">
  <link rel="stylesheet" href="css/swiper.min.css">
  <link rel="stylesheet" href="css/bootstrap.min.css">
  <link rel="stylesheet" href="css/style.css">
</head>

<body>

  <!-- HEADER SECTION -->
  <header class="header">
    <div class="topbar">
      <div class="container">
        <div class="topbar-left">
          <ul class="topbar-menu">
            <li><a href="tel:+1234567890"><i class="fa fa-phone"></i> +1 234 567 890</a></li>
            <li><a href="mailto:info@fsc-software.com"><i class="fa fa-envelope"></i> info@fsc-software.com</a></li>
          </ul>
        </div>
      </div>
    </div>

    <nav class="navbar navbar-expand-lg navbar-light">
      <div class="container">
        <div class="logo">
          <a href="index.html">
            <img src="images/LOGO_FSC-01.png" alt="FSC Software Logo">
          </a>
        </div>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ml-auto">
            <li class="nav-item"><a class="nav-link" href="index.html">Home</a></li>
            <li class="nav-item"><a class="nav-link" href="services.html">Services</a></li>
            <li class="nav-item"><a class="nav-link" href="solutions01.html">Solutions</a></li>
            <li class="nav-item"><a class="nav-link" href="about-us.html">About</a></li>
            <li class="nav-item"><a class="nav-link" href="contact.html">Contact</a></li>
          </ul>
        </div>
      </div>
    </nav>
  </header>

  <!-- PAGE HEADER -->
  <section class="page-header">
    <div class="container">
      <h1 class="page-title">{title}</h1>
      <nav class="breadcrumb">
        <a href="index.html">Home</a>
        <span>/</span>
        <span>Blog</span>
      </nav>
    </div>
  </section>

  <!-- MAIN BLOG CONTENT -->
  <section class="blog">
    <div class="container">
      {article_html}
    </div>
  </section>

  <!-- FOOTER SECTION -->
  <footer class="footer">
    <div class="footer-content">
      <div class="container">
        <div class="row">
          <!-- Contact Info 1 -->
          <div class="col-md-4">
            <div class="contact-box">
              <h4><i class="fa fa-map-marker"></i> Head Office</h4>
              <p>123 Tech Street<br>New York, NY 10001<br>United States</p>
            </div>
          </div>

          <!-- Contact Info 2 -->
          <div class="col-md-4">
            <div class="contact-box">
              <h4><i class="fa fa-clock-o"></i> Working Hours</h4>
              <p>Monday - Friday: 9:00 AM - 6:00 PM<br>Saturday: 10:00 AM - 4:00 PM<br>Sunday: Closed</p>
            </div>
          </div>

          <!-- Contact Info 3 -->
          <div class="col-md-4">
            <div class="contact-box">
              <h4><i class="fa fa-headphones"></i> Support</h4>
              <p>Email: <a href="mailto:support@fsc-software.com">support@fsc-software.com</a><br>
              Phone: <a href="tel:+1234567890">+1 234 567 890</a></p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="sub-footer">
      <div class="container">
        <span class="copyright">© 2024 FSC Software. All rights reserved.</span>
      </div>
    </div>
  </footer>

</body>

</html>
'''
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    return True, "Rebuilt with proper structure"

def main():
    base_dir = Path('/Users/mac/Documents/fsc/fsc-adrien.github.io')
    blog_files = sorted(base_dir.glob('blog-*.html'))
    
    print("🔨 Rebuilding blog files with proper structure...\n")
    
    rebuilt_count = 0
    errors = []
    
    for file in blog_files:
        try:
            was_rebuilt, msg = rebuild_blog(str(file))
            if was_rebuilt:
                print(f"✅ REBUILT: {file.name}")
                rebuilt_count += 1
            else:
                print(f"⚠️  SKIPPED: {file.name} - {msg}")
                errors.append((file.name, msg))
        except Exception as e:
            print(f"❌ ERROR: {file.name} - {str(e)}")
            errors.append((file.name, str(e)))
    
    print(f"\n{'='*70}")
    print(f"✅ Rebuilt: {rebuilt_count}/{len(blog_files)} files")
    
    if errors:
        print(f"\n⚠️  Errors encountered:")
        for fname, err in errors:
            print(f"  - {fname}: {err}")

if __name__ == '__main__':
    main()
