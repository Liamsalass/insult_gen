from r_data_scraper import scrapper

# create a scraper object
roast_me_test = scrapper(client_id= , client_secret= , user_agent= )

# get the data
roast_me_test.get_all_data('RoastMe', 100, 5, (256, 256), 'roast_me_test')