#!/usr/bin/env python3
"""
Complete blog synchronization script
- Adds full header (search-box, sandwich-menu, topbar, navbar)
- Adds all favicon links
- Standardizes layout to .blog section
- Removes sidebars
- Fixes post-tags format
- Handles minified and malformed files
"""

import os
import re
from pathlib import Path
import json

FULL_HEADER = '''<!doctype html>
<html lang="en">

<head>
  <!-- META TAGS -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>{title}</title>
  <meta name="author" content="FSCSoftware">
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">

  <!-- SOCIAL MEDIA META -->
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="https://fsc-software.com/ico/preview.png">
  <meta property="og:site_name" content="FSC Software Blog">
  <meta property="og:title" content="{title}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://fsc-software.com/{filename}">

  <!-- TWITTER META -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@fsc-software">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="https://fsc-software.com/ico/preview.png">

  <!-- FAVICON FILES -->
  <link href="ico/favicon_fsc_144.png" rel="apple-touch-icon" sizes="144x144">
  <link href="ico/favicon_fsc_114.png" rel="apple-touch-icon" sizes="114x114">
  <link href="ico/favicon_fsc_72.png" rel="apple-touch-icon" sizes="72x72">
  <link href="ico/favicon_fsc_57.png" rel="apple-touch-icon">
  <link href="ico/favicon_fsc.png" rel="shortcut icon">

  <!-- CSS FILES -->
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
  <div class="search-box">
    <div class="close-btn"> <span></span> <span></span> </div>
    <form>
      <input type="search" placeholder="Type here to search...">
      <h6>Type above and press enter or press close to cancel.</h6>
    </form>
  </div>

  <aside class="sandwich-menu">
    <div class="overlay"></div>
    <div class="logo"> <img src="images/LOGO_FSC-17.png" alt="Image"></div>
    <ul class="nav-menu">
      <li><a href="/">Home</a></li>
      <li><a href="about-us.html">About Us</a></li>
      <li><a href="blogs.html">Blogs</a></li>
      <li><a href="career.html">Careers</a></li>
      <li><a href="contact.html">Contact</a></li>
    </ul>
    <p>Welcome to FSC Software!<br>A comprehensive and effective IT outsourcing services provider.</p>
    <address>
      <p>12th Floor, 111 Y Lan Street, Phu Thi Ward,</p>
      <p>Gia Lam District, Ha Noi City, Viet Nam</p>
      <p>Call us: <a href="tel:+84969005169">+84 969 005 169</a><br>
        E-mail <a href="mailto:sales@fsc-software.com">sales@fsc-software.com</a></p>
    </address>
    <ul class="social-media">
      <li><a target="_blank" href="https://www.facebook.com/fscsoftwareglobal"><i class="fa fa-facebook"></i></a></li>
      <li><a target="_blank" href="https://www.instagram.com/fscsoftwarevn"><i class="fa fa-instagram"></i></a></li>
      <li><a target="_blank" href="https://www.linkedin.com/company/fsc-software"><i class="fa fa-linkedin"></i></a></li>
      <li><a href="mailto:sales@fsc-software.com"><i class="fa fa-google-plus"></i></a></li>
    </ul>
    <span class="copyright">© 2023 FSC Software - Software Development | IT Consultant | E-commerce Solutions</span>
  </aside>

  <header class="header">
    <div class="topbar">
      <div class="container">
        <div class="tagline">Your Trusted IT Outsourcing Partner for Seamless Solutions</div>
        <ul class="social-media">
          <li><a target="_blank" href="https://www.facebook.com/fscsoftwareglobal"><i class="fa fa-facebook"></i></a></li>
          <li><a target="_blank" href="https://www.instagram.com/fscsoftwarevn"><i class="fa fa-instagram"></i></a></li>
          <li><a target="_blank" href="https://www.linkedin.com/company/fsc-software"><i class="fa fa-linkedin"></i></a></li>
          <li><a href="mailto:sales@fsc-software.com"><i class="fa fa-google-plus"></i></a></li>
        </ul>
        <div class="phone"><a href="tel:+84969005169"><img src="images/icon-phone.png" alt="Image"> <span>+(84) 969 005 169</span></a></div>
      </div>
    </div>

    <nav class="navbar">
      <div class="container">
        <div class="logo"> <a href="/"> <img src="images/LOGO_FSC-01.png" alt="FSC Software"></a></div>
        <ul class="nav-menu">
          <li><a href="/">Home</a></li>
          <li><a href="about-us.html">About Us</a></li>
          <li><a href="blogs.html">Blogs</a></li>
          <li><a href="career.html">Careers</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
        <div class="search-btn"> <i class="fa fa-search"></i> </div>
        <div class="sandwich-btn"> <span></span> <span></span> <span></span> </div>
        <div class="bottom-bar"></div>
      </div>
    </nav>
  </header>

  <!-- PAGE HEADER -->
  <section class="page-header">
    <div class="container">
      <a href="javascript:window.print()" class="print">PRINT PAGE <img src="images/icon-print.png" alt="Image"></a>
      <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/">Home</a></li>
        <li class="breadcrumb-item"><a href="blogs.html">Blog</a></li>
        <li class="breadcrumb-item active" aria-current="page">{breadcrumb_title}</li>
      </ol>
      <h2>{page_title}</h2>
    </div>
  </section>
'''

