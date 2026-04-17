# FSC Blog Template System - Deployment Checklist

## ✅ Pre-Deployment Checklist

### System Preparation
- [ ] Python 3 installed and working
  ```bash
  python3 --version  # Should show version 3.x
  ```
- [ ] All template files exist in `templates/` directory
  ```bash
  ls -la templates/  # Should list 5 .hbs files
  ```
- [ ] All 78 blog files present
  ```bash
  ls blog-*.html | wc -l  # Should show 78
  ```
- [ ] Build script is executable
  ```bash
  ls -la build_blogs_final.py  # Should exist
  ```
- [ ] Git repository is clean (optional but recommended)
  ```bash
  git status  # Should be clean before backup
  ```

### Documentation Review
- [ ] Read QUICK_START.md
- [ ] Understood customization process
- [ ] Identified any needed customizations
- [ ] Noted contact information (if to be updated in footer)
- [ ] Listed any new scripts to be added

### Backup & Version Control
- [ ] Created backup directory
  ```bash
  mkdir -p ../fsc-adrien-backup-$(date +%Y%m%d)
  cp -r . ../fsc-adrien-backup-$(date +%Y%m%d)/
  ```
- [ ] Created git backup branch (optional)
  ```bash
  git checkout -b backup/pre-template-system
  git push origin backup/pre-template-system
  ```
- [ ] Committed current state
  ```bash
  git add .
  git commit -m "Backup before template system deployment"
  ```

---

## 🔨 Build & Test Phase

### Run Build Script
- [ ] Navigate to project directory
  ```bash
  cd /Users/mac/Documents/fsc/fsc-adrien.github.io
  ```
- [ ] Run build script
  ```bash
  python3 build_blogs_final.py
  ```
- [ ] Verify success
  - [ ] Build completed without errors
  - [ ] Summary shows "✅ Success: 78 files"
  - [ ] No "❌ Failures" reported
- [ ] If errors occur
  - [ ] Run with verbose output: `python3 build_blogs_final.py 2>&1 | head -100`
  - [ ] Check template files for syntax errors
  - [ ] Review QUICK_START.md troubleshooting section

### File Verification
- [ ] All 78 blog files still exist
  ```bash
  ls blog-*.html | wc -l  # Should be 78
  ```
- [ ] File sizes are reasonable (2-5KB)
  ```bash
  ls -lh blog-*.html | head -5  # Check sizes
  ```
- [ ] No backup or temporary files created
  ```bash
  ls *.bak *.tmp 2>/dev/null | wc -l  # Should be 0
  ```

### Content Verification (Spot Check 5 Files)
For each file (e.g., blog-ai-revolution.html, blog-ar-vr.html, etc.):

- [ ] **File Loads Correctly**
  - [ ] Open in browser: `open blog-ai-revolution.html`
  - [ ] Page loads without errors
  - [ ] No console errors (F12 → Console)

- [ ] **Structure Correct**
  - [ ] Header displays at top
  - [ ] Navigation menu visible
  - [ ] Page content shows
  - [ ] Footer displays at bottom

- [ ] **Navigation Works**
  - [ ] Click "Home" button → navigates
  - [ ] Click logo → navigates
  - [ ] Mobile menu opens on mobile view
  - [ ] Breadcrumb navigation present

- [ ] **Content Proper**
  - [ ] Article title displays as H1
  - [ ] Post content shows correctly
  - [ ] Post metadata (date, author) visible
  - [ ] Post tags displayed

- [ ] **Styling Applied**
  - [ ] CSS styles applied (not bare HTML)
  - [ ] Colors correct
  - [ ] Fonts display properly
  - [ ] Layout looks professional

### SEO Verification (Spot Check 3 Files)
For each file, right-click → "View Page Source" and check:

- [ ] **Meta Tags Present**
  ```html
  <meta name="description" content="...">
  <meta name="keywords" content="...">
  ```

- [ ] **Canonical URL**
  ```html
  <link rel="canonical" href="https://fsc-software.com/blog-ai-revolution.html">
  ```

- [ ] **Open Graph Tags**
  ```html
  <meta property="og:type" content="article">
  <meta property="og:title" content="...">
  <meta property="og:description" content="...">
  ```

