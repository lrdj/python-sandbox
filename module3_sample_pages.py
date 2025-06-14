#!/usr/bin/env python3
"""
Module 3: Generate Sample Pages for GOV.UK Frontend Jekyll Site

This script creates sample pages demonstrating various GOV.UK Frontend components
for a Jekyll site that uses either self-hosted or CDN-based GOV.UK Frontend assets.

Usage:
    python module3_sample_pages.py [site_dir]

Arguments:
    site_dir            Directory of the Jekyll site (default: test_jekyll_site)
"""

import os
import sys
import argparse
import json

def create_start_page(site_dir):
    """Create a sample start page"""
    content = """---
layout: govuk-default
title: Start page example
---

<div class="govuk-grid-row">
  <div class="govuk-grid-column-two-thirds">
    <h1 class="govuk-heading-xl">Service name goes here</h1>

    <p class="govuk-body">Use this service to:</p>

    <ul class="govuk-list govuk-list--bullet">
      <li>do something</li>
      <li>update something</li>
      <li>apply for something</li>
    </ul>

    <p class="govuk-body">Registering takes around 5 minutes.</p>

    <a href="question-page" role="button" draggable="false" class="govuk-button govuk-button--start" data-module="govuk-button">
      Start now
      <svg class="govuk-button__start-icon" xmlns="http://www.w3.org/2000/svg" width="17.5" height="19" viewBox="0 0 33 40" aria-hidden="true" focusable="false">
        <path fill="currentColor" d="M0 0h13l20 20-20 20H0l20-20z" />
      </svg>
    </a>

    <h2 class="govuk-heading-m">Before you start</h2>

    <p class="govuk-body">You'll need:</p>

    <ul class="govuk-list govuk-list--bullet">
      <li>item 1</li>
      <li>item 2</li>
      <li>item 3</li>
    </ul>

    <p class="govuk-body">
      Read the <a href="#" class="govuk-link">guidance notes</a> before completing this application.
    </p>
  </div>

  <div class="govuk-grid-column-one-third">
    <aside class="govuk-prototype-kit-common-templates-related-items" role="complementary">
      <h2 class="govuk-heading-m" id="subsection-title">
        Related content
      </h2>
      <nav role="navigation" aria-labelledby="subsection-title">
        <ul class="govuk-list govuk-!-font-size-16">
          <li>
            <a href="#" class="govuk-link">
              Related link
            </a>
          </li>
          <li>
            <a href="#" class="govuk-link">
              Related link
            </a>
          </li>
        </ul>
      </nav>
    </aside>
  </div>
</div>
"""
    
    with open(os.path.join(site_dir, "start-page.md"), 'w') as f:
        f.write(content)
    print("Created start-page.md")

def create_question_page(site_dir):
    """Create a sample question page"""
    content = """---
layout: govuk-default
title: Question page example
show_back_link: true
---

<div class="govuk-grid-row">
  <div class="govuk-grid-column-two-thirds">
    <form action="components" method="get">
      <div class="govuk-form-group">
        <fieldset class="govuk-fieldset">
          <legend class="govuk-fieldset__legend govuk-fieldset__legend--l">
            <h1 class="govuk-fieldset__heading">
              Where do you live?
            </h1>
          </legend>
          
          <div class="govuk-radios" data-module="govuk-radios">
            <div class="govuk-radios__item">
              <input class="govuk-radios__input" id="where-do-you-live" name="where-do-you-live" type="radio" value="england">
              <label class="govuk-label govuk-radios__label" for="where-do-you-live">
                England
              </label>
            </div>
            <div class="govuk-radios__item">
              <input class="govuk-radios__input" id="where-do-you-live-2" name="where-do-you-live" type="radio" value="scotland">
              <label class="govuk-label govuk-radios__label" for="where-do-you-live-2">
                Scotland
              </label>
            </div>
            <div class="govuk-radios__item">
              <input class="govuk-radios__input" id="where-do-you-live-3" name="where-do-you-live" type="radio" value="wales">
              <label class="govuk-label govuk-radios__label" for="where-do-you-live-3">
                Wales
              </label>
            </div>
            <div class="govuk-radios__item">
              <input class="govuk-radios__input" id="where-do-you-live-4" name="where-do-you-live" type="radio" value="northern-ireland">
              <label class="govuk-label govuk-radios__label" for="where-do-you-live-4">
                Northern Ireland
              </label>
            </div>
            <div class="govuk-radios__divider">or</div>
            <div class="govuk-radios__item">
              <input class="govuk-radios__input" id="where-do-you-live-5" name="where-do-you-live" type="radio" value="abroad">
              <label class="govuk-label govuk-radios__label" for="where-do-you-live-5">
                I am a British citizen living abroad
              </label>
            </div>
          </div>
        </fieldset>
      </div>

      <button class="govuk-button" data-module="govuk-button">
        Continue
      </button>
    </form>
  </div>
</div>
"""
    
    with open(os.path.join(site_dir, "question-page.md"), 'w') as f:
        f.write(content)
    print("Created question-page.md")

