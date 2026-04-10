#!/usr/bin/env python3
"""
Comprehensive blog verification and health check
"""

import os
from pathlib import Path
from collections import defaultdict

def check_blog_file(file_path):
    """Check blog file structure and content"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    status = {
        'file': Path(file_path).name,
        'size_kb': len(content) / 1024,
        'line_count': len(content.splitlines()),
        'is_minified': len(content.splitlines()) <= 10,
    }
    
    # Check critical elements
    checks = {
        '✅ DOCTYPE': '<!doctype html>' in content.lower(),
        '✅ HTML5 tag': '<html lang="en">' in content,
        '✅ Head section': '<head>' in content,
        '✅ Meta charset': 'charset="utf-8"' in content,
        '✅ Viewport meta': 'viewport' in content,
        '✅ Title tag': '<title>' in content and '</title>' in content,
        '✅ OG tags': 'og:title' in content,
        '✅ Twitter tags': 'twitter:card' in content,
        '✅ Canonical URL': 'rel="canonical"' in content,
        '✅ Favicons': 'favicon_fsc' in content,
        '✅ All 9 CSS files': (
            'animate.min.css' in content and
            'font-awesome.min.css' in content and
            'flipbox.min.css' in content and
            'timeline.css' in content and
            'odometer.min.css' in content and
            'fancybox.min.css' in content and
            'swiper.min.css' in content and
            'bootstrap.min.css' in content and
            'style.css' in content
        ),
        '✅ Header section': '<header class="header">' in content,
        '✅ Page header': '<section class="page-header">' in content,
        '✅ Blog section': '<section class="blog">' in content,
        '✅ Article tag': '<article class="post-single">' in content,
        '✅ Post meta': '<div class="post-meta">' in content,
        '✅ Post content': '<div class="post-content">' in content,
        '✅ Post date icon': 'fa-calendar' in content,
        '✅ Post author icon': 'fa-user' in content,
        '✅ Footer section': '<footer class="footer">' in content,
        '✅ Contact boxes': content.count('<div class="contact-box">') >= 3,
        '✅ Sub-footer': '<div class="sub-footer">' in content,
        '✅ Closing tags': '</html>' in content,
    }
    
    status['checks'] = {}
    for check_name, result in checks.items():
        status['checks'][check_name] = '✅ PASS' if result else '❌ FAIL'
        if not result:
            issues.append(check_name.replace('✅ ', ''))
    
    status['issues'] = issues
    status['all_pass'] = len(issues) == 0
    
    return status

def main():
    base_dir = Path('/Users/mac/Documents/fsc/fsc-adrien.github.io')
    blog_files = sorted(base_dir.glob('blog-*.html'))
    
    print("="*80)
    print("📊 COMPREHENSIVE BLOG VERIFICATION REPORT")
    print("="*80)
    print(f"Total blog files found: {len(blog_files)}\n")
    
    all_results = []
    stats = {
        'total': len(blog_files),
        'passed': 0,
        'minified': 0,
        'issues': defaultdict(int),
    }
    
    for file in blog_files:
        result = check_blog_file(str(file))
        all_results.append(result)
        
        if result['all_pass']:
            stats['passed'] += 1
            print(f"✅ {result['file']:40} | {result['size_kb']:6.1f} KB | {result['line_count']:3} lines")
        else:
            status_icon = "⚠️ " if result['is_minified'] else "❌"
            print(f"{status_icon} {result['file']:40} | Issues: {len(result['issues'])}")
            for issue in result['issues']:
                stats['issues'][issue] += 1
        
        if result['is_minified']:
            stats['minified'] += 1
    
    print("\n" + "="*80)
    print("📈 SUMMARY STATISTICS")
    print("="*80)
    print(f"✅ Files with all checks passing: {stats['passed']}/{stats['total']}")
    print(f"⚠️  Minified files: {stats['minified']}/{stats['total']}")
    print(f"📊 Average file size: {sum(r['size_kb'] for r in all_results)/len(all_results):.1f} KB")
    
    if stats['issues']:
        print("\n⚠️  Issues found:")
        for issue, count in sorted(stats['issues'].items(), key=lambda x: -x[1]):
            print(f"  - {issue}: {count} files")
    else:
        print("\n✅ NO ISSUES FOUND - All blogs standardized!")
    
    print("\n" + "="*80)
    print("📋 DETAILED CHECK SUMMARY")
    print("="*80)
    
    # Show what passed/failed per check
    all_checks = set()
    for result in all_results:
        all_checks.update(result['checks'].keys())
    
    check_results = defaultdict(lambda: {'pass': 0, 'fail': 0})
    for result in all_results:
        for check, status in result['checks'].items():
            if 'PASS' in status:
                check_results[check]['pass'] += 1
            else:
                check_results[check]['fail'] += 1
    
    for check in sorted(check_results.keys()):
        result = check_results[check]
        if result['fail'] == 0:
            print(f"✅ {check:40} | {result['pass']}/{stats['total']} passed")
        else:
            print(f"❌ {check:40} | {result['pass']}/{stats['total']} passed, {result['fail']} FAILED")

if __name__ == '__main__':
    main()
