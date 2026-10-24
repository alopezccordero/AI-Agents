from concurrent.futures import ThreadPoolExecutor
import time

def fetch_data(site_id):
    time.sleep(1)
    return f"Data from site {site_id}"

# The context manager automatically cleans up and joins threads when done
with ThreadPoolExecutor(max_workers=3) as executor:
    # Use map to apply the function to an iterable of inputs concurrently
    results = executor.map(fetch_data, range(1, 6))

# Print the gathered results
for result in results:
    print(result)
