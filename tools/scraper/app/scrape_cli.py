# web_scraper_cli.py
import argparse
import requests
import json

class WebScraperCLI:
    def __init__(self):
        """
        Initialize the WebScraperCLI class and configure the argument parser.
        """
        self.parser = argparse.ArgumentParser(description='Web Scraper Tool - Scrape data from a webpage.')
        self.configure_arguments()

    def configure_arguments(self):
        """
        Configure the command-line arguments for the WebScraperCLI.
        """
        self.parser.add_argument('url', help='URL of the webpage to be scraped.')
        self.parser.add_argument('-o', '--output_file', help='Path to the output JSON file. If not provided, the result will be printed on the screen.', default=None)
        self.parser.add_argument('-u', '--api_url', help='URL of the web scraper API. If not provided, the default API URL will be used.', default='http://127.0.0.1:5000/scrape')

    def run(self):
        """
        Parse the command-line arguments and process the URL using the web scraper API.
        """
        args = self.parser.parse_args()
        result = self.scrape_url(args.url, args.api_url)

        if args.output_file:
            with open(args.output_file, 'w') as output_file:
                json.dump(result, output_file, indent=2)
        else:
            print(json.dumps(result, indent=2))

    def scrape_url(self, url, api_url):
        """
        Send the URL to the web scraper API and return the scraped data.
        """
        response = requests.post(api_url, json={"url": url})
        response.raise_for_status()
        return response.json()

if __name__ == '__main__':
    web_scraper_cli = WebScraperCLI()
    web_scraper_cli.run()
