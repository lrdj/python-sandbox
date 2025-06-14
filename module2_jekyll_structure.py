#!/usr/bin/env python3
"""
Module 2: Create Jekyll Structure with GOV.UK Frontend

This script creates a minimal Jekyll site structure that uses GOV.UK Frontend.
It supports both self-hosted assets (default) and CDN-based assets.

Usage:
    python module2_jekyll_structure.py [output_dir] [--site-name NAME] [--cdn]

Arguments:
    output_dir           Directory to create the Jekyll site (default: current directory)
    
Options:
    --site-name NAME     Name of the Jekyll site (default: GOV.UK Frontend Jekyll Site)
    --cdn                Use CDN for GOV.UK Frontend assets instead of self-hosted files
"""

import os
import sys
import argparse
import json
import datetime
import shutil
import subprocess

# Configuration
GOVUK_FRONTEND_VERSION = "5.10.2"
GOVUK_FRONTEND_CDN_BASE = f"https://cdn.jsdelivr.net/npm/govuk-frontend@{GOVUK_FRONTEND_VERSION}"
GOVUK_FRONTEND_CSS = f"{GOVUK_FRONTEND_CDN_BASE}/dist/govuk-frontend-{GOVUK_FRONTEND_VERSION}.min.css"
GOVUK_FRONTEND_JS = f"{GOVUK_FRONTEND_CDN_BASE}/dist/govuk-frontend-{GOVUK_FRONTEND_VERSION}.min.js"

# Essential directories for Jekyll
JEKYLL_DIRS = [
    "_layouts",
    "_includes",
    "assets",
    "assets/css",
    "assets/js",
    "assets/images",
    "assets/fonts"
]

def create_jekyll_structure(output_dir):
    """Create the necessary directory structure for Jekyll"""
    print(f"Creating Jekyll directory structure in {output_dir}...")
    for directory in JEKYLL_DIRS:
        dir_path = os.path.join(output_dir, directory)
        os.makedirs(dir_path, exist_ok=True)

def create_config_yml(output_dir, site_name="GOV.UK Frontend Jekyll Site"):
    """Create a Jekyll _config.yml file"""
    config_content = f"""# Site settings
title: {site_name}
email: your-email@example.com
description: >-
  A Jekyll site using the GOV.UK Frontend design system.
baseurl: "" # the subpath of your site, e.g. /blog
url: "" # the base hostname & protocol for your site, e.g. http://example.com

# Build settings
markdown: kramdown
plugins:
  - jekyll-feed

# Exclude from processing
exclude:
  - .sass-cache/
  - .jekyll-cache/
  - gemfiles/
  - Gemfile
  - Gemfile.lock
  - node_modules/
  - vendor/bundle/
  - vendor/cache/
  - vendor/gems/
  - vendor/ruby/
  - govuk_jekyll_integration.py
"""
    
    with open(os.path.join(output_dir, "_config.yml"), 'w') as f:
        f.write(config_content)
    print("Created _config.yml")

def create_gemfile(output_dir):
    """Create a Gemfile for the Jekyll site"""
    gemfile_content = """source "https://rubygems.org"

gem "jekyll", "~> 4.2"
gem "webrick", "~> 1.7"
gem "jekyll-feed", "~> 0.12"

# Windows and JRuby does not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library.
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", "~> 1.2"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]
"""
    
    with open(os.path.join(output_dir, "Gemfile"), 'w') as f:
        f.write(gemfile_content)
    print("Created Gemfile")

def create_custom_css(output_dir):
    """Create a custom CSS file for additional styles"""
    css_content = """---
---
/* Custom styles for GOV.UK Frontend Jekyll site */

/* Add your custom styles below */
"""
    
    with open(os.path.join(output_dir, "assets/css/custom.css"), 'w') as f:
        f.write(css_content)
    print("Created custom.css")

