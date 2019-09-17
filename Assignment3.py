#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Week 3 Assignment - Text Processing

"""
import argparse
import urllib.request
import urllib.error
import csv
import re
import datetime

#urlsite = 'http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv'
imageCount = {'images': 0, 'non-images': 0}
myfile = 'Weblog_Data.csv'
searchBrowser = {}


def downloadData(url):
    """A function that takes a csv url parameter using agrparse
    to test the validity of the url.
    """
    response = urllib.request.urlopen(url)
    csvfile = response.read()
    csv_str = str(csvfile)
    lines = csv_str.split("\\n")
    dest_url = 'Weblog_Data.csv'
    fx = open(dest_url, 'w')

    for line in lines:
        fx.write(line + '\n')

    fx.close()

    return dest_url


def imageHits(filename):
    """Process the data in csv file to search for all the hits of image files
    Args:
        filename (file): file used to search for re expressions
    Returns:
        Str: string with image count and percent of count.
    """

    with open(filename, 'rt') as csvFile:

        reader = csv.reader(csvFile)

        for row in reader:
            for element in row:
                if re.search('(jpg|png|gif)$', element, re.IGNORECASE):
                    imageCount['images'] += 1
                else:
                    imageCount['non-images'] += 1

    return ('   Image requests account for {:.2f} percent of all requests.'.
            format(imageCount['images'] / sum(imageCount.values()) * 100))


def popularBrowser(filename):
    """Process the data in csv file to search for the most popular browser
    Args:
        filename (file): file used to search for re expressions
    Returns:
        Str: string with most popular browser
    """

    with open(filename, 'rt') as csvFile:

        reader = csv.reader(csvFile)

        for row in reader:
            for element in row:
                if re.search('(safari)\w*', element, re.IGNORECASE):
                    try:
                        searchBrowser['Safari'] += 1
                    except KeyError:
                        searchBrowser['Safari'] = 1
                elif re.search('(firefox)\w*', element, re.IGNORECASE):
                    try:
                        searchBrowser['firefox'] += 1
                    except KeyError:
                        searchBrowser['firefox'] = 1
                elif re.search('(Internet Explorer)\w*', element, re.IGNORECASE):
                    try:
                        searchBrowser['Internet Explorer'] += 1
                    except KeyError:
                        searchBrowser['Internet Explorer'] = 1
                elif re.search('(chrome)\w*', element, re.IGNORECASE):
                    try:
                        searchBrowser['chrome'] += 1
                    except KeyError:
                        searchBrowser['chrome'] = 1

        v = list(searchBrowser.values())
        k = list(searchBrowser.keys())

        return '   The most popular browser of the day is {}.'.format(k[v.index(max(v))])


def main():
    #Use the argparse module to allow the user to send a url parameter to the script
    parser = argparse.ArgumentParser(description='my url')
    #Add the parameters
    parser.add_argument('url', help="Enter your url to download data")
    #Parse the arguments
    args = parser.parse_args()

    #url input errors
    try:
        csvData = downloadData(args.url)
    except urllib.error.HTTPError as e:
        print('   There is an HTTP error.', e.code)
    except urllib.error.URLError as e:
        print('   There is a URL error.', e.reason)
    except ValueError:
        print('   The URL provided is in invalid format.')
    else:
        print(imageHits(myfile))
        print(popularBrowser(myfile))


if __name__ == '__main__':
    main()

