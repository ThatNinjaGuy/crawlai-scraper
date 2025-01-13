# Web Crawler for AI Content

A simple web crawler designed to extract AI-related content from web pages.

## Important Note on Compliance

Before crawling any website, please ensure you check and comply with the site's `robots.txt` file (e.g., <https://www.linkedin.com/robots.txt>) and respect the website's crawling policies. Some websites may:

- Disallow certain paths from being crawled
- Set specific crawl-delay requirements
- Have user-agent specific rules
- Require authentication or API usage instead of direct crawling

Non-compliance with a website's robots.txt can result in your IP being blocked or potential legal issues.

## Features

This crawler provides three main ways to extract content:

1. **Single Page Crawling**: Quick crawling of individual web pages
2. **Sequential Crawling**: Process multiple URLs one after another, reusing browser sessions
3. **Parallel Crawling**: Efficiently crawl multiple URLs simultaneously with configurable concurrency

## Example Usage

### Single Page Crawling

```python
from crawl4ai import AsyncWebCrawler

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(url="https://example.com")
    print(result.markdown)
```

### Sequential Crawling

Ideal for crawling multiple pages while minimizing resource usage:

```python
urls = ["https://example.com/page1", "https://example.com/page2"]
crawler = AsyncWebCrawler(config=BrowserConfig(headless=True))
await crawler.start()

for url in urls:
    result = await crawler.arun(url=url, session_id="session1")
    print(f"Crawled {url}: {len(result.markdown)} chars")

await crawler.close()
```

### Parallel Crawling

For faster processing of multiple URLs:

```python
async with AsyncWebCrawler() as crawler:
    tasks = [crawler.arun(url=url) for url in urls]
    results = await asyncio.gather(*tasks)
```

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

## Output

The crawler generates Markdown files containing the extracted content. Output files are saved in the `output` directory with timestamps:

- Single page: `crawl_result_YYYYMMDD_HHMMSS.md`
- Sequential crawling: `crawl-docs-sequentially_YYYYMMDD_HHMMSS.md`
- Parallel crawling: `crawl-docs-parallel_YYYYMMDD_HHMMSS.md`
