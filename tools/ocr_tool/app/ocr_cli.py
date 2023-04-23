"""
example usage: python ocr_cli.py input_image.jpg
"""

import argparse
import requests
import os
import json

class OCR_CLI:
    def __init__(self):
        """
        Initialize the OCR_CLI class and configure the argument parser.
        """
        self.parser = argparse.ArgumentParser(description='OCR Tool - Extract text from images.')
        self.configure_arguments()

    def configure_arguments(self):
        """
        Configure the command-line arguments for the OCR_CLI.
        """
        self.parser.add_argument('input_file', help='Path to the input image file.')
        self.parser.add_argument('-o', '--output_file', help='Path to the output text file. If not provided, the result will be printed on the screen.', default=None)
        # self.parser.add_argument('-u', '--api_url', help='URL of the custom OCR API. If not provided, the default OCR API will be used.', default='http://localhost:5000/ocr')
        self.parser.add_argument('-u', '--api_url', help='URL of the custom OCR API. If not provided, the default OCR API will be used.', default='http://127.0.0.1:5000/ocr')


    def run(self):
        """
        Parse the command-line arguments and process the input image using the OCR API.
        """
        args = self.parser.parse_args()
        result = self.process_image(args.input_file, args.api_url)

        if args.output_file:
            with open(args.output_file, 'w') as output_file:
                output_file.write(result)
        else:
            print(result)

    def process_image(self, input_file, api_url):
        """
        Send the input image file to the OCR API and return the extracted text.
        """
        with open(input_file, 'rb') as file:
            response = requests.post(api_url, files={'file': file})
            response.raise_for_status()
            return response.text

if __name__ == '__main__':
    ocr_cli = OCR_CLI()
    ocr_cli.run()