FULL_FOOTER = '''
  <!-- FOOTER -->
  <footer class="footer">
    <div class="contact-wrapper">
      <div class="container">
        <div class="content-box"> <img src="images/footer-icon03.png" alt="Image">
          <h3>address infos</h3>
          <p>12th Floor, 111 Y Lan Street, Phu Thi Ward, Gia Lam District, Ha Noi City, Viet Nam</p>
        </div>
      </div>
    </div>
    <div class="sub-footer">
      <div class="container">
        <span class="copyright">© 2023 FSC Software - All rights reserved</span>
      </div>
    </div>
  </footer>

  <a href="#" class="scrollup"><i class="fa fa-long-arrow-up" aria-hidden="true"></i></a>

  <!-- JS FILES -->
  <script src="js/jquery.min.js"></script>
  <script src="js/popper.min.js"></script>
  <script src="js/bootstrap.min.js"></script>
  <script src="js/fancybox.min.js"></script>
  <script src="js/odometer.min.js"></script>
  <script src="js/timeline.js"></script>
  <script src="js/swiper.min.js"></script>
  <script src="js/isotope.min.js"></script>
  <script src="js/wow.min.js"></script>
  <script src="js/imagesloaded.pkgd.min.js"></script>
  <script src="js/scripts.js"></script>
</body>

</html>
'''

def prettify_html(content):
    """Add proper formatting to minified HTML"""
    # Add newlines and indentation
    content = re.sub(r'><', '>\n<', content)
    return content

def extract_title(content):
    """Extract title from HTML"""
    match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
    return match.group(1) if match else "FSC Software Blog"

def extract_description(content):
    """Extract description"""
    match = re.search(r'<meta name="description" content="([^"]+)"', content, re.IGNORECASE)
    return match.group(1) if match else "Discover insights on technology and business."

def extract_keywords(content):
    """Extract keywords"""
    match = re.search(r'<meta name="keywords" content="([^"]+)"', content, re.IGNORECASE)
    return match.group(1) if match else "blog, technology"

def extract_h2_title(content):
    """Extract first H2 tag content"""
    match = re.search(r'<h2[^>]*>([^<]+)</h2>', content, re.IGNORECASE)
    if match:
        title = match.group(1).strip()
        return title, title[:50]
    return "Blog Post", "Blog Post"

