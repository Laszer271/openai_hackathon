from amazondata.search_result_extractor import SearchResultExtractor

product_description = 'perfume for men'

search_result_extractor = SearchResultExtractor()

data = search_result_extractor.search(product_description, 3)
product_name = data['products'][0]['title']
product_url = data['products'][0]['url']
print(product_name)
print(product_url)
