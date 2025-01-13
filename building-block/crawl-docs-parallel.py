import requests
from xml.etree import ElementTree
import os
import asyncio
from datetime import datetime
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode


async def crawl_parallel(urls: List[str], output_file: str, max_concurrent: int = 3):
    print("\n=== Parallel Crawling with Browser Reuse ===")

    # Minimal browser config
    browser_config = BrowserConfig(
        headless=True,
        verbose=False,
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )
    crawl_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

    # Create the crawler instance
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()

    try:
        success_count = 0
        fail_count = 0

        with open(output_file, "w", encoding="utf-8") as f:
            # We'll chunk the URLs in batches of 'max_concurrent'
            for i in range(0, len(urls), max_concurrent):
                batch = urls[i : i + max_concurrent]
                tasks = []

                for j, url in enumerate(batch):
                    # Unique session_id per concurrent sub-task
                    session_id = f"parallel_session_{i + j}"
                    task = crawler.arun(
                        url=url, config=crawl_config, session_id=session_id
                    )
                    tasks.append(task)

                # Gather results
                results = await asyncio.gather(*tasks, return_exceptions=True)

                # Process and write results
                for url, result in zip(batch, results):
                    # Add header for each URL
                    header = f"\n\n# Crawl Results for: {url}\n\n---\n\n"
                    f.write(header)

                    if isinstance(result, Exception):
                        error_msg = f"Error crawling URL: {str(result)}\n"
                        print(f"Error crawling {url}: {result}")
                        f.write(error_msg)
                        fail_count += 1
                    elif result.success:
                        print(f"Successfully crawled: {url}")
                        f.write(result.markdown_v2.raw_markdown)
                        success_count += 1
                    else:
                        error_msg = (
                            f"Failed to crawl URL. Error: {result.error_message}\n"
                        )
                        print(f"Failed: {url} - Error: {result.error_message}")
                        f.write(error_msg)
                        fail_count += 1

                    # Add separator between URLs
                    f.write("\n\n---\n")

        print(f"\nSummary:")
        print(f"  - Successfully crawled: {success_count}")
        print(f"  - Failed: {fail_count}")

    finally:
        print("\nClosing crawler...")
        await crawler.close()


def get_pydantic_ai_docs_urls():
    """
    Fetches all the urls from the Pydantic AI documentation.
    Uses the sitemap (https://ai.pydantic.dev/sitemap.xml) to get these URLs.

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
    output_file = os.path.join(output_dir, f"crawl-docs-parallel_{timestamp}.md")

    urls = get_pydantic_ai_docs_urls()
    if urls:
        print(f"Found {len(urls)} URLs to crawl")
        print(f"Output will be saved to: {output_file}")
        await crawl_parallel(urls, output_file, max_concurrent=10)
        print(f"\nCrawling complete. Results saved to: {output_file}")
    else:
        print("No URLs found")


if __name__ == "__main__":
    asyncio.run(main())
