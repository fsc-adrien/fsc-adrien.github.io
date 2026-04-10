#!/usr/bin/env python3
"""
Complete blog synchronization script - fixes all 78 blog files
Ensures consistent structure, headers, footers, and formatting
"""

import os
import re
from pathlib import Path

def prettify_html(content):
    """Format minified HTML by adding newlines and indentation"""
    # Add newlines after tags
    content = re.sub(r'><', '>\n<', content)
    return content

def extract_title(content):
    """Extract page title from <title> tag"""
    match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
    return match.group(1) if match else "Blog Post"

def extract_description(content):
    """Extract meta description"""
    match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content, re.IGNORECASE)
    return match.group(1) if match else ""

def extract_keywords(content):
    """Extract meta keywords"""
    match = re.search(r'<meta\s+name="keywords"\s+content="([^"]+)"', content, re.IGNORECASE)
    return match.group(1) if match else ""

def extract_h2_title(content):
    """Extract first H2 as page breadcrumb title"""
    # Look for first H2 in content
    match = re.search(r'<h2[^>]*>([^<]+)</h2>', content, re.IGNORECASE)
    if match:
        text = match.group(1).strip()
        # Keep first 50 chars for breadcrumb
        return text[:50] if len(text) > 50 else text
    return "Blog"

def extract_blog_content(content):
    """Extract the main blog content section"""
    # Try to find .blog section
    blog_match = re.search(r'<section\s+class="blog"[^>]*>.*?</section>', content, re.IGNORECASE | re.DOTALL)
    if blog_match:
        return blog_match.group(0)
    
    # Try .latest-news section
    latest_match = re.search(r'<section\s+class="latest-news"[^>]*>.*?</section>', content, re.IGNORECASE | re.DOTALL)
    if latest_match:
        return latest_match.group(0)
    
    # Try article tag
    article_match = re.search(r'<article[^>]*>.*?</article>', content, re.IGNORECASE | re.DOTALL)
    if article_match:
        return article_match.group(0)
    
    return None

def clean_blog_content(content):
    """Standardize blog content structure"""
    # Convert .latest-news to .blog
    content = re.sub(r'class="latest-news"', 'class="blog"', content, flags=re.IGNORECASE)
    
    # Remove sidebars (col-lg-4)
    content = re.sub(r'<div\s+class="col-lg-4[^"]*"[^>]*>.*?</div>\s*</div>\s*</div>\s*</section>', 
                     '</article>\n    </div>\n  </section>', content, re.IGNORECASE | re.DOTALL)
    
    # Remove wrapping row divs if they have col-lg-8
    content = re.sub(r'<div\s+class="row"[^>]*>\s*<div\s+class="col-lg-8[^"]*"[^>]*>',
                     '', content, re.IGNORECASE)
    
    # Clean post-meta: remove icon spans
    content = re.sub(r'<span><i\s+class="fa\s+fa-calendar[^"]*"></i>\s*', '<span>', content, re.IGNORECASE)
    content = re.sub(r'<span><i\s+class="fa\s+fa-user[^"]*"></i>\s*', '<span>', content, re.IGNORECASE)
    content = re.sub(r'<span><i\s+class="fa\s+fa-folder[^"]*"></i>\s*', '<span>', content, re.IGNORECASE)
    
    # Clean post-tags: remove # symbols and <span> wrappers
    content = re.sub(r'<span><strong>Tags:</strong></span>', '', content)
    content = re.sub(r'#([a-zA-Z0-9\-]+)', r'\1', content)  # Remove # prefix
    
    # Fix post-tags format
    content = re.sub(r'<a\s+href="[^"]*">([^<]+)</a>', r'<a href="blogs.html">\1</a>', content)
    
    return content

def sync_blog_file(filepath):
    """Sync a single blog file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Prettify if minified
        if content.count('\n') < 50:  # Likely minified
            content = prettify_html(content)
        
        # Extract metadata
        title = extract_title(content)
        description = extract_description(content)
        keywords = extract_keywords(content)
        breadcrumb_title = extract_h2_title(content)
        
        # Extract and clean blog content
        blog_content = extract_blog_content(content)
        if blog_content:
            blog_content = clean_blog_content(blog_content)
        else:
            blog_content = "<section class=\"blog\"><div class=\"container\"><article class=\"post-single\"></article></div></section>"
        
        # Build complete header
        header = f"""<!doctype html>
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
  <meta property="og:url" content="https://fsc-software.com/{os.path.basename(filepath)}">

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
      <h2>{title}</h2>
    </div>
  </section>

  {blog_content}

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

</html>"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(header)
        
        return True
    except Exception as e:
        print(f"❌ Error: {filepath} - {str(e)}")
        return False

def main():
    """Main sync function"""
    base_path = Path("/Users/mac/Documents/fsc/fsc-adrien.github.io")
    blog_files = sorted(base_path.glob("blog-*.html"))
    
    print(f"🔄 Syncing {len(blog_files)} blog files...\n")
    
    success_count = 0
    for i, blog_file in enumerate(blog_files, 1):
        if sync_blog_file(str(blog_file)):
            print(f"✅ [{i:2d}/{len(blog_files)}] {blog_file.name}")
            success_count += 1
        else:
            print(f"❌ [{i:2d}/{len(blog_files)}] {blog_file.name}")
    
    print(f"\n{'='*60}")
    print(f"✅ Successfully synced: {success_count}/{len(blog_files)} files")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