def create_default_layout(output_dir, use_cdn=False):
    """Create a default Jekyll layout that uses GOV.UK Frontend"""
    
    # Determine asset paths based on mode
    if use_cdn:
        css_path = GOVUK_FRONTEND_CSS
        js_path = GOVUK_FRONTEND_JS
        favicon_path = f"{GOVUK_FRONTEND_CDN_BASE}/dist/assets/images/favicon.ico"
        mask_icon_path = f"{GOVUK_FRONTEND_CDN_BASE}/dist/assets/images/govuk-icon-mask.svg"
        apple_touch_icon_path = f"{GOVUK_FRONTEND_CDN_BASE}/dist/assets/images/govuk-icon-180.png"
    else:
        css_path = "{{ '/assets/css/govuk-frontend-" + GOVUK_FRONTEND_VERSION + ".min.css' | relative_url }}"
        js_path = "{{ '/assets/js/govuk-frontend-" + GOVUK_FRONTEND_VERSION + ".min.js' | relative_url }}"
        favicon_path = "{{ '/assets/images/favicon.ico' | relative_url }}"
        mask_icon_path = "{{ '/assets/images/govuk-icon-mask.svg' | relative_url }}"
        apple_touch_icon_path = "{{ '/assets/images/govuk-icon-180.png' | relative_url }}"
    
    layout_content = f"""<!DOCTYPE html>
<html lang="en" class="govuk-template">
  <head>
    <meta charset="utf-8">
    <title>{{% if page.title %}}{{{{ page.title }}}} - {{% endif %}}{{{{ site.title }}}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    <meta name="theme-color" content="#0b0c0c">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    
    <!-- Load GOV.UK Frontend CSS -->
    <link rel="stylesheet" href="{css_path}">
    
    <!-- Load custom CSS -->
    <link rel="stylesheet" href="{{{{ '/assets/css/custom.css' | relative_url }}}}">
    
    <!-- Favicons -->
    <link rel="shortcut icon" href="{favicon_path}" type="image/x-icon">
    <link rel="mask-icon" href="{mask_icon_path}" color="#0b0c0c">
    <link rel="apple-touch-icon" href="{apple_touch_icon_path}">
  </head>
  <body class="govuk-template__body">
    <script>document.body.className = ((document.body.className) ? document.body.className + ' js-enabled' : 'js-enabled');</script>
    
    <a href="#main-content" class="govuk-skip-link">Skip to main content</a>
    
    <header class="govuk-header" role="banner" data-module="govuk-header">
      <div class="govuk-header__container govuk-width-container">
        <div class="govuk-header__logo">
          <a href="{{{{ '/' | relative_url }}}}" class="govuk-header__link govuk-header__link--homepage">
            <span class="govuk-header__logotype">
              <svg aria-hidden="true" focusable="false" class="govuk-header__logotype-crown" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 132 97" height="30" width="36">
                <path fill="currentColor" fill-rule="evenodd" d="M25 30.2c3.5 1.5 7.7-.2 9.1-3.7 1.5-3.6-.2-7.8-3.9-9.2-3.6-1.4-7.6.3-9.1 3.9-1.4 3.5.3 7.5 3.9 9zM9 39.5c3.6 1.5 7.8-.2 9.2-3.7 1.5-3.6-.2-7.8-3.9-9.1-3.6-1.5-7.6.2-9.1 3.8-1.4 3.5.3 7.5 3.8 9zM4.4 57.2c3.5 1.5 7.7-.2 9.1-3.8 1.5-3.6-.2-7.7-3.9-9.1-3.5-1.5-7.6.3-9.1 3.8-1.4 3.5.3 7.6 3.9 9.1zm38.3-21.4c3.5 1.5 7.7-.2 9.1-3.8 1.5-3.6-.2-7.7-3.9-9.1-3.6-1.5-7.6.3-9.1 3.8-1.3 3.6.4 7.7 3.9 9.1zm64.4-5.6c-3.6 1.5-7.8-.2-9.1-3.7-1.5-3.6.2-7.8 3.8-9.2 3.6-1.4 7.7.3 9.2 3.9 1.3 3.5-.4 7.5-3.9 9zm15.9 9.3c-3.6 1.5-7.7-.2-9.1-3.7-1.5-3.6.2-7.8 3.7-9.1 3.6-1.5 7.7.2 9.2 3.8 1.5 3.5-.3 7.5-3.8 9zm4.7 17.7c-3.6 1.5-7.8-.2-9.2-3.8-1.5-3.6.2-7.7 3.9-9.1 3.6-1.5 7.7.3 9.2 3.8 1.3 3.5-.4 7.6-3.9 9.1zM89.3 35.8c-3.6 1.5-7.8-.2-9.2-3.8-1.4-3.6.2-7.7 3.9-9.1 3.6-1.5 7.7.3 9.2 3.8 1.4 3.6-.3 7.7-3.9 9.1zM69.7 17.7l8.9 4.7V9.3l-8.9 2.8c-.2-.3-.5-.6-.9-.9L72.4 0H59.6l3.5 11.2c-.3.3-.6.5-.9.9l-8.8-2.8v13.1l8.8-4.7c.3.3.6.7.9.9l-5 15.4v.1c-.2.8-.4 1.6-.4 2.4 0 4.1 3.1 7.5 7 8.1h.2c.3 0 .7.1 1 .1.4 0 .7 0 1-.1h.2c4-.6 7.1-4.1 7.1-8.1 0-.8-.1-1.7-.4-2.4V34l-5.1-15.4c.4-.2.7-.6 1-.9zM66 92.8c16.9 0 32.8 1.1 47.1 3.2 4-16.9 8.9-26.7 14-33.5l-9.6-3.4c1 4.9 1.1 7.2 0 10.2-1.5-1.4-3-4.3-4.2-8.7L108.6 76c2.8-2 5-3.2 7.5-3.3-4.4 9.4-10 11.9-13.6 11.2-4.3-.8-6.3-4.6-5.6-7.9 1-4.7 5.7-5.9 8-.5 4.3-8.7-3-11.4-7.6-8.8 7.1-7.2 7.9-13.5 2.1-21.1-8 6.1-8.1 12.3-4.5 20.8-4.7-5.4-12.1-2.5-9.5 6.2 3.4-5.2 7.9-2 7.2 3.1-.6 4.3-6.4 7.8-13.5 7.2-10.3-.9-10.9-8-11.2-13.8 2.5-.5 7.1 1.8 11 7.3L80.2 60c-4.1 4.4-8 5.3-12.3 5.4 1.4-4.4 8-11.6 8-11.6H55.5s6.4 7.2 7.9 11.6c-4.2-.1-8-1-12.3-5.4l1.4 16.4c3.9-5.5 8.5-7.7 10.9-7.3-.3 5.8-.9 12.8-11.1 13.8-7.2.6-12.9-2.9-13.5-7.2-.7-5 3.8-8.3 7.1-3.1 2.7-8.7-4.6-11.6-9.4-6.2 3.7-8.5 3.6-14.7-4.6-20.8-5.8 7.6-5 13.9 2.2 21.1-4.7-2.6-11.9.1-7.7 8.8 2.3-5.5 7.1-4.2 8.1.5.7 3.3-1.3 7.1-5.7 7.9-3.5.7-9-1.8-13.5-11.2 2.5.1 4.7 1.3 7.5 3.3l-4.7-15.4c-1.2 4.4-2.7 7.2-4.3 8.7-1.1-3-.9-5.3 0-10.2l-9.5 3.4c5 6.9 9.9 16.7 14 33.5 14.8-2.1 30.8-3.2 47.7-3.2z"></path>
              </svg>
              <span class="govuk-header__logotype-text">
                GOV.UK
              </span>
            </span>
          </a>
        </div>
        <div class="govuk-header__content">
          <a href="{{{{ '/' | relative_url }}}}" class="govuk-header__link govuk-header__link--service-name">
            {{{{ site.title }}}}
          </a>
        </div>
      </div>
    </header>

    <div class="govuk-width-container">
      {{% if page.show_phase_banner %}}
      <div class="govuk-phase-banner">
        <p class="govuk-phase-banner__content">
          <strong class="govuk-tag govuk-phase-banner__content__tag">
            {{{{ page.phase | default: "alpha" }}}}
          </strong>
          <span class="govuk-phase-banner__text">
            This is a new service – your <a class="govuk-link" href="#">feedback</a> will help us to improve it.
          </span>
        </p>
      </div>
      {{% endif %}}
      
      {{% if page.show_back_link %}}
      <a href="javascript:window.history.back()" class="govuk-back-link">Back</a>
      {{% endif %}}

      <main class="govuk-main-wrapper" id="main-content" role="main">
        {{{{ content }}}}
      </main>
    </div>

    <footer class="govuk-footer" role="contentinfo">
      <div class="govuk-width-container">
        <div class="govuk-footer__meta">
          <div class="govuk-footer__meta-item govuk-footer__meta-item--grow">
            <h2 class="govuk-visually-hidden">Support links</h2>
            <ul class="govuk-footer__inline-list">
              <li class="govuk-footer__inline-list-item">
                <a class="govuk-footer__link" href="#">
                  Help
                </a>
              </li>
              <li class="govuk-footer__inline-list-item">
                <a class="govuk-footer__link" href="#">
                  Privacy
                </a>
              </li>
              <li class="govuk-footer__inline-list-item">
                <a class="govuk-footer__link" href="#">
                  Cookies
                </a>
              </li>
              <li class="govuk-footer__inline-list-item">
                <a class="govuk-footer__link" href="#">
                  Accessibility statement
                </a>
              </li>
            </ul>
            
            <svg aria-hidden="true" focusable="false" class="govuk-footer__licence-logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 483.2 195.7" height="17" width="41">
              <path fill="currentColor" d="M421.5 142.8V.1l-50.7 32.3v161.1h112.4v-50.7zm-122.3-9.6A47.12 47.12 0 0 1 221 97.8c0-26 21.1-47.1 47.1-47.1 16.7 0 31.4 8.7 39.7 21.8l42.7-27.2A97.63 97.63 0 0 0 268.1 0c-36.5 0-68.3 20.1-85.1 49.7A98 98 0 0 0 97.8 0C43.9 0 0 43.9 0 97.8s43.9 97.8 97.8 97.8c36.5 0 68.3-20.1 85.1-49.7a97.76 97.76 0 0 0 149.6 25.4l19.4 22.2h3v-87.8h-80l24.3 27.5zM97.8 145c-26 0-47.1-21.1-47.1-47.1s21.1-47.1 47.1-47.1 47.2 21 47.2 47S123.8 145 97.8 145"></path>
            </svg>
            <span class="govuk-footer__licence-description">
              All content is available under the
              <a class="govuk-footer__link" href="https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/" rel="license">Open Government Licence v3.0</a>, except where otherwise stated
            </span>
          </div>
          <div class="govuk-footer__meta-item">
            <a class="govuk-footer__link govuk-footer__copyright-logo" href="https://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/crown-copyright/">© Crown copyright</a>
          </div>
        </div>
      </div>
    </footer>
    
    <!-- Load GOV.UK Frontend JavaScript -->
    <script src="{js_path}"></script>
    <script>window.GOVUKFrontend.initAll()</script>
  </body>
</html>
"""
    
    layouts_dir = os.path.join(output_dir, "_layouts")
    os.makedirs(layouts_dir, exist_ok=True)
    
    with open(os.path.join(layouts_dir, "govuk-default.html"), 'w') as f:
        f.write(layout_content)
    print("Created govuk-default.html layout")

