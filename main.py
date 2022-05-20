import requests
import json
import os

def _get_image_from_shopee_url(url):
    try:
        shop_id = url.split('.')[2]
        item_id = url.split('.')[3].split('?')[0]
        url = 'https://shopee.vn/api/v2/item/get_ratings?filter=3&flag=1&itemid='+item_id+'&shopid='+shop_id+'&type=0'
        # list_of_images = []
        data = json.loads(requests.get(url).text)
        ratings = data['data']['ratings']
        list_of_media = []
        for i in ratings:
            list_of_images = [x for x in i['images']]
            list_of_videos = [x['url'] for x in i['videos']]
            list_of_media.append(list_of_images + list_of_videos)
        return list_of_media
    except:
        print('Error')

def _create_html_file(list_of_images):
    html = '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><title>Bootstrap demo</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet"  integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor"  crossorigin="anonymous"/></head><body><div class="container"><div class="row mt-3">'
    for image in list_of_images:
        for img in image:
            if img.split('.')[-1] == 'mp4':
                html += '<div class = "col-sm-3" ><div class = "card mt-3" ><iframe class="embed-responsive-item" src="'+img+'" allowfullscreen></iframe></div ></div >'
            else:
                html += '<div class = "col-sm-3" ><div class = "card mt-3" ><img src = "https://cf.shopee.vn/file/'+img+'" class = "card-img-top" ></div ></div >'
    html += '</div ></div ><script  src = "https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js" integrity = "sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2" crossorigin = "anonymous"> < /script ></body></html>'

    with open('index.html', 'w') as f:
        f.write(html)
    print('Done')

if __name__=='__main__':
    url = input('Enter the url of the product: ')
    _create_html_file(_get_image_from_shopee_url(url))
