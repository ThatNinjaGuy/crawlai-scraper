# Web Crawler for AI Content

A simple web crawler designed to extract AI-related content from web pages.

## Important Note on Compliance

Before crawling any website, please ensure you check and comply with the site's `robots.txt` file (e.g., <https://www.linkedin.com/robots.txt>) and respect the website's crawling policies. Some websites may:

- Disallow certain paths from being crawled
- Set specific crawl-delay requirements
- Have user-agent specific rules
- Require authentication or API usage instead of direct crawling

Non-compliance with a website's robots.txt can result in your IP being blocked or potential legal issues.

## Data Scraping Methodology

This crawler uses sitemap.xml files as the primary method for discovering and crawling website content. Sitemaps provide a structured way to access all publicly available pages on a website.

### How it Works

1. The crawler first attempts to locate the sitemap by checking common locations:
   - `https://example.com/sitemap.xml`
   - `https://example.com/sitemap_index.xml`
   - Looking up the sitemap location in `robots.txt`

2. Once found, the crawler:
   - Parses the XML structure
   - Extracts all URLs listed in the sitemap
   - Filters for relevant content pages (excluding media files, etc.)
   - Respects the crawl-delay and rate limits specified in robots.txt

### Example Usage

## Quick Start

## Development Setup

1. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:

   ```bash
   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run post-installation setup:

   ```bash
   crawl4ai-setup
   ```

5. Verify installation:

   ```bash
   crawl4ai-doctor
   ```

6. When you're done, deactivate the virtual environment:

   ```bash
   deactivate
   ```

Note: Make sure you have Python 3.x installed before starting.
