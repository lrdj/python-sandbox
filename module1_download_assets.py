#!/usr/bin/env python3
"""
Module 1: Download GOV.UK Frontend Assets

This script downloads GOV.UK Frontend assets for self-hosting in a Jekyll site.
It extracts the necessary files from the official release.

Usage:
    python module1_download_assets.py [output_dir] [--version VERSION]

Arguments:
    output_dir           Directory to save the assets (default: ./assets)
    
Options:
    --version VERSION    Specific version of GOV.UK Frontend to download (default: v5.10.2)
"""

import os
import sys
import shutil
import zipfile
import tempfile
import argparse
import requests
import json
from pathlib import Path
import datetime

# Configuration
GOVUK_FRONTEND_REPO = "alphagov/govuk-frontend"
DEFAULT_VERSION = "v5.10.2"
VERSION_FILE = "govuk_frontend_version.json"

def get_latest_version():
    """Get the latest version of GOV.UK Frontend from GitHub API"""
    try:
        response = requests.get(f"https://api.github.com/repos/{GOVUK_FRONTEND_REPO}/releases/latest")
        if response.status_code == 200:
            return response.json()["tag_name"]
        else:
            return DEFAULT_VERSION
    except Exception as e:
        print(f"Error fetching latest version: {e}")
        return DEFAULT_VERSION

def save_version_info(output_dir, version):
    """Save version information to the version file"""
    version_file_path = os.path.join(output_dir, VERSION_FILE)
    data = {
        "version": version,
        "download_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "files": {
            "css": [],
            "js": [],
            "assets": []
        }
    }
    
    with open(version_file_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    return version_file_path

def download_govuk_frontend(temp_dir, version=DEFAULT_VERSION):
    """Download the specified version of GOV.UK Frontend zip file"""
    zip_url = f"https://github.com/{GOVUK_FRONTEND_REPO}/archive/{version}.zip"
    print(f"Downloading GOV.UK Frontend {version} from {zip_url}...")
    
    response = requests.get(zip_url, stream=True)
    if response.status_code != 200:
        raise Exception(f"Failed to download GOV.UK Frontend: HTTP {response.status_code}")
    
    zip_path = os.path.join(temp_dir, "govuk-frontend.zip")
    
    with open(zip_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"Download complete: {zip_path}")
    return zip_path

def extract_zip(zip_path, extract_dir):
    """Extract the zip file"""
    print(f"Extracting files to {extract_dir}...")
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    
    # Find the extracted directory (usually govuk-frontend-X.Y.Z)
    extracted_dirs = [d for d in os.listdir(extract_dir) if os.path.isdir(os.path.join(extract_dir, d))]
    if not extracted_dirs:
        raise Exception("Failed to extract GOV.UK Frontend")
    
    extracted_dir = os.path.join(extract_dir, extracted_dirs[0])
    print(f"Extracted to: {extracted_dir}")
    return extracted_dir

def copy_assets(extracted_dir, output_dir):
    """Copy necessary assets to the output directory"""
    # Create asset directories
    css_dir = os.path.join(output_dir, "css")
    js_dir = os.path.join(output_dir, "js")
    fonts_dir = os.path.join(output_dir, "fonts")
    images_dir = os.path.join(output_dir, "images")
    
    os.makedirs(css_dir, exist_ok=True)
    os.makedirs(js_dir, exist_ok=True)
    os.makedirs(fonts_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    
    # Copy CSS files
    css_files = []
    for root, dirs, files in os.walk(extracted_dir):
        for file in files:
            if file.endswith('.min.css'):
                src_path = os.path.join(root, file)
                dest_path = os.path.join(css_dir, file)
                shutil.copy2(src_path, dest_path)
                css_files.append(dest_path)
                print(f"Copied CSS: {file}")
    
    # Copy JS files
    js_files = []
    for root, dirs, files in os.walk(extracted_dir):
        for file in files:
            if file.endswith('.min.js'):
                src_path = os.path.join(root, file)
                dest_path = os.path.join(js_dir, file)
                shutil.copy2(src_path, dest_path)
                js_files.append(dest_path)
                print(f"Copied JS: {file}")
    
    # Copy font files
    font_files = []
    for root, dirs, files in os.walk(extracted_dir):
        for file in files:
            if file.endswith(('.woff', '.woff2')):
                src_path = os.path.join(root, file)
                dest_path = os.path.join(fonts_dir, file)
                shutil.copy2(src_path, dest_path)
                font_files.append(dest_path)
                print(f"Copied font: {file}")
    
    # Copy image files
    image_files = []
    for root, dirs, files in os.walk(extracted_dir):
        for file in files:
            if file.endswith(('.png', '.svg', '.ico')):
                src_path = os.path.join(root, file)
                dest_path = os.path.join(images_dir, file)
                shutil.copy2(src_path, dest_path)
                image_files.append(dest_path)
                print(f"Copied image: {file}")
    
    return {
        "css": css_files,
        "js": js_files,
        "fonts": font_files,
        "images": image_files
    }

def main():
    parser = argparse.ArgumentParser(description="Download GOV.UK Frontend assets for self-hosting")
    parser.add_argument("output_dir", nargs="?", default="./assets", help="Output directory for assets")
    parser.add_argument("--version", default=DEFAULT_VERSION, help="Version of GOV.UK Frontend to download")
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Create temporary directory for download and extraction
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Download GOV.UK Frontend
            zip_path = download_govuk_frontend(temp_dir, args.version)
            
            # Extract the zip file
            extracted_dir = extract_zip(zip_path, temp_dir)
            
            # Copy assets to output directory
            copied_files = copy_assets(extracted_dir, args.output_dir)
            
            # Save version information
            version_file = save_version_info(args.output_dir, args.version)
            
            print("\nAsset download and extraction complete!")
            print(f"Assets saved to: {os.path.abspath(args.output_dir)}")
            print(f"Version information saved to: {os.path.abspath(version_file)}")
            print("\nSummary of copied files:")
            print(f"CSS files: {len(copied_files['css'])}")
            print(f"JavaScript files: {len(copied_files['js'])}")
            print(f"Font files: {len(copied_files['fonts'])}")
            print(f"Image files: {len(copied_files['images'])}")
            
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