- [ ] **Twitter Card Tags**
  ```html
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="...">
  ```

- [ ] **Title Tag**
  ```html
  <title>... - FSC Software Blog</title>
  ```

### Responsive Design Test (3 Files)
For each file:

- [ ] **Desktop View**
  - [ ] Open in browser
  - [ ] Content width appropriate
  - [ ] All elements visible
  - [ ] No horizontal scrolling

- [ ] **Tablet View**
  - [ ] Press F12 for DevTools
  - [ ] Select tablet size (iPad)
  - [ ] Content responsive
  - [ ] Menu accessible

- [ ] **Mobile View**
  - [ ] Press F12 for DevTools
  - [ ] Select mobile size (iPhone)
  - [ ] Navigation hamburger menu visible
  - [ ] Click menu → opens/closes
  - [ ] Content readable without scrolling
  - [ ] All elements fit on screen

### Performance Check
- [ ] Open DevTools (F12)
- [ ] Go to "Network" tab
- [ ] Refresh page
- [ ] Check:
  - [ ] All CSS files load (green status)
  - [ ] All JS files load (green status)
  - [ ] No 404 errors
  - [ ] Page load time < 3 seconds

### Accessibility Check
- [ ] Open blog in browser
- [ ] Check accessibility (AXE DevTools or Lighthouse)
  - F12 → Lighthouse → Accessibility score
  - [ ] Score > 90
  - [ ] No critical issues

### Link Verification
- [ ] Navigation links work
  - [ ] Home link → index.html
  - [ ] Services link → services.html
  - [ ] Other menu items work

- [ ] Social media links work
  - [ ] Facebook link → Facebook page
  - [ ] LinkedIn link → LinkedIn page
  - [ ] Twitter link → Twitter page

---

## 📝 Customization Phase (If Needed)

### Update Footer Address
If needed:
- [ ] Edit `templates/_footer.hbs`
- [ ] Find contact information section
- [ ] Update address, phone, email
- [ ] Save file
- [ ] Run build script again: `python3 build_blogs_final.py`
- [ ] Verify footer updated on 3 random blogs

### Update Navigation
If needed:
- [ ] Edit `templates/_header.hbs`
- [ ] Find navigation menu section
- [ ] Add/remove/edit menu items
- [ ] Save file
- [ ] Run build script again: `python3 build_blogs_final.py`
- [ ] Verify navigation updated on 3 random blogs

### Add New JavaScript
If needed:
- [ ] Edit `templates/_footer.hbs`
- [ ] Find JavaScript section at bottom
- [ ] Add new `<script>` tag
- [ ] Save file
- [ ] Run build script again: `python3 build_blogs_final.py`
- [ ] Verify JS file loads (F12 → Network)

### Update Meta Tags
If needed:
- [ ] Edit `templates/layout.hbs`
- [ ] Find meta tags section
- [ ] Update as needed (author, viewport, etc.)
- [ ] Save file
- [ ] Run build script again: `python3 build_blogs_final.py`
- [ ] Verify in View Page Source of 3 blogs

---

## 🚀 Deployment Phase

### Pre-Deployment Review
- [ ] All file checks passed
- [ ] All content verified
- [ ] SEO tags verified
- [ ] Responsive design verified
- [ ] Performance verified
- [ ] All tests passed

### Staging Deployment (Optional)
If you have a staging environment:
- [ ] Upload all blog files to staging
- [ ] Test on staging server
- [ ] Verify all links work
- [ ] Verify performance
- [ ] Check with real browser (mobile + desktop)

### Production Deployment

#### Option 1: Direct File Upload
- [ ] Upload `blog-*.html` files to production server
- [ ] Keep `templates/` directory local (not needed on production)
- [ ] Verify files upload successfully
- [ ] Test 3 random blogs on production
- [ ] Check that file sizes match local

#### Option 2: Git Deployment
- [ ] Commit all changes
  ```bash
  git add .
  git commit -m "Deploy template system for all 78 blogs"
  git push origin main
  ```
- [ ] Deploy via your CI/CD pipeline
- [ ] Verify deployment completed
- [ ] Test 3 random blogs on production

