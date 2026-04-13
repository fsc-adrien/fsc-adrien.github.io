#!/usr/bin/env python3
"""
Batch fix remaining blog HTML files by standardizing structure and prettifying minified files
"""

from pathlib import Path
import re

# Standard HTML template
STANDARD_TEMPLATE = '''<!doctype html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>{title}</title>
  <meta name="author" content="FSCSoftware">
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="https://fsc-software.com/ico/preview.png">
  <meta property="og:site_name" content="FSC Software Blog">
  <meta property="og:title" content="{title}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://fsc-software.com/{filename}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@fsc-software">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
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
        <li class="breadcrumb-item active" aria-current="page">{breadcrumb}</li>
      </ol>
      <h2>{title}</h2>
    </div>
  </section>

  <section class="blog">
    <div class="container">
      <article class="post-single">
        <div class="post-meta">
          <span>{date}</span>
          <span>FSC Software Team</span>
        </div>

        <div class="post-content">
{content}
        </div>
      </article>
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


def extract_title(content):
    """Extract title from <title> tag"""
    match = re.search(r'<title>([^<]+)</title>', content)
    return match.group(1) if match else "Blog Post"


def extract_description(content):
    """Extract description from meta tag or content"""
    match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content)
    if match:
        return match.group(1)
    # Fallback to first paragraph
    match = re.search(r'<p>([^<]{50,150})', content)
    return match.group(1) if match else "Blog post"


def extract_keywords(content):
    """Extract keywords from meta tag"""
    match = re.search(r'<meta\s+name="keywords"\s+content="([^"]+)"', content)
    return match.group(1) if match else "blog, post"


def extract_breadcrumb(title):
    """Extract breadcrumb title from main title (max 40 chars)"""
    return title[:40] if len(title) > 40 else title


def extract_date(content):
    """Extract date from content"""
    patterns = [
        r'<span>([A-Z][a-z]+ \d+, \d{4})',
        r'<span>\s*([A-Z][a-z]+\s+\d+,\s+\d{4})',
    ]
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1)
    return "January 1, 2024"


def extract_content(content):
    """Extract blog content from various section types"""
    # Try .blog section
    match = re.search(r'<section\s+class="blog">.*?<div\s+class="post-content">(.*?)</div>\s*</article>', content, re.DOTALL)
    if match:
        text = match.group(1)
    else:
        # Try .latest-news or article
        match = re.search(r'<div\s+class="post-content">(.*?)</div>\s*</article>', content, re.DOTALL)
        text = match.group(1) if match else "<p>Content</p>"
    
    # Clean up content: remove sidebar references
    text = re.sub(r'<div\s+class="col-lg-4"[^>]*>.*?</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<aside[^>]*>.*?</aside>', '', text, flags=re.DOTALL)
    
    # Remove icon spans from post-meta
    text = re.sub(r'<span><i\s+class="fa[^>]*></i>\s*', '<span>', text)
    
    # Clean up post-tags
    text = re.sub(r'<a\s+href="[^"]*"\s*>#([^<]+)</a>', r'<a href="blogs.html">\1</a>', text)
    
    return text.strip()


def prettify_html(content):
    """Add newlines to minified HTML"""
    # Split on >< boundaries but preserve the tags
    content = re.sub(r'>\s*<', '>\n<', content)
    return content


def fix_blog_file(filepath):
    """Fix individual blog file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Detect minified (very few newlines)
        if content.count('\n') < 50:
            content = prettify_html(content)
        
        # Extract metadata
        title = extract_title(content)
        description = extract_description(content)
        keywords = extract_keywords(content)
        breadcrumb = extract_breadcrumb(title)
        date = extract_date(content)
        blog_content = extract_content(content)
        filename = filepath.name
        
        # Build new HTML
        new_html = STANDARD_TEMPLATE.format(
            title=title,
            description=description,
            keywords=keywords,
            breadcrumb=breadcrumb,
            date=date,
            content=blog_content,
            filename=filename
        )
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        return True
    except Exception as e:
        print(f"❌ Error in {filepath.name}: {e}")
        return False


def main():
    """Main function"""
    blog_files = sorted(Path('.').glob('blog-*.html'))
    fixed = 0
    failed = 0
    
    print(f"Processing {len(blog_files)} blog files...")
    
    # Skip already fixed files
    skip_files = {
        'blog-ar-vr.html', 'blog-5g-technology.html', 'blog-ruby-rails.html',
        'blog-csharp-dotnet.html', 'blog-lowcode-nocode.html',
        'blog-cloud-computing.html', 'blog-ai-revolution.html',
        'blog-cybersecurity.html', 'blog-devops.html', 'blog-microservices.html',
        'blog-devops-new.html', 'blog-cloud-computing-new.html',
        'blog-microservices-new.html', 'blog-iot-edge.html',
        'blog-quantum-computing.html', 'blog-machine-learning.html'
    }
    
    for filepath in blog_files:
        if filepath.name in skip_files:
            print(f"⊘  Skipping {filepath.name} (already fixed)")
            continue
        
        if fix_blog_file(filepath):
            fixed += 1
            print(f"✅ Fixed {filepath.name}")
        else:
            failed += 1
    
    print(f"\n📊 Summary: {fixed} fixed, {failed} failed, {len(skip_files)} skipped")


if __name__ == '__main__':
    main()
