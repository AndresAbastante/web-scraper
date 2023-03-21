import pandas as pd
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
import os

url='https://www.ebay.com/mye/myebay/v2/purchase?page=1&moduleId=122169&mp=purchase-module-v2&type=v2&pg=purchase'

pd.set_option('display.max_rows', 500)
APPLICATION_ID = os.environ.get('API_KEY')
def get_results(payload):
    try:
        api = Finding(siteid='EBAY-GB', appid=APPLICATION_ID, config_file=None)
        response = api.execute('findItemsAdvanced', payload)
        return response.dict()
    except ConnectionError as e:
        print(e)
        print(e.response.dict())

payload = {
        'keywords': '12 string bass guitar', 
        'categoryId': ['3858'],
        'itemFilter': [
            {'name': 'LocatedIn', 'value': 'GB'},
        ],
        'sortOrder': 'StartTimeNewest',
}

results = get_results(payload)

def get_total_pages(results):
    '''Get the total number of pages from the results'''
    if results:
        return int(results.get('paginationOutput').get('totalPages'))
    else:
        return

def search_ebay(payload):
    '''parse the response - results and concatentate to the dataframe'''
    results = get_results(payload)
    total_pages = get_total_pages(results)
    items_list = results['searchResult']['item']
        
    i = 2
    while(i <= total_pages):
        payload['paginationInput'] = {'entriesPerPage': 100, 'pageNumber': i}        
        results = get_results(payload)
        items_list.extend(results['searchResult']['item'])
        i += 1
        
    df_items = pd.DataFrame(columns=['itemId', 'title', 'viewItemURL', 'galleryURL', 'location', 'postalCode',
                                 'paymentMethod''listingType', 'bestOfferEnabled', 'buyItNowAvailable',
                                 'currentPrice', 'bidCount', 'sellingState'])

    for item in items_list:
        row = {
            'itemId': item.get('itemId'),
            'title': item.get('title'),
            'viewItemURL': item.get('viewItemURL'),
            'galleryURL': item.get('galleryURL'),
            'location': item.get('location'),
            'postalCode': item.get('postalCode'),
            'paymentMethod': item.get('paymentMethod'),        
            'listingType': item.get('listingInfo').get('listingType'),
            'bestOfferEnabled': item.get('listingInfo').get('bestOfferEnabled'),
            'buyItNowAvailable': item.get('listingInfo').get('buyItNowAvailable'),
            'currentPrice': item.get('sellingStatus').get('currentPrice').get('value'),
            'bidCount': item.get('bidCount'),
            'sellingState': item.get('sellingState'),
        }

        ## Deprecation note - don't use append
        '''https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.append.html'''
        
        new_df = pd.DataFrame([row])
        df_items = pd.concat([df_items, new_df],axis=0, ignore_index=True)


    return df_items

df = search_ebay(payload)