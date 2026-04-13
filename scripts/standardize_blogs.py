#!/usr/bin/env python3
"""
standardize_blogs.py
Standardizes all blog-*.html files:
- Keeps: title, meta description/keywords, og/twitter tags, canonical, post-meta, post-content, post-tags
- Replaces: header, footer, CSS list, JS list with correct/complete versions
"""

import os
import re
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def extract_tag(html, pattern):
    m = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
    return m.group(0) if m else ''

def extract_group(html, pattern, group=1):
    m = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
    return m.group(group).strip() if m else ''

# ─────────────────────────────────────────────
# BUILD FINAL HTML
# ─────────────────────────────────────────────

def build_html(title, description, keywords, og_title, og_url, og_description,
               tw_title, tw_description, canonical,
               page_header_title, breadcrumb_last,
               post_date, post_author, post_category,
               post_content_html, post_tags_html):

    return f"""<!doctype html>
<html lang="en">

<head>
  <!-- META TAGS -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>{title}</title>
  <meta name="author" content="FSCSoftware">
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">

  <!-- OPEN GRAPH / SOCIAL MEDIA META -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{og_description}">
  <meta property="og:image" content="https://fsc-software.com/ico/preview.png">
  <meta property="og:site_name" content="FSC Software Blog">
  <meta property="og:url" content="{og_url}">

  <!-- TWITTER CARD META -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@fsc-software">
  <meta name="twitter:title" content="{tw_title}">
  <meta name="twitter:description" content="{tw_description}">
  <meta name="twitter:image" content="https://fsc-software.com/ico/preview.png">

  <!-- CANONICAL URL -->
  <link rel="canonical" href="{canonical}">

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
  <!-- SEARCH BOX OVERLAY -->
  <div class="search-box">
    <div class="close-btn"><span></span><span></span></div>
    <form>
      <input type="search" placeholder="Type here to search...">
      <h6>Type above and press enter or press close to cancel.</h6>
    </form>
  </div>

  <!-- SANDWICH MENU (Mobile Navigation) -->
  <aside class="sandwich-menu">
    <div class="overlay"></div>
    <div class="logo"><img src="images/LOGO_FSC-17.png" alt="FSC Software Logo"></div>

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

  <!-- MAIN HEADER -->
  <header class="header">
    <!-- TOP BAR -->
    <div class="topbar">
      <div class="container">
        <div class="tagline">Your Trusted IT Outsourcing Partner for Seamless Solutions</div>
        <ul class="social-media">
          <li><a target="_blank" href="https://www.facebook.com/fscsoftwareglobal"><i class="fa fa-facebook"></i></a></li>
          <li><a target="_blank" href="https://www.instagram.com/fscsoftwarevn"><i class="fa fa-instagram"></i></a></li>
          <li><a target="_blank" href="https://www.linkedin.com/company/fsc-software"><i class="fa fa-linkedin"></i></a></li>
          <li><a href="mailto:sales@fsc-software.com"><i class="fa fa-google-plus"></i></a></li>
        </ul>
        <div class="phone"><a href="tel:+84969005169"><img src="images/icon-phone.png" alt="Phone icon"> <span>+(84) 969 005 169</span></a></div>
      </div>
    </div>

    <!-- NAVIGATION BAR -->
    <nav class="navbar">
      <div class="container">
        <div class="logo"><a href="/"><img src="images/LOGO_FSC-01.png" alt="FSC Software"></a></div>

        <ul class="nav-menu">
          <li><a href="/">Home</a></li>
          <li><a href="about-us.html">About Us</a></li>
          <li><a href="blogs.html">Blogs</a></li>
          <li><a href="career.html">Careers</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>

        <div class="search-btn"><i class="fa fa-search"></i></div>
        <div class="sandwich-btn"><span></span><span></span><span></span></div>
        <div class="bottom-bar"></div>
      </div>
    </nav>
  </header>

  <!-- PAGE HEADER / BREADCRUMB -->
  <section class="page-header">
    <div class="container">
      <a href="javascript:window.print()" class="print">PRINT PAGE <img src="images/icon-print.png" alt="Print"></a>
      <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/">Home</a></li>
        <li class="breadcrumb-item"><a href="blogs.html">Blog</a></li>
        <li class="breadcrumb-item active" aria-current="page">{breadcrumb_last}</li>
      </ol>
      <h1>{page_header_title}</h1>
    </div>
  </section>

  <!-- BLOG CONTENT -->
  <section class="blog">
    <div class="container">
      <article class="post-single">

        <!-- POST METADATA -->
        <div class="post-meta">
          <span class="post-date"><i class="fa fa-calendar"></i> {post_date}</span>
          <span class="post-author"><i class="fa fa-user"></i> {post_author}</span>
          <span class="post-category"><i class="fa fa-tag"></i> {post_category}</span>
        </div>

        <!-- POST CONTENT -->
        <div class="post-content">
{post_content_html}
        </div>

        <!-- POST TAGS -->
        <div class="post-tags">
{post_tags_html}
        </div>

      </article>
    </div>
  </section>

  <!-- FOOTER -->
  <footer class="footer">
    <div class="contact-wrapper">
      <div class="container">
        <div class="content-box">
          <img src="images/footer-icon03.png" alt="Address icon">
          <h3>address infos</h3>
          <p>12th Floor, 111 Y Lan Street, Phu Thi Ward, Gia Lam District, Ha Noi City, Viet Nam</p>
        </div>
        <div class="content-box">
          <img src="images/footer-icon02.png" alt="Working hours icon">
          <h3>working hours</h3>
          <p>Monday to Friday 09:00 to 18:30 and Saturday we work until 15:30</p>
        </div>
        <div class="content-box">
          <img src="images/footer-icon01.png" alt="Support center icon">
          <h3>support center</h3>
          <p>FSC Software is your trusted call service that you can <a href="tel:+84969005169">call</a> or <a href="mailto:sales@fsc-software.com">e-mail</a> us anytime</p>
        </div>
      </div>
    </div>

    <div class="content-wrapper">
      <div class="container">
        <div class="row">
          <div class="col-lg-4">
            <a href="/"><img src="images/LOGO_FSC-17.png" alt="FSC Software Logo" class="logo"></a>
            <p>Let's construct your digital transformation with<br>FSC Software!</p>
          </div>
          <div class="col-lg-2 col-md-6">
            <ul class="footer-menu">
              <li><a href="/">Home</a></li>
              <li><a href="about-us.html">About Us</a></li>
              <li><a href="services.html">Services</a></li>
            </ul>
          </div>
          <div class="col-lg-2 col-md-6">
            <ul class="footer-menu">
              <li><a href="contact.html">Contact</a></li>
              <li><a href="career.html">Careers</a></li>
            </ul>
          </div>
          <div class="col-lg-4">
            <div class="contact-box">
              <h3>CALL US</h3><br>
              <h4><a href="tel:+84969005169">+84 969 005 169</a></h4>
              <h4><a href="mailto:sales@fsc-software.com">sales@fsc-software.com</a></h4>
              <ul>
                <li><a target="_blank" href="https://www.facebook.com/fscsoftwareglobal"><i class="fa fa-facebook"></i></a></li>
                <li><a target="_blank" href="https://www.instagram.com/fscsoftwarevn"><i class="fa fa-instagram"></i></a></li>
                <li><a target="_blank" href="https://www.linkedin.com/company/fsc-software"><i class="fa fa-linkedin"></i></a></li>
                <li><a href="mailto:sales@fsc-software.com"><i class="fa fa-google-plus"></i></a></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="sub-footer">
      <div class="container">
        <span class="copyright">© 2023 FSC Software - All rights reserved</span>
      </div>
    </div>
  </footer>

  <!-- SCROLL UP BUTTON -->
  <a href="#" class="scrollup"><i class="fa fa-long-arrow-up" aria-hidden="true"></i></a>

  <!-- JAVASCRIPT FILES -->
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
"""