#### Option 3: rsync/SCP
```bash
rsync -avz blog-*.html user@server:/path/to/www/
```
- [ ] Verify files copied
- [ ] Test 3 random blogs on production

### Post-Deployment Verification
- [ ] Open 5 random blogs on production
- [ ] Check all elements load
- [ ] Check SEO tags present
- [ ] Check responsive design
- [ ] Check performance (should load in < 2s)
- [ ] Monitor error logs for 24 hours

### Analytics & Monitoring
- [ ] Check Google Analytics
  - [ ] No unusual bounce rate changes
  - [ ] Traffic patterns normal
  - [ ] Page load times acceptable

- [ ] Check Search Console
  - [ ] No crawl errors
  - [ ] No index coverage issues
  - [ ] Canonical URLs indexed

- [ ] Check for user issues
  - [ ] Contact forms working
  - [ ] No user complaints
  - [ ] Email notifications working

---

## 📋 Documentation Updates

- [ ] Update README with template system info
- [ ] Update internal wiki/docs
- [ ] Add troubleshooting notes
- [ ] Document customization changes made
- [ ] Create runbook for future builds:
  ```bash
  #!/bin/bash
  # Quick build and deploy
  cd /Users/mac/Documents/fsc/fsc-adrien.github.io
  python3 build_blogs_final.py
  git add .
  git commit -m "Automated blog build - $(date)"
  git push origin main
  ```

---

## 🔄 Post-Deployment Maintenance

### Weekly
- [ ] Monitor analytics for issues
- [ ] Check error logs
- [ ] Verify all blogs loading correctly

### Monthly
- [ ] Run build script to ensure consistency
- [ ] Update templates with new content (if needed)
- [ ] Test responsive design
- [ ] Check SEO performance

### Quarterly
- [ ] Full system audit
- [ ] Backup entire project
- [ ] Review and update documentation
- [ ] Plan enhancements

### Annually
- [ ] Complete system review
- [ ] Performance optimization
- [ ] Security audit
- [ ] Plan next phase features

---

## ❓ Troubleshooting During Deployment

### Issue: Build fails with errors
```
Solution:
1. Check Python version: python3 --version
2. Verify templates exist: ls templates/
3. Run verbose: python3 build_blogs_final.py 2>&1 | head -100
4. Check template syntax
5. Restore from backup if needed
```

### Issue: Blog looks wrong
```
Solution:
1. Check CSS files load (F12 → Network)
2. Check for JavaScript errors (F12 → Console)
3. Verify HTML is valid
4. Compare with original blog file
5. Restore original and re-run build
```

### Issue: SEO tags missing
```
Solution:
1. View page source (Ctrl+U)
2. Search for meta tags
3. Check templates/layout.hbs for tag definitions
4. Run build script again
5. Verify changes appeared
```

### Issue: Links not working
```
Solution:
1. Check link URLs in view page source
2. Verify files exist on server
3. Check file paths are correct
4. Test on local first
5. Check server permissions
```

### Issue: Mobile view broken
```
Solution:
1. Check viewport meta tag
2. Verify CSS is mobile-responsive
3. Test in real mobile browser (not just DevTools)
4. Check for horizontal scrolling
5. Review responsive design on 3 browsers
```

---

## ✅ Final Sign-Off Checklist

- [ ] All 78 blogs verified working
- [ ] All tests passed
- [ ] SEO verified
- [ ] Performance acceptable
- [ ] Responsive design confirmed
- [ ] Documentation updated
- [ ] Team notified of deployment
- [ ] Monitoring set up
- [ ] Rollback plan documented
- [ ] Ready for production ✅

---

## 🎉 Deployment Complete!

When all checks pass, you're ready to mark as complete:

```bash
# Final commit
git add .
git commit -m "Template system deployment complete - all 78 blogs live"
git push origin main

# Create deployment tag
git tag -a deployment/template-system-v1.0 -m "Template system deployment"
git push origin deployment/template-system-v1.0

# Notify team
echo "✅ Template system deployed successfully!"
echo "📊 All 78 blogs now using centralized templates"
echo "⏰ Estimated annual time savings: 40+ hours"
```

---

**Deployment Status**: Ready for Production ✅
**Last Updated**: 2026
**Version**: 1.0