def create_index_page(output_dir):
    """Create a simple index page"""
    index_content = """---
layout: govuk-default
title: Home
---

<div class="govuk-grid-row">
  <div class="govuk-grid-column-two-thirds">
    <h1 class="govuk-heading-xl">GOV.UK Frontend with Jekyll</h1>
    
    <p class="govuk-body-l">This is a sample site demonstrating GOV.UK Frontend components with Jekyll.</p>
    
    <p class="govuk-body">This site uses the GOV.UK Frontend files to provide the styling and components.</p>
    
    <h2 class="govuk-heading-m">Sample pages</h2>
    
    <ul class="govuk-list govuk-list--bullet">
      <li><a href="start-page" class="govuk-link">Start page example</a></li>
      <li><a href="question-page" class="govuk-link">Question page example</a></li>
      <li><a href="components" class="govuk-link">Component examples</a></li>
    </ul>
    
    <a href="start-page" role="button" draggable="false" class="govuk-button govuk-button--start" data-module="govuk-button">
      Start now
      <svg class="govuk-button__start-icon" xmlns="http://www.w3.org/2000/svg" width="17.5" height="19" viewBox="0 0 33 40" aria-hidden="true" focusable="false">
        <path fill="currentColor" d="M0 0h13l20 20-20 20H0l20-20z" />
      </svg>
    </a>
  </div>
</div>
"""
    
    with open(os.path.join(output_dir, "index.md"), 'w') as f:
        f.write(index_content)
    print("Created index.md")

