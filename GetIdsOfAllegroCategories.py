from AllegroRestApi import AllegroRestApi
import requests

class GetIdsOfAllegroCategories():
    def __init__(self):
        self.lista = []
    def get_main_categories(self):
        allegro_api = AllegroRestApi()
        headers = {}
        headers['charset'] = 'utf-8'
        headers['Accept-Language'] = 'pl-PL'
        headers['Content-Type'] = 'application/json'
        headers['Api-Key'] = allegro_api.api_key
        headers['Accept'] = 'application/vnd.allegro.public.v1+json'
        headers['Authorization'] = "Bearer {}".format(allegro_api.access_token)

        with requests.Session() as session:
            session.headers.update(headers)
            response = session.get(allegro_api.DEFAULT_API_URL + '/sale/categories').json()
            return response

    def get_categories_by_parent_id(self, parent_id):
        allegro_api = AllegroRestApi()
        headers = {}
        headers['charset'] = 'utf-8'
        headers['Accept-Language'] = 'pl-PL'
        headers['Content-Type'] = 'application/json'
        headers['Api-Key'] = allegro_api.api_key
        headers['Accept'] = 'application/vnd.allegro.public.v1+json'
        headers['Authorization'] = "Bearer {}".format(allegro_api.access_token)

        parameters = {'parent.id': '{}'.format(parent_id)}

        with requests.Session() as session:
            session.headers.update(headers)
            response = session.get(allegro_api.DEFAULT_API_URL + '/sale/categories', params=parameters).json()
            return response

    def get_categories_by_id(self, category_id):
        allegro_api = AllegroRestApi()
        headers = {}
        headers['charset'] = 'utf-8'
        headers['Accept-Language'] = 'pl-PL'
        headers['Content-Type'] = 'application/json'
        headers['Api-Key'] = allegro_api.api_key
        headers['Accept'] = 'application/vnd.allegro.public.v1+json'
        headers['Authorization'] = "Bearer {}".format(allegro_api.access_token)

        with requests.Session() as session:
            session.headers.update(headers)
            response = session.get(allegro_api.DEFAULT_API_URL + '/sale/categories/{}'.format(category_id)).json()
            return response

    def get_list_of_all_child_categories(self, id):
            child_category = self.get_categories_by_parent_id(id)
            for item in child_category['categories']:
                self.lista.append(item)
                id = item['id']
                condition = len(child_category['categories'])
                if condition != 0:
                    self.get_categories_by_parent_id(id)

    def test(self, parent_id):
        ids_list = []
        child_category = self.get_categories_by_parent_id(parent_id)
        for id in child_category['categories']:
            id = id['id']
            self.get_list_of_all_child_categories(id)

    # def get_list_of_all_categories(self, main_categories_id):
    #     main_categories = self.get_categories_by_parent_id(main_categories_id)
    #     for item in main_categories['categories']:
    #         parent_category_id = item['id']


            #
            # test1 = self.get_categories_by_parent_id(parent_category_id)
            # for item in test1['categories']:
            #     parent_category_id = item['id']
            #     test2 = self.get_categories_by_parent_id(parent_category_id)
            #     print(test2)
            #


