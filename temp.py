import asyncio
import random

# Mock API request (first function)
async def api_request(item):
    print(f"Starting API request for {item}")
    await asyncio.sleep(random.uniform(1, 3))  # Simulate variable API response time
    print(f"Completed API request for {item}")
    return f"key_{item}"  # Simulated key returned by the API

# Mock download (second function)dddd
async def download_data(key):
    print(f"Attempting to download data for {key}")
    # Simulate a scenario where the key might not be ready yet
    if random.random() < 0.25:  # 50% chance of raising an error
        raise ValueError(f"Data for {key} is not ready yet.")
    await asyncio.sleep(random.uniform(1, 2))  # Simulate download time
    print(f"Successfully downloaded data for {key}")

# Process a single item with retry for download
async def process_item_with_retry(item, semaphore, max_retries=5, delay=2):
    async with semaphore:  # Ensure concurrency limit
        key = await api_request(item)
        retries = 0
        while retries < max_retries:
            try:
                await download_data(key)
                break  # Exit loop if download is successful
            except ValueError as e:
                print(f"Retry {retries + 1}/{max_retries} for {key}: {e}")
                retries += 1
                await asyncio.sleep(delay)  # Wait before retrying
        else:
            print(f"Failed to download data for {key} after {max_retries} retries.")

# Main function to process all items
async def main():
    items = list(range(10))  # Example list of 10 items
    max_concurrent_requests = 3  # Limit to 3 concurrent API requests
    semaphore = asyncio.Semaphore(max_concurrent_requests)
    
    # Create and run tasks
    tasks = [process_item_with_retry(item, semaphore) for item in items]
    await asyncio.gather(*tasks)  # Wait for all tasks to complete

# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())