def create_components_page(site_dir):
    """Create a sample components page"""
    content = """---
layout: govuk-default
title: Component examples
show_back_link: true
show_phase_banner: true
phase: beta
---

<div class="govuk-grid-row">
  <div class="govuk-grid-column-full">
    <h1 class="govuk-heading-xl">GOV.UK Frontend Components</h1>
    
    <p class="govuk-body-l">This page demonstrates various GOV.UK Frontend components.</p>
  </div>
</div>

<div class="govuk-grid-row">
  <div class="govuk-grid-column-two-thirds">
    <h2 class="govuk-heading-l">Typography</h2>
    
    <h1 class="govuk-heading-xl">govuk-heading-xl</h1>
    <h2 class="govuk-heading-l">govuk-heading-l</h2>
    <h3 class="govuk-heading-m">govuk-heading-m</h3>
    <h4 class="govuk-heading-s">govuk-heading-s</h4>
    
    <p class="govuk-body-l">govuk-body-l</p>
    <p class="govuk-body">govuk-body</p>
    <p class="govuk-body-s">govuk-body-s</p>
    
    <h2 class="govuk-heading-l">Buttons</h2>
    
    <button class="govuk-button" data-module="govuk-button">
      Default button
    </button>
    
    <button class="govuk-button govuk-button--secondary" data-module="govuk-button">
      Secondary button
    </button>
    
    <button class="govuk-button govuk-button--warning" data-module="govuk-button">
      Warning button
    </button>
    
    <button class="govuk-button" disabled="disabled" aria-disabled="true" data-module="govuk-button">
      Disabled button
    </button>
    
    <h2 class="govuk-heading-l">Text input</h2>
    
    <div class="govuk-form-group">
      <label class="govuk-label" for="input-example">
        National Insurance number
      </label>
      <div id="input-example-hint" class="govuk-hint">
        It's on your National Insurance card, benefit letter, payslip or P60. For example, 'QQ 12 34 56 C'.
      </div>
      <input class="govuk-input" id="input-example" name="test-name" type="text" aria-describedby="input-example-hint">
    </div>
    
    <h2 class="govuk-heading-l">Error messages</h2>
    
    <div class="govuk-form-group govuk-form-group--error">
      <label class="govuk-label" for="file-upload-1">
        Upload a file
      </label>
      <div id="file-upload-1-hint" class="govuk-hint">
        The file must be a PDF
      </div>
      <span id="file-upload-1-error" class="govuk-error-message">
        <span class="govuk-visually-hidden">Error:</span> The file must be a PDF
      </span>
      <input class="govuk-file-upload govuk-file-upload--error" id="file-upload-1" name="file-upload-1" type="file" aria-describedby="file-upload-1-hint file-upload-1-error">
    </div>
    
    <h2 class="govuk-heading-l">Warning text</h2>
    
    <div class="govuk-warning-text">
      <span class="govuk-warning-text__icon" aria-hidden="true">!</span>
      <strong class="govuk-warning-text__text">
        <span class="govuk-warning-text__assistive">Warning</span>
        You can be fined up to £5,000 if you don't register.
      </strong>
    </div>
    
    <h2 class="govuk-heading-l">Summary list</h2>
    
    <dl class="govuk-summary-list">
      <div class="govuk-summary-list__row">
        <dt class="govuk-summary-list__key">
          Name
        </dt>
        <dd class="govuk-summary-list__value">
          Sarah Philips
        </dd>
        <dd class="govuk-summary-list__actions">
          <a class="govuk-link" href="#">
            Change<span class="govuk-visually-hidden"> name</span>
          </a>
        </dd>
      </div>
      <div class="govuk-summary-list__row">
        <dt class="govuk-summary-list__key">
          Date of birth
        </dt>
        <dd class="govuk-summary-list__value">
          5 January 1978
        </dd>
        <dd class="govuk-summary-list__actions">
          <a class="govuk-link" href="#">
            Change<span class="govuk-visually-hidden"> date of birth</span>
          </a>
        </dd>
      </div>
      <div class="govuk-summary-list__row">
        <dt class="govuk-summary-list__key">
          Address
        </dt>
        <dd class="govuk-summary-list__value">
          72 Guild Street<br>London<br>SE23 6FH
        </dd>
        <dd class="govuk-summary-list__actions">
          <a class="govuk-link" href="#">
            Change<span class="govuk-visually-hidden"> address</span>
          </a>
        </dd>
      </div>
      <div class="govuk-summary-list__row">
        <dt class="govuk-summary-list__key">
          Contact details
        </dt>
        <dd class="govuk-summary-list__value">
          <p class="govuk-body">07700 900457</p>
          <p class="govuk-body">sarah.phillips@example.com</p>
        </dd>
        <dd class="govuk-summary-list__actions">
          <a class="govuk-link" href="#">
            Change<span class="govuk-visually-hidden"> contact details</span>
          </a>
        </dd>
      </div>
    </dl>
    
    <h2 class="govuk-heading-l">Notification banner</h2>
    
    <div class="govuk-notification-banner" role="region" aria-labelledby="govuk-notification-banner-title" data-module="govuk-notification-banner">
      <div class="govuk-notification-banner__header">
        <h2 class="govuk-notification-banner__title" id="govuk-notification-banner-title">
          Important
        </h2>
      </div>
      <div class="govuk-notification-banner__content">
        <p class="govuk-notification-banner__heading">
          You have 7 days left to send your application.
          <a class="govuk-notification-banner__link" href="#">View application</a>.
        </p>
      </div>
    </div>
    
    <div class="govuk-notification-banner govuk-notification-banner--success" role="alert" aria-labelledby="govuk-notification-banner-title" data-module="govuk-notification-banner">
      <div class="govuk-notification-banner__header">
        <h2 class="govuk-notification-banner__title" id="govuk-notification-banner-title">
          Success
        </h2>
      </div>
      <div class="govuk-notification-banner__content">
        <h3 class="govuk-notification-banner__heading">
          Application complete
        </h3>
        <p class="govuk-body">
          Your reference number is <br><strong>HDJ2123F</strong>
        </p>
      </div>
    </div>
  </div>
</div>
"""
    
    with open(os.path.join(site_dir, "components.md"), 'w') as f:
        f.write(content)
    print("Created components.md")

