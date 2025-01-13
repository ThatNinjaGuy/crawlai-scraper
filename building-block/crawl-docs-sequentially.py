import asyncio
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import requests
from xml.etree import ElementTree
import os
from datetime import datetime


async def crawl_sequential(urls: List[str], output_file: str):
    print("\n=== Sequential Crawling with Session Reuse ===")

    browser_config = BrowserConfig(
        headless=True,
        # For better performance in Docker or low-memory environments:
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )

    crawl_config = CrawlerRunConfig(markdown_generator=DefaultMarkdownGenerator())

    # Create the crawler (opens the browser)
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()

    try:
        session_id = "session1"  # Reuse the same session across all URLs
        with open(output_file, "w", encoding="utf-8") as f:
            for url in urls:
                # Add header for each URL
                header = f"\n\n# Crawl Results for: {url}\n\n---\n\n"
                f.write(header)
                print(f"\nCrawling: {url}")

                result = await crawler.arun(
                    url=url, config=crawl_config, session_id=session_id
                )
                if result.success:
                    print(f"Successfully crawled: {url}")
                    print(f"Markdown length: {len(result.markdown_v2.raw_markdown)}")
                    # Write the markdown content
                    f.write(result.markdown_v2.raw_markdown)
                else:
                    error_msg = f"Failed to crawl URL. Error: {result.error_message}\n"
                    print(f"Failed: {url} - Error: {result.error_message}")
                    f.write(error_msg)

                # Add separator between URLs
                f.write("\n\n---\n")

    finally:
        # After all URLs are done, close the crawler (and the browser)
        await crawler.close()


def get_pydantic_ai_docs_urls():
    """
    Fetches all the urls from the Pydantic AI documentation.
    Uses the sitemap (https://ai.pydantic.dev/sitemap.xml) to get these URLs

    Returns:
        List[str]: A list of URLs to crawl.
    """
    sitemap_url = "https://ai.pydantic.dev/sitemap.xml"
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()

        # Parse the xml
        root = ElementTree.fromstring(response.content)

        # Extract all urls from sitemap.xml
        # Namespace is usually defined in the root element
        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [elem.text for elem in root.findall(".//ns:loc", namespace)]

        return urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}")


async def main():
    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"crawl-docs-sequentially_{timestamp}.md")

    urls = get_pydantic_ai_docs_urls()
    if urls:
        print(f"Found {len(urls)} URLs to crawl")
        print(f"Output will be saved to: {output_file}")
        await crawl_sequential(urls, output_file)
        print(f"\nCrawling complete. Results saved to: {output_file}")
    else:
        print("No URLs found")


if __name__ == "__main__":
    asyncio.run(main())