def extract_blog_content(content):
    """Extract blog/article content"""
    # Try to find .blog section
    match = re.search(r'<section[^>]*class="[^"]*blog[^"]*"[^>]*>(.*?)</section>', content, re.DOTALL | re.IGNORECASE)
    if match:
        return "<section class=\"blog\">\n" + match.group(1) + "\n</section>"
    
    # Try to find .latest-news section
    match = re.search(r'<section[^>]*class="[^"]*latest-news[^"]*"[^>]*>(.*?)</section>', content, re.DOTALL | re.IGNORECASE)
    if match:
        return "<section class=\"blog\">\n" + match.group(1) + "\n</section>"
    
    # Try article tag
    match = re.search(r'<article[^>]*>(.*?)</article>', content, re.DOTALL | re.IGNORECASE)
    if match:
        return "<section class=\"blog\">\n<div class=\"container\">\n" + match.group(0) + "\n</div>\n</section>"
    
    return None

def clean_blog_content(content):
    """Clean blog content"""
    # Remove sidebar
    content = re.sub(r'<div class="col-lg-4[^>]*>.*?</div>\s*</div>\s*</div>\s*</div>\s*</section>', '', content, flags=re.DOTALL)
    
    # Remove row wrapper
    content = re.sub(r'<div class="row">\s*<div class="col-lg-8[^>]*>', '<div class="container">\n<article class="post-single">', content)
    
    # Replace latest-news with blog
    content = content.replace('class="latest-news"', 'class="blog"')
    
    # Remove wow fadeIn
    content = re.sub(r'\s+class="[^"]*wow\s+fadeIn[^"]*"', '', content)
    
    # Clean post-meta
    content = re.sub(r'<span class="post-date"><i class="fa[^"]*"></i>\s*([^<]+)</span>', r'<span>\1</span>', content)
    content = re.sub(r'<span class="post-author"><i class="fa[^"]*"></i>\s*([^<]+)</span>', r'<span>\1</span>', content)
    content = re.sub(r'<span class="post-category"><i class="fa[^"]*"></i>\s*([^<]+)</span>', r'<span>\1</span>', content)
    
    # Clean post-tags
    content = re.sub(r'<span><strong>Tags:</strong></span>\s*', '', content)
    content = re.sub(r'<a href="blogs\.html">#([^<]+)</a>', r'<a href="blogs.html">\1</a>', content)
    
    # Wrap content in proper structure if needed
    if '<div class="container">' not in content:
        content = '<div class="container">\n' + content + '\n</div>'
    
    return content

def sync_blog_file(filepath):
    """Sync a blog file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if minified
        if len(content) > 1000 and '\n' not in content[:500]:
            content = prettify_html(content)
        
        title = extract_title(content)
        desc = extract_description(content)
        keywords = extract_keywords(content)
        page_title, breadcrumb = extract_h2_title(content)
        blog_content = extract_blog_content(content)
        
        if not blog_content:
            print(f"⚠️  Skip {os.path.basename(filepath)}: No content")
            return False
        
        blog_content = clean_blog_content(blog_content)
        
        filename = os.path.basename(filepath)
        new_html = FULL_HEADER.format(
            title=title,
            description=desc,
            keywords=keywords,
            filename=filename,
            breadcrumb_title=breadcrumb,
            page_title=page_title
        )
        
        new_html += "\n  <!-- BLOG CONTENT -->\n  " + blog_content + "\n"
        new_html += FULL_FOOTER
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print(f"✅ {filename}")
        return True
    
    except Exception as e:
        print(f"❌ {os.path.basename(filepath)}: {str(e)}")
        return False

def main():
    base_dir = '/Users/mac/Documents/fsc/fsc-adrien.github.io'
    blog_files = sorted(Path(base_dir).glob('blog-*.html'))
    
    print(f"\n{'='*70}")
    print(f"Syncing {len(blog_files)} blog files...")
    print(f"{'='*70}\n")
    
    success_count = 0
    for blog_file in blog_files:
        if sync_blog_file(str(blog_file)):
            success_count += 1
    
    print(f"\n{'='*70}")
    print(f"✅ Synced {success_count}/{len(blog_files)} blog files")
    print(f"{'='*70}\n")

if __name__ == '__main__':
    main()
