import itertools

import requests
import json
from AllegroRestApi import AllegroRestApi
from GetIdsOfAllegroCategories import GetIdsOfAllegroCategories

class BestSellingItems():
    def merge_list(self, auction_list):
        merged_list = list(itertools.chain(*auction_list))
        return merged_list

    def make_request(self, category_id, offset, limit=100):
        allegro_api = AllegroRestApi()
        headers = {}
        headers['charset'] = 'utf-8'
        headers['Accept-Language'] = 'pl-PL'
        headers['Content-Type'] = 'application/json'
        headers['Api-Key'] = allegro_api.api_key
        headers['Accept'] = 'application/vnd.allegro.public.v1+json'
        headers['Authorization'] = "Bearer {}".format(allegro_api.access_token)

        parameters = {'category.id': '{}'.format(category_id),
                      'sort': '{}'.format('-popularity'),
                      'limit': '{}'.format(limit),
                      'offset': '{}'.format(offset)}
        with requests.Session() as session:
            session.headers.update(headers)
            response = session.get(allegro_api.DEFAULT_API_URL + '/offers/listing',
                                   params=parameters).json()
            return response

    def get_promoted_items(self, category_id):
        promoted_items_list = []
        response = self.make_request(category_id, offset=0)
        promoted_items = response['items']['promoted']
        for item in promoted_items:
            if item['sellingMode']['format'] == 'BUY_NOW':
                promoted_items_list.append(item)
        return promoted_items_list

    def get_regular_items(self, category_id):
        response = self.make_request(category_id, offset=0)
        list_of_regular_items = []
        regular_items = response['items']['regular']
        offset = 101
        while(1):
            if regular_items:
                for item in regular_items:
                    if item['sellingMode']['format'] == 'BUY_NOW':
                        list_of_regular_items.append(item)
                number_of_items = len(regular_items)
                if number_of_items < 100:
                    number_of_missing_items = 100 - number_of_items
                    response = self.make_request(category_id, offset, limit=number_of_missing_items)
                    regular_items = response['items']['regular']
                    for item in regular_items:
                        if item['sellingMode']['format'] == 'BUY_NOW':
                            list_of_regular_items.append(item)
                break
            else:
                response = self.make_request(category_id, offset)
                offset += 100
                regular_items = response['items']['regular']
        # try:
        #     list_of_regular_items = self.merge_list(list_of_regular_items)
        # except:
        #     pass
        return list_of_regular_items

    def get_auction_id(self, auction):
        return auction['id']

    def get_auction_name(self, auction):
        return auction['name']

    def get_auction_url(self, auction_id):
        return 'https://allegro.pl/oferta/{}'.format(auction_id)

    def get_image_url(self, auction):
        image_url = auction['images'][0]
        return image_url['url']

    def get_product_price(self, auction):
        selling_mode_field = auction['sellingMode']
        price_field = selling_mode_field['price']
        product_price = price_field['amount']
        return product_price

    def get_lowest_delivery_price(self, auction):
        delivery_field = auction['delivery']
        lowest_price_field = delivery_field['lowestPrice']
        lowest_delivery_price = lowest_price_field['amount']
        return lowest_delivery_price

    def get_number_of_sold_items(self, auction):
        selling_mode_field = auction['sellingMode']
        number_of_sold_items = selling_mode_field['popularity']
        return number_of_sold_items

    def get_category_id(self, auction):
        category_field = auction['category']
        category_id = category_field['id']
        return category_id

    def get_category_name(self, category_id):
        category_resolver = GetIdsOfAllegroCategories()
        category_field = category_resolver.get_categories_by_id(category_id)
        category_name = category_field['name']
        return category_name


    def create_auction_fields_dict(self, auction_name, auction_url,
                                   image_url, product_price, lowest_delivery_price,
                                   number_of_sold_items, category_id, category_name):
        auction_fields_dict = {}
        auction_fields_dict['auction_name'] = auction_name
        auction_fields_dict['auction_url'] = auction_url
        auction_fields_dict['image_url'] = image_url
        auction_fields_dict['product_price'] = float(product_price)
        auction_fields_dict['lowest_delivery_price'] = float(lowest_delivery_price)
        auction_fields_dict['number_of_sold_items'] = float(number_of_sold_items)
        auction_fields_dict['category_id'] = category_id
        auction_fields_dict['category_name'] = category_name
        return auction_fields_dict

    def get_parsed_auction_list(self, auction_list):
        parsed_auction_list = []
        for auction in auction_list:
            auction_id = self.get_auction_id(auction)
            auction_name = self.get_auction_name(auction)
            auction_url = self.get_auction_url(auction_id)
            image_url = self.get_image_url(auction)
            product_price = self.get_product_price(auction)
            lowest_delivery_price = self.get_lowest_delivery_price(auction)
            number_of_sold_items = self.get_number_of_sold_items(auction)
            category_id = self.get_category_id(auction)
            category_name = self.get_category_name(category_id)
            auction_fields_dict = self.create_auction_fields_dict(auction_name, auction_url,
                                                                  image_url, product_price, lowest_delivery_price,
                                                                  number_of_sold_items, category_id, category_name)

            parsed_auction_list.append(auction_fields_dict)

            # parsed_auction_list_json = json.dumps(parsed_auction_list, ensure_ascii=False)
        return parsed_auction_list
