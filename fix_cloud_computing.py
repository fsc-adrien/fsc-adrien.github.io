#!/usr/bin/env python3
"""Fix blog-cloud-computing.html by restoring content from git."""
import re, subprocess, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    git_result = subprocess.run(
        ['git', 'show', 'b02ca86:blog-cloud-computing.html'],
        capture_output=True, text=True, cwd=BASE_DIR
    )
    git_html = git_result.stdout

    # Extract post-body content (between <div class="post-body"> and the closing </div> before post-footer)
    m = re.search(r'<div[^>]*class="post-body"[^>]*>(.*?)</div>\s*\n\s*<div class="post-footer"', git_html, re.DOTALL)
    if not m:
        print('ERROR: could not find post-body in git version')
        return
    content = m.group(1).strip()

    # Extract tags
    tags_links = re.findall(r'<a href="blogs\.html">[^<]*</a>', git_html)
    tags_html = '\n'.join(f'          {t}' for t in tags_links) if tags_links else '          <a href="blogs.html">Cloud</a>'

    # Read current file
    filepath = os.path.join(BASE_DIR, 'blog-cloud-computing.html')
    with open(filepath, 'r', encoding='utf-8') as f:
        cur = f.read()

    # Replace post-content
    cur = re.sub(
        r'(<div[^>]*class="post-content"[^>]*>).*?(</div>)',
        lambda m2: m2.group(1) + '\n' + content + '\n        ' + m2.group(2),
        cur, count=1, flags=re.DOTALL
    )

    # Replace post-tags
    cur = re.sub(
        r'(<div[^>]*class="post-tags"[^>]*>).*?(</div>)',
        lambda m2: m2.group(1) + '\n' + tags_html + '\n        ' + m2.group(2),
        cur, count=1, flags=re.DOTALL
    )

    # Fix description
    cur = re.sub(
        r'(<meta\s+name="description"\s+content=").*?(")',
        r'\1Discover the latest developments in cloud infrastructure, multi-cloud strategies, and how enterprises are leveraging cloud technology for competitive advantage.\2',
        cur, count=1
    )

    # Fix keywords
    cur = re.sub(
        r'(<meta\s+name="keywords"\s+content=").*?(")',
        r'\1cloud computing, AWS, Azure, multi-cloud, scalability, cloud security\2',
        cur, count=1
    )

    # Fix og:description
    cur = re.sub(
        r'(<meta\s+property="og:description"\s+content=").*?(")',
        r'\1Discover the latest developments in cloud infrastructure, multi-cloud strategies, and enterprise cloud technology.\2',
        cur, count=1
    )

    # Fix post date
    cur = re.sub(
        r'(<span[^>]*class="post-date"[^>]*><i[^>]*></i>\s*)([^<]+)(</span>)',
        r'\1April 8, 2026\3',
        cur, count=1
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cur)

    print(f'Done! Content restored ({len(content)} chars)')

if __name__ == '__main__':
    main()
