#!/bin/bash

# Sync all blog files with proper header and footer
cd /Users/mac/Documents/fsc/fsc-adrien.github.io

python3 << 'EOF'
import os
import re
from pathlib import Path

def get_metadata(content):
    """Extract title, description, keywords from HTML"""
    title_match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
    title = title_match.group(1) if title_match else "Blog Post"
    
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content, re.IGNORECASE)
    desc = desc_match.group(1) if desc_match else title
    
    kw_match = re.search(r'<meta\s+name="keywords"\s+content="([^"]*)"', content, re.IGNORECASE)
    keywords = kw_match.group(1) if kw_match else ""
    
    return title, desc, keywords

def extract_blog_body(content):
    """Extract blog content"""
    # Try blog section
    match = re.search(r'<section\s+class="blog"[^>]*>(.*?)</section>', content, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1)
    # Try latest-news
    match = re.search(r'<section\s+class="latest-news"[^>]*>(.*?)</section>', content, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1)
    return ""

def get_h2_title(content):
    """Get first H2"""
    match = re.search(r'<h2[^>]*>([^<]+)</h2>', content, re.IGNORECASE)
    if match:
        title = match.group(1).strip()
        return title[:50] if len(title) > 50 else title
    return "Blog"

def build_page(title, desc, keywords, blog_body, filename):
    """Build complete HTML page"""
    h2_title = get_h2_title(blog_body) if blog_body else "Blog"
    
    header = f'''<!doctype html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>{title}</title>
  <meta name="author" content="FSCSoftware">
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{keywords}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://fsc-software.com/ico/preview.png">
  <meta property="og:site_name" content="FSC Software Blog">
  <meta property="og:title" content="{title}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://fsc-software.com/{filename}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@fsc-software">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="https://fsc-software.com/ico/preview.png">
  <link href="ico/favicon_fsc_144.png" rel="apple-touch-icon" sizes="144x144">
  <link href="ico/favicon_fsc_114.png" rel="apple-touch-icon" sizes="114x114">
  <link href="ico/favicon_fsc_72.png" rel="apple-touch-icon" sizes="72x72">
  <link href="ico/favicon_fsc_57.png" rel="apple-touch-icon">
  <link href="ico/favicon_fsc.png" rel="shortcut icon">
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

  <section class="page-header">
    <div class="container">
      <a href="javascript:window.print()" class="print">PRINT PAGE <img src="images/icon-print.png" alt="Image"></a>
      <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/">Home</a></li>
        <li class="breadcrumb-item"><a href="blogs.html">Blog</a></li>
        <li class="breadcrumb-item active" aria-current="page">{h2_title}</li>
      </ol>
      <h2>{title}</h2>
    </div>
  </section>

  <section class="blog">
    <div class="container">
      {blog_body}
    </div>
  </section>

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

</html>'''
    
    return header

base_path = Path(".")
blog_files = sorted(base_path.glob("blog-*.html"))

print(f"Processing {len(blog_files)} blog files...")
success = 0

for i, blog_file in enumerate(blog_files, 1):
    try:
        with open(blog_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        title, desc, keywords = get_metadata(content)
        blog_body = extract_blog_body(content)
        
        new_content = build_page(title, desc, keywords, blog_body, blog_file.name)
        
        with open(blog_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ [{i:2d}/{len(blog_files)}] {blog_file.name}")
        success += 1
    except Exception as e:
        print(f"❌ [{i:2d}/{len(blog_files)}] {blog_file.name} - {str(e)[:50]}")

print(f"\nSuccessfully synced: {success}/{len(blog_files)} files")
EOF