def detect_asset_mode(site_dir):
    """Detect whether the site is using CDN or self-hosted assets"""
    layout_path = os.path.join(site_dir, "_layouts", "govuk-default.html")
    if not os.path.exists(layout_path):
        print("Warning: Could not detect asset mode. Layout file not found.")
        return "unknown"
    
    with open(layout_path, 'r') as f:
        content = f.read()
    
    if "cdn.jsdelivr.net" in content:
        return "CDN"
    else:
        return "self-hosted"

def main():
    parser = argparse.ArgumentParser(description="Generate sample pages for GOV.UK Frontend Jekyll site")
    parser.add_argument("site_dir", nargs="?", default="test_jekyll_site", help="Directory of the Jekyll site")
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.site_dir):
        print(f"Error: Directory '{args.site_dir}' does not exist.")
        print("Please run module2_jekyll_structure.py first to create the Jekyll site structure.")
        sys.exit(1)
    
    try:
        # Detect asset mode
        asset_mode = detect_asset_mode(args.site_dir)
        
        # Create sample pages
        create_start_page(args.site_dir)
        create_question_page(args.site_dir)
        create_components_page(args.site_dir)
        
        print(f"\nSample pages have been created in {args.site_dir}")
        print(f"Asset mode detected: {asset_mode}")
        print("To start the Jekyll server, run:")
        print(f"  cd {args.site_dir}")
        print(f"  bundle install --path vendor/bundle")
        print(f"  bundle exec jekyll serve")
        print("\nYour GOV.UK Frontend Jekyll site is now ready to use!")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
