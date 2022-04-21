import requests
import json
import os
import urllib3
import sys
import wget

image_url = 'https://cf.shopee.vn/file/'
offset = 1
count = 0

input_url = input('Enter url: ')

# Get shopid, itemid
try:
    ids = input_url.split('/')[-1]
    shopid = ids.split('.')[1]
    itemid = ids.split('.')[2].split('?')[0]
    # Get number of reviews with image
    limit = 500
    api_url = 'https://shopee.vn/api/v2/item/get_ratings?filter=3&flag=1&itemid=' + str(itemid) + '&limit=' + str(limit) + '&offset=1&shopid=' + str(shopid) + '&type=0'
    res = requests.get(api_url)
    data = json.loads(res.text)
    numOfImages = int(data['data']['item_rating_summary']['rcount_with_image'])
    # Create folder
    folder_name = 'shopee_' + str(shopid) + '_' + str(itemid)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    # Get reviews
    limit = 50
    for i in range(0, numOfImages, limit):
        api_url = 'https://shopee.vn/api/v2/item/get_ratings?filter=3&flag=1&itemid=' + str(itemid) + '&limit=' + str(limit) + '&offset=' + str(offset) + '&shopid=' + str(shopid) + '&type=0'
        res = requests.get(api_url)
        data = json.loads(res.text)
        orders = data['data']['ratings']
        for order in orders:
            for image in order['images']:
                image_url_req = image_url + image
                image_name = str(image) + '.jpg'
                # print(image_url_req, end='\r')
                try:
                    image_data = requests.get(image_url, stream=True)
                    # with open(folder_name + '/' + image_name, 'wb') as handler:
                    wget.download(image_url_req, out=folder_name + '/' + image_name)
                except:
                    print('Error: ' + image_url)
                print('\tDownloaded: ' + image_name + '\t' + str(count) + '/' + str(numOfImages), end='\r')
                count += 1
        offset += limit
except:
    print('Cannot get shopid or itemid from url')
    sys.exit()
