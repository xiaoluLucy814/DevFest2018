## -*- coding: utf-8 -*-
"""
Yelp Fusion API code sample.
This program demonstrates the capability of the Yelp Fusion API
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.
Please refer to http://www.yelp.com/developers/v3/documentation for the API
documentation.
This program requires the Python requests library, which you can install via:
`pip install -r requirements.txt`.
Sample usage of the program:
`python sample.py --term="bars" --location="San Francisco, CA"`
"""
# @ Author:Zeyi Liu
# @ Date: Feb 3rd
# @ Email: zl2753@columbia.edu

from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
import pandas as pd

# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode

# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# You can find it on
# https://www.yelp.com/developers/v3/manage_app
API_KEY = "nB49juCDUUkRnYCtolvtlfUeU3hZhpnSHwXhahAh76Nm-VfyOzoCYh0gw4uC78nuPow6gLbX0mt5Ezra" \
          "AthRUJegJOAtMJFYGn9YsY1MZsXa1DrBpK1-ZD8GHytRXHYx"

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

# Defaults for our simple example.
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'Morningside Heights'
SEARCH_LIMIT = 20



def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'sort_by': "distance"
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


def query_api(term, location):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    business_ids = [i['id'] for i in businesses]
    for i in range(0, 19):
        print(u'{0} businesses found, querying business info ' \
              'for "{1}" ...'.format(
            len(businesses), business_ids[i]))
    responses = [get_business(API_KEY, business_id) for business_id in business_ids]

    return responses

    '''
    for i in range(0, 29):
        business_id = businesses[i]['id']
        print(u'{0} businesses found, querying business info '\
        'for result "{1}" ...'.format(
            len(businesses), business_id))
        response = get_business(API_KEY, business_id)
        
        print(u'Result for business "{0}" found:'.format(business_id))
        pprint.pprint(response, indent=2)

    '''


def create_new_entry(metadata):
    """
    Reads in the metadata from a response from query_api and stores individual entries into a pandas DataFrame

    Args:
        param1: metadata (dict) stores the response from query_api

    Returns:
        pandas.DataFrame with one entry
    """

    new_entry = dict()
    #new_entry['id'] = metadata.get('id','empty')
    #if a key value is not found, return empty
    new_entry['name'] = metadata.get('name','empty')
    new_entry['review_count'] = metadata.get('review_count','empty')
    new_entry['rating'] = metadata.get('rating','empty')
    new_entry['price'] = metadata.get('price','empty')


    if(metadata.get('hours','empty') == 'empty'):
        new_entry['open'] = False
    else:
        new_entry['open'] = metadata['hours'][0]['is_open_now']

    """categories = dict()
    for i in range(len(metadata['categories'])):
        categories[i] = metadata['categories'][i]
"""
    new_entry['categories'] = metadata['categories'][0]['alias']

    file = json.dumps(new_entry)
    f = open("new_entry.json", "a")
    f.write(file+'\n')
    f.close()

    #return pd.DataFrame(new_entry, index=[0])


def get_yelp_info(term, location):
    """
    Reads in a list of responses from query_api and stores the entries all in a pandas DataFrame using create_new_entry

    Args:
        param1: responses (list) stories responses from query_api

    Returns:
        pandas.DataFrame with all responses as entries
    """
    responses = query_api(term, location)
    [create_new_entry(response) for response in responses]



'''
def create_category_entry(metadata):
    """
    Method to record the categories of restaurant the response from query_api in a pandas.DataFrame

    Args:
        param1: metadata (dict) stores the response from query_api

    Returns:
        pandas.DataFrame with entries with the 'id' of the restaurant and the associated categorization
    """
    new_entry = dict()
    categories = dict()
    new_entry['id'] = metadata['id']
    for i in range(len(metadata['categories'])):
        categories[i] = metadata['categories'][i]
    new_entry['categories'] = categories
    return pd.DataFrame(new_entry)


def create_category_data_frame(term, location):
    """
    Method to record the categories of restaurants the responses from query_api in a pandas.DataFrame

    Args:
        param1: responses (list) stories responses from query_api

    Returns:
        pandas.DataFrame with entries with the 'id's of the restaurants and their associated categorizations
    """
    responses = query_api(term, location)
    output = pd.concat([create_category_entry(response) for response in responses])
    output = output.reset_index(drop=True)
    return output


def collate_data(df, location_ids):
    """
    Method to take the category_DataFrame and store it as a dictionary where the key is the location_id
    and the value is a list of the labels that was categorized.

    Args:
        param1: df (pandas.DataFrame) the input category dataFrame
        param2: location_ids (list, array) unique identifier for the restaurant

    Returns
        Dictionary: a dictionary where the key is the location_id and the value
        is a list of the labels that was categorized.
    """

    output = dict()

    for loc in location_ids:
        aliases = []
        for i in df[df['id'] == loc]['categories']:
            aliases.append(i['alias'])
        output[loc] = aliases

    return output


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        query_api(input_values.term, input_values.location)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    main()
    
'''