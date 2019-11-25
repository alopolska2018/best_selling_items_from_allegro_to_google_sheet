from GoogleSheet import GoogleSheet
from BestSellingItems import BestSellingItems
from GetIdsOfAllegroCategories import GetIdsOfAllegroCategories

def add_items_to_gsheet(auction_list):
    url_fields_list = []
    image_url_fields_list = []
    product_price_fields_list = []
    lowest_delivery_price_fields_list = []
    number_of_sold_items_fields_list = []
    category_id_fields_list = []
    category_name_fields_list = []

    for auction in auction_list:
        url_fields_list.append(get_url_field(auction))
        image_url_fields_list.append(get_image_url_field(auction))
        product_price_fields_list.append(get_product_price_field(auction))
        lowest_delivery_price_fields_list.append(get_lowest_delivery_price_field(auction))
        number_of_sold_items_fields_list.append(get_number_of_sold_items(auction))
        category_id_fields_list.append(get_category_id(auction))
        category_name_fields_list.append(get_category_name(auction))


    last_row = len(url_fields_list) + 1
    google_sheet.update_rows_in_batch(url_fields_list, 2, 1, last_row, 1)
    google_sheet.update_rows_in_batch(image_url_fields_list, 2, 2, last_row, 2)
    google_sheet.update_rows_in_batch(product_price_fields_list, 2, 3, last_row, 3)
    google_sheet.update_rows_in_batch(lowest_delivery_price_fields_list, 2, 4, last_row, 4)
    google_sheet.update_rows_in_batch(number_of_sold_items_fields_list, 2, 5, last_row, 5)
    google_sheet.update_rows_in_batch(category_name_fields_list, 2, 6, last_row, 6)
    google_sheet.update_rows_in_batch(category_id_fields_list, 2, 7, last_row, 7)

def get_number_of_sold_items(auction):
    return auction['number_of_sold_items']

def get_lowest_delivery_price_field(auction):
    return auction['lowest_delivery_price']


def get_product_price_field(auction):
    return auction['product_price']


def get_category_id(auction):
    return auction['category_id']

def get_category_name(auction):
    return auction['category_name']

def get_image_url_field(auction):
    image_url = auction['image_url']
    image_field = '=IMAGE(\"{}\")'.format(image_url)
    return image_field


def get_url_field(auction):
    auction_name = auction['auction_name']
    auction_url = auction['auction_url']
    auction_url_field = '=HYPERLINK(\"{}";"{}\")'.format(auction_url, auction_name)
    return auction_url_field

category_resolver = GetIdsOfAllegroCategories()
allegro = BestSellingItems()

category_id = input('Category id: ')
category_field = category_resolver.get_categories_by_id(category_id)
category_name = category_field['name']

promoted_items = allegro.get_promoted_items(category_id)
regular_items = allegro.get_regular_items(category_id)

promoted_items_parsed_list = allegro.get_parsed_auction_list(promoted_items)
regular_items_parsed_list = allegro.get_parsed_auction_list(regular_items)

joined_list = promoted_items_parsed_list + regular_items_parsed_list
worksheet_name = '{}/{}'.format(category_name, category_id)
google_sheet = GoogleSheet('towar z cn', worksheet_name, '300', '9')
add_items_to_gsheet(joined_list)
print('Google worksheet created, named: {}'.format(category_id))