# ─────────────────────────────────────────────
# EXTRACT FIELDS FROM EXISTING HTML
# ─────────────────────────────────────────────

def extract_fields(html, filename):
    slug = filename.replace('.html', '')

    # Title
    title = extract_group(html, r'<title>([^<]+)</title>')
    if not title:
        title = slug.replace('-', ' ').title() + ' - FSC Software Blog'

    # Meta description
    description = extract_group(html, r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']')
    if not description:
        description = f'Read our latest blog post about {slug.replace("blog-", "").replace("-", " ")} on FSC Software.'

    # Meta keywords
    keywords = extract_group(html, r'<meta\s+name=["\']keywords["\']\s+content=["\'](.*?)["\']')
    if not keywords:
        keywords = slug.replace('blog-', '').replace('-', ', ')

    # OG tags
    og_title = extract_group(html, r'<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']')
    if not og_title:
        og_title = title

    og_url = extract_group(html, r'<meta\s+property=["\']og:url["\']\s+content=["\'](.*?)["\']')
    if not og_url:
        og_url = f'https://fsc-software.com/{filename}'

    og_desc = extract_group(html, r'<meta\s+property=["\']og:description["\']\s+content=["\'](.*?)["\']')
    if not og_desc:
        og_desc = description

    # Twitter tags
    tw_title = extract_group(html, r'<meta\s+name=["\']twitter:title["\']\s+content=["\'](.*?)["\']')
    if not tw_title:
        tw_title = og_title

    tw_desc = extract_group(html, r'<meta\s+name=["\']twitter:description["\']\s+content=["\'](.*?)["\']')
    if not tw_desc:
        tw_desc = og_desc

    # Canonical
    canonical = extract_group(html, r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']')
    if not canonical:
        canonical = f'https://fsc-software.com/{filename}'

    # Page header h1/h2
    page_h = extract_group(html, r'<section[^>]*class=["\'][^"\']*page-header[^"\']*["\'][^>]*>.*?<h[12][^>]*>([^<]+)</h[12]>', 1)
    if not page_h:
        page_h = title.replace(' - FSC Software Blog', '').replace(' | FSC Software Blog', '')

    # Breadcrumb last item
    breadcrumb_last = extract_group(html, r'<li[^>]*class=["\'][^"\']*active[^"\']*["\'][^>]*[^>]*>\s*(?:<[^>]+>)?\s*([^<]+?)\s*(?:</[^>]+>)?\s*</li>')
    if not breadcrumb_last:
        # Fallback: use first word(s) of page title
        breadcrumb_last = page_h.split(':')[0].strip()

    # Post date
    post_date = extract_group(html, r'<span[^>]*class=["\'][^"\']*post-date[^"\']*["\'][^>]*>(?:<[^>]+>)?\s*([^<]+?)\s*(?:</[^>]+>)?\s*</span>')
    if not post_date or 'calendar' in post_date.lower():
        post_date = 'January 1, 2024'

    # Post author
    post_author = extract_group(html, r'<span[^>]*class=["\'][^"\']*post-author[^"\']*["\'][^>]*>(?:<[^>]+>)?\s*([^<]+?)\s*(?:</[^>]+>)?\s*</span>')
    if not post_author or 'user' in post_author.lower() or not post_author.strip():
        post_author = 'FSC Software Team'

    # Post category
    post_category = extract_group(html, r'<span[^>]*class=["\'][^"\']*post-category[^"\']*["\'][^>]*>(?:<[^>]+>)?\s*([^<]+?)\s*(?:</[^>]+>)?\s*</span>')
    if not post_category or 'tag' in post_category.lower():
        post_category = 'Technology'

    # Post content (inner HTML of .post-content)
    post_content = extract_group(html, r'<div[^>]*class=["\'][^"\']*post-content[^"\']*["\'][^>]*>(.*?)</div>\s*(?:<!--[^>]*-->)?\s*(?:<div[^>]*class=["\'][^"\']*post-tags)', 1)
    if not post_content:
        post_content = extract_group(html, r'<div[^>]*class=["\'][^"\']*post-content[^"\']*["\'][^>]*>(.*?)</div>', 1)
    post_content = post_content.strip() if post_content else '<p>Content coming soon.</p>'

    # Clean up "Content not found" placeholder
    if post_content.strip() == '<p>Content not found</p>' or post_content.strip() == '<p>Content not found.</p>':
        post_content = '<p>Content coming soon. Please check back later.</p>'

    # Post tags
    post_tags_match = re.search(
        r'<div[^>]*class=["\'][^"\']*post-tags[^"\']*["\'][^>]*>(.*?)</div>',
        html, re.DOTALL | re.IGNORECASE
    )
    if post_tags_match:
        inner = post_tags_match.group(1).strip()
        # Normalize links
        links = re.findall(r'<a[^>]*>[^<]*</a>', inner)
        post_tags_html = '\n'.join(f'          {l}' for l in links)
    else:
        tag_word = slug.replace('blog-', '').replace('-', ' ').title()
        post_tags_html = f'          <a href="blogs.html">{tag_word}</a>'

    return {
        'title': title,
        'description': description,
        'keywords': keywords,
        'og_title': og_title,
        'og_url': og_url,
        'og_description': og_desc,
        'tw_title': tw_title,
        'tw_description': tw_desc,
        'canonical': canonical,
        'page_header_title': page_h,
        'breadcrumb_last': breadcrumb_last,
        'post_date': post_date,
        'post_author': post_author,
        'post_category': post_category,
        'post_content_html': post_content,
        'post_tags_html': post_tags_html,
    }

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    files = sorted(glob.glob(os.path.join(BASE_DIR, 'blog-*.html')))
    # Exclude blogs.html listing page
    files = [f for f in files if os.path.basename(f) != 'blogs.html']

    success = 0
    failed = []

    for filepath in files:
        filename = os.path.basename(filepath)
        try:
            with open(filepath, 'r', encoding='utf-8') as fh:
                html = fh.read()

            fields = extract_fields(html, filename)
            new_html = build_html(**fields)

            with open(filepath, 'w', encoding='utf-8') as fh:
                fh.write(new_html)

            content_preview = fields['post_content_html'][:60].replace('\n', ' ')
            print(f'✅ {filename} | {fields["title"][:55]}...')
            success += 1

        except Exception as e:
            print(f'❌ {filename}: {e}')
            failed.append(filename)

    print(f'\n{"="*60}')
    print(f'Done: {success} success, {len(failed)} failed')
    if failed:
        print('Failed files:', failed)

if __name__ == '__main__':
    main()
