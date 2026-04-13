#!/usr/bin/env python3
"""
restore_content_from_git.py
Restores post-content (and improved meta) from git commit b02ca86
into the current standardized blog files.
"""

import os
import re
import subprocess
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GIT_COMMIT = 'b02ca86'

def git_show(commit, filename):
    result = subprocess.run(
        ['git', 'show', f'{commit}:{filename}'],
        capture_output=True, text=True, cwd=BASE_DIR
    )
    return result.stdout if result.returncode == 0 else None

def extract_between(html, start_tag_pattern, end_tag):
    """Extract innerHTML between a start tag (regex) and end tag string."""
    m = re.search(start_tag_pattern, html, re.DOTALL | re.IGNORECASE)
    if not m:
        return None
    start_pos = m.end()
    end_pos = html.find(end_tag, start_pos)
    if end_pos == -1:
        return None
    return html[start_pos:end_pos].strip()

def extract_post_content(html):
    """Extract innerHTML of .post-content div."""
    return extract_between(html, r'<div[^>]*class=["\'][^"\']*post-content[^"\']*["\'][^>]*>', '</div>')

def extract_meta(html, name):
    m = re.search(rf'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
    return m.group(1) if m else ''

def extract_og(html, prop):
    m = re.search(rf'<meta\s+property=["\']og:{prop}["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE | re.DOTALL)
    return m.group(1) if m else ''

def extract_twitter(html, name):
    m = re.search(rf'<meta\s+name=["\']twitter:{name}["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE | re.DOTALL)
    return m.group(1) if m else ''

def extract_keywords(html):
    m = re.search(r'<meta\s+name=["\']keywords["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
    return m.group(1) if m else ''

def extract_post_tags(html):
    m = re.search(r'<div[^>]*class=["\'][^"\']*post-tags[^"\']*["\'][^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
    if not m:
        return None
    inner = m.group(1).strip()
    links = re.findall(r'<a[^>]*>.*?</a>', inner, re.DOTALL)
    return '\n'.join(f'          {l}' for l in links) if links else None

def extract_post_date(html):
    m = re.search(r'<span[^>]*class=["\'][^"\']*post-date[^"\']*["\'][^>]*>(.*?)</span>', html, re.DOTALL | re.IGNORECASE)
    if m:
        text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if text:
            return text
    return None

def extract_post_author(html):
    m = re.search(r'<span[^>]*class=["\'][^"\']*post-author[^"\']*["\'][^>]*>(.*?)</span>', html, re.DOTALL | re.IGNORECASE)
    if m:
        text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if text:
            return text
    return None

def main():
    files = sorted(glob.glob(os.path.join(BASE_DIR, 'blog-*.html')))
    files = [f for f in files if os.path.basename(f) != 'blogs.html']

    success = 0
    skipped = 0
    failed = []

    for filepath in files:
        filename = os.path.basename(filepath)

        # Get git version of this file
        git_html = git_show(GIT_COMMIT, filename)
        if not git_html:
            print(f'⏭️  {filename}: not in git commit, skipping')
            skipped += 1
            continue

        # Extract content from git version
        git_content = extract_post_content(git_html)
        if not git_content or 'Content not found' in git_content or 'Content coming soon' in git_content:
            print(f'⚠️  {filename}: git version also has no real content')
            skipped += 1
            continue

        # Read current file
        with open(filepath, 'r', encoding='utf-8') as fh:
            current_html = fh.read()

        # Check if current file also has no content (needs update)
        current_content = extract_post_content(current_html)
        if current_content and 'Content not found' not in current_content and 'Content coming soon' not in current_content:
            print(f'✅ {filename}: already has real content, skipping')
            skipped += 1
            continue

        updated = current_html

        # 1. Replace post-content
        updated = re.sub(
            r'(<div[^>]*class=["\'][^"\']*post-content[^"\']*["\'][^>]*>).*?(</div>)',
            lambda m: m.group(1) + '\n' + git_content + '\n        ' + m.group(2),
            updated,
            count=1,
            flags=re.DOTALL | re.IGNORECASE
        )

        # 2. Restore better meta description from git (if current is generic)
        current_desc_m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', updated, re.IGNORECASE)
        current_desc = current_desc_m.group(1) if current_desc_m else ''
        if current_desc in ('Read our latest blog post about technology, software development, and digital solutions.',
                             'Read our latest tech blog post', ''):
            git_desc = extract_meta(git_html, 'description')
            if git_desc:
                updated = re.sub(
                    r'(<meta\s+name=["\']description["\']\s+content=["\']).*?(["\'])',
                    lambda m: m.group(1) + git_desc + m.group(2),
                    updated, count=1, flags=re.IGNORECASE
                )

        # 3. Restore keywords from git if generic
        current_kw_m = re.search(r'<meta\s+name=["\']keywords["\']\s+content=["\'](.*?)["\']', updated, re.IGNORECASE)
        current_kw = current_kw_m.group(1) if current_kw_m else ''
        if current_kw in ('blog, technology, software', ''):
            git_kw = extract_keywords(git_html)
            if git_kw:
                updated = re.sub(
                    r'(<meta\s+name=["\']keywords["\']\s+content=["\']).*?(["\'])',
                    lambda m: m.group(1) + git_kw + m.group(2),
                    updated, count=1, flags=re.IGNORECASE
                )

        # 4. Restore og:description if generic
        current_og_desc_m = re.search(r'(<meta\s+property=["\']og:description["\']\s+content=["\']).*?(["\'])', updated, re.IGNORECASE)
        if current_og_desc_m:
            cval = current_og_desc_m.group(0)
            if 'Read our latest' in cval or 'tech blog post' in cval:
                git_og_desc = extract_og(git_html, 'description')
                if git_og_desc:
                    updated = re.sub(
                        r'(<meta\s+property=["\']og:description["\']\s+content=["\']).*?(["\'])',
                        lambda m: m.group(1) + git_og_desc + m.group(2),
                        updated, count=1, flags=re.IGNORECASE
                    )

        # 5. Restore post tags from git if better
        git_tags = extract_post_tags(git_html)
        if git_tags:
            current_tags_m = re.search(r'<div[^>]*class=["\'][^"\']*post-tags[^"\']*["\'][^>]*>(.*?)</div>', updated, re.DOTALL | re.IGNORECASE)
            if current_tags_m:
                updated = updated[:current_tags_m.start(1)] + '\n' + git_tags + '\n        ' + updated[current_tags_m.end(1):]

        # 6. Restore post date from git if better
        git_date = extract_post_date(git_html)
        if git_date:
            updated = re.sub(
                r'(<span[^>]*class=["\'][^"\']*post-date[^"\']*["\'][^>]*><i[^>]*></i>\s*)([^<]+)(</span>)',
                lambda m: m.group(1) + git_date + m.group(3),
                updated, count=1, flags=re.IGNORECASE
            )

        # Write back
        with open(filepath, 'w', encoding='utf-8') as fh:
            fh.write(updated)

        content_preview = git_content[:80].replace('\n', ' ')
        print(f'✅ {filename}: content restored ({len(git_content)} chars)')
        success += 1

    print(f'\n{"="*60}')
    print(f'Done: {success} restored, {skipped} skipped/already OK, {len(failed)} failed')
    if failed:
        print('Failed:', failed)

if __name__ == '__main__':
    main()