def create_readme(output_dir, version, use_cdn=False):
    """Create a README file with usage instructions"""
    asset_mode = "CDN" if use_cdn else "self-hosted"
    
    readme_content = f"""# GOV.UK Frontend for Jekyll

This directory contains a Jekyll site with GOV.UK Frontend integration using {asset_mode} assets.

## Version Information
- GOV.UK Frontend version: {version}
- Created: {datetime.datetime.now().strftime("%Y-%m-%d")}
- Asset mode: {asset_mode}

## Getting Started

1. Install Jekyll and Bundler:
   ```
   gem install jekyll bundler
   ```

2. Install dependencies:
   ```
   bundle install --path vendor/bundle
   ```

3. Start the Jekyll server:
   ```
   bundle exec jekyll serve
   ```

4. View the site at [http://localhost:4000](http://localhost:4000)

## Components

This site includes sample pages demonstrating GOV.UK Frontend components:

- Home page
- Start page example
- Question page example
- Component examples page

For more information on available components, refer to the [GOV.UK Design System](https://design-system.service.gov.uk/components/).

## Customization

You can customize this site by:

1. Editing the `_config.yml` file to change site settings
2. Modifying the layout in `_layouts/govuk-default.html`
3. Adding your own styles in `assets/css/custom.css`
4. Creating new pages using the GOV.UK Frontend components
"""
    
    with open(os.path.join(output_dir, "README.md"), 'w') as f:
        f.write(readme_content)
    print("Created README.md")

