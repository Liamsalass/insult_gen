import r_data_scraper as ds
import requests



secret = 'WbFmtLt970ZnlguOqAaXGNUFu5XzrQ'
client_id = '1xk7tjG6z2mAYOL8cPEWEg'

# create a scraper object
roast_me_test = ds.scraper(client_id=client_id, client_secret=secret, username='SandInMyHoles', user_agent='demo')

# get the data
num_posts = input('Enter the number of top posts to scrape: ')
show_images = input('Show images? (y/n): ')
if show_images == 'y':
    show_images = True
else:
    show_images = False

roast_me_test.get_all_data(num_top_posts=int(num_posts), show_images=show_images)

# save the data
roast_me_test.save_data_hdf5()

# load the data
roast_me_test.load_data_hdf5()

# Save to csvp
roast_me_test.save_data()

# show the data
roast_me_test.show_data()

#show images 
roast_me_test.show_image_range(0,4)
