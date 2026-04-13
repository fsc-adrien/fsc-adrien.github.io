#!/usr/bin/env python3
import os
import re
from pathlib import Path

os.chdir('/Users/mac/Documents/fsc/fsc-adrien.github.io')

def process_blog(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract metadata
    title_match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
    title = title_match.group(1) if title_match else "Blog"
    
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content, re.IGNORECASE)
    desc = desc_match.group(1) if desc_match else ""
    
    kw_match = re.search(r'<meta\s+name="keywords"\s+content="([^"]*)"', content, re.IGNORECASE)
    keywords = kw_match.group(1) if kw_match else ""
    
    # Extract blog section
    blog_match = re.search(r'<section\s+class="blog".*?</section>', content, re.IGNORECASE | re.DOTALL)
    if not blog_match:
        blog_match = re.search(r'<section\s+class="latest-news".*?</section>', content, re.IGNORECASE | re.DOTALL)
    
    blog_content = blog_match.group(0) if blog_match else "<section class=\"blog\"><div class=\"container\"></div></section>"
    
    # Clean blog content
    blog_content = blog_content.replace('class="latest-news"', 'class="blog"')
    blog_content = re.sub(r'<div\s+class="col-lg-4[^"]*"[^>]*>.*?</div>\s*</div>\s*</div>\s*</section>', '</section>', blog_content, flags=re.DOTALL | re.IGNORECASE)
    
    # Get H2 for breadcrumb
    h2_match = re.search(r'<h2[^>]*>([^<]+)</h2>', blog_content, re.IGNORECASE)
    breadcrumb_title = h2_match.group(1).strip()[:50] if h2_match else "Blog"
    
    # Build new file
    new_content = f'''<!doctype html>
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
        <li class="breadcrumb-item active" aria-current="page">{breadcrumb_title}</li>
      </ol>
      <h2>{title}</h2>
    </div>
  </section>

  {blog_content}

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
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)

blog_files = sorted(Path('.').glob('blog-*.html'))
print(f'Processing {len(blog_files)} files...')

for i, f in enumerate(blog_files, 1):
    try:
        process_blog(str(f))
        print(f'✅ [{i:2d}/{len(blog_files)}] {f.name}')
    except Exception as e:
        print(f'❌ [{i:2d}/{len(blog_files)}] {f.name}: {e}')

print(f'Done!')