def download_assets_if_needed(output_dir, version):
    """Download assets if using self-hosted mode"""
    assets_dir = os.path.join(output_dir, "assets")
    
    # Check if module1 script exists
    module1_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "module1_download_assets.py")
    
    if os.path.exists(module1_path):
        print("Downloading GOV.UK Frontend assets for self-hosting...")
        try:
            subprocess.run([sys.executable, module1_path, assets_dir, "--version", f"v{version}"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to download assets: {e}")
            return False
    else:
        print("Warning: module1_download_assets.py not found. Please download assets manually.")
        return False

def main():
    parser = argparse.ArgumentParser(description="Create Jekyll structure with GOV.UK Frontend")
    parser.add_argument("output_dir", nargs="?", default=".", help="Output directory for Jekyll site")
    parser.add_argument("--site-name", default="GOV.UK Frontend Jekyll Site", help="Name of the Jekyll site")
    parser.add_argument("--cdn", action="store_true", help="Use CDN for GOV.UK Frontend assets instead of self-hosted files")
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    try:
        # Create Jekyll structure
        create_jekyll_structure(args.output_dir)
        
        # Download assets if using self-hosted mode
        if not args.cdn:
            download_assets_if_needed(args.output_dir, GOVUK_FRONTEND_VERSION)
        
        # Create config.yml
        create_config_yml(args.output_dir, args.site_name)
        
        # Create Gemfile
        create_gemfile(args.output_dir)
        
        # Create custom CSS
        create_custom_css(args.output_dir)
        
        # Create default layout
        create_default_layout(args.output_dir, args.cdn)
        
        # Create index page
        create_index_page(args.output_dir)
        
        # Create README
        create_readme(args.output_dir, f"v{GOVUK_FRONTEND_VERSION}", args.cdn)
        
        asset_mode = "CDN" if args.cdn else "self-hosted"
        print(f"\nJekyll structure with GOV.UK Frontend v{GOVUK_FRONTEND_VERSION} ({asset_mode} mode) has been created in {args.output_dir}")
        print("To start the Jekyll server, run:")
        print(f"  cd {args.output_dir}")
        print(f"  bundle install --path vendor/bundle")
        print(f"  bundle exec jekyll serve")
        print("\nYou can now run module3_sample_pages.py to create sample pages.")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
