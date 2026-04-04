# wikimedia-outreachy-task-2
## URL Status Checker from CSV
### Overview

This script reads a list of URLs from a CSV file and checks their HTTP status codes. It is designed to validate whether each URL is reachable and responding correctly.

The script prints the status code alongside each URL, making it easy to identify broken or unreachable links.

Features
* Reads URLs from a CSV file
* Automatically normalizes URLs (adds http:// if missing)
* Uses HEAD requests for faster checks
* Falls back to GET requests if HEAD is not supported
* Handles errors gracefully
* Displays results in a simple (status) URL format

### Requirements
* Python 3.x
* nrequests library

Install the required dependency using:

`pip install requests `

### CSV Format

* The input CSV file must contain a column named:

`urls`

Example:

```urls
google.com
https://example.com
invalid-url

```
### How It Works
1. URL Normalization

The script ensures every URL has a valid scheme (http:// or https://).
If missing, it automatically prepends http://.


2. Reading the CSV File
Uses csv.DictReader to read rows
Extracts values from the urls column
Ignores empty entries


3. Sending Requests
First attempts a HEAD request (faster, no body content)
If the server does not support HEAD (e.g., returns 405 or 501), it falls back to a GET request
Uses a timeout of 15 seconds to prevent hanging



4. Output

Each URL is printed with its status:
```
(200) http://google.com
(404) http://example.com/page
(ERROR) http://invalid-url
```

Usage

Run the script from the terminal:


` python url_status_from_csv.py "Task 2 - Intern.csv"`



### Code Structure

`normalize_url(url)`

* Cleans and formats the URL
* Adds a scheme if missing

`iter_urls_from_csv(csv_path, column_name)`
* Reads URLs from the CSV file
* Yields valid, normalized URLs

main()
* Handles command-line input
* Sends HTTP requests
* Prints results


### Error Handling

* Invalid URLs or failed requests are caught using requests.RequestException
* These are reported as:

`(ERROR) url`




### Author

This script was written as part of an Outreachy contribution task.

### What I Learned

* While working on this task, I gained a better understanding of how to interact with web resources using Python.

* One thing I learned was the difference between HEAD and GET requests. Initially, I assumed all requests should use GET, but I discovered that HEAD is more efficient when you only need the status of a URL because it does not return the response body. However, I also learned that not all servers support HEAD requests, which is why I implemented a fallback to GET when necessary.

* I also learned how to work with CSV files using csv.DictReader. This made it easier to access specific columns by name instead of relying on index positions, which improves code readability and flexibility.

* Another important concept I understood was URL normalization. Some of the URLs in the CSV file may not include a scheme like http:// or https://, and without it, requests can fail. By adding a normalization step, I ensured that all URLs are in a valid format before making requests.

* Additionally, I improved my understanding of error handling in Python using try and except. Instead of allowing the script to crash when a request fails, I handled exceptions gracefully and printed a clear (ERROR) message for failed URLs.

* Finally, I learned how to use requests.Session() to reuse connections, which is more efficient than making individual requests without a session.



### Challenges Faced

* During this task, one challenge I encountered was handling URLs that were incomplete or missing a scheme. This initially caused request failures until I added a normalization step.

* Another challenge was dealing with servers that reject HEAD requests. At first, I was confused by unexpected status codes, but after investigating, I implemented a fallback to GET, which made the script more robust.