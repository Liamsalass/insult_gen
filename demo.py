import r_data_scraper as ds
import requests



secret = 'WbFmtLt970ZnlguOqAaXGNUFu5XzrQ'
client_id = '1xk7tjG6z2mAYOL8cPEWEg'

# create a scraper object
roast_me_test = ds.scraper(client_id=client_id, client_secret=secret, username='SandInMyHoles', user_agent='demo')

# get the data
roast_me_test.get_all_data(num_top_posts=1)

# store the data
roast_me_test.store_data()