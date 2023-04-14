import praw
import csv
from PIL import Image
import requests
from io import BytesIO
from base64 import b64encode
from tqdm import tqdm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import h5py



class scraper:
    def __init__(self, client_id='1xk7tjG6z2mAYOL8cPEWEg', client_secret='WbFmtLt970ZnlguOqAaXGNUFu5XzrQ', username='SandInMyHoles', user_agent='test', hdf5_file_name='data.hdf5'):
        self.hdf5_file_name = hdf5_file_name


        # authenticate with Reddit

        password = input('Enter your Reddit password: ')
        
        if password == None:
            print('Error: Password is required')
            exit()
        try:
            self.reddit = praw.Reddit(client_id=client_id,
                                      client_secret=client_secret,
                                      username=username,
                                      password=password,
                                      user_agent=user_agent)
        except Exception as e:
            print(e)
            print('Error: Could not authenticate with Reddit')
            exit()

        self.data = None

        # set up hdf5 group
        self.hdf = h5py.File(hdf5_file_name, 'w')
      
        self.scrapedata = self.hdf.create_group('/scrapedata')


    def store_data(self, data_set_name='default'):
        if self.data is None:
            print('Error: No data to store')
            return
        
        # store data in hdf5 file
        self.scrapedata.create_dataset(data_set_name, data=self.data)



        
            

    def get_all_data(self, subreddit_name='RoastMe', num_top_posts=3, num_comments=5, image_size=(100,100)):
        print('Scraping data from subreddit: ' + subreddit_name)
        print('Number of top posts to scrape: ' + str(num_top_posts))
        print('Number of top comments to scrape: ' + str(num_comments))
        print('Image size: ' + str(image_size))
        print('=' * 50)

        # create a pandas dataframe to store the data
        df = pd.DataFrame(columns=['title', 'image', 'comments'])

        # get the top posts from the subreddit
        subreddit = self.reddit.subreddit(subreddit_name)
        top_posts = subreddit.top(limit=num_top_posts)

        # loop through the top posts and write the data to the dataframe
        for post in tqdm(top_posts):
            # get the post title
            title = post.title.replace('\n', ' ')

            # get the post image and resize it
            if post.url.endswith(('jpg', 'png', 'gif')):
                response = requests.get(post.url)
                img = Image.open(BytesIO(response.content))
                img = img.resize(image_size)
                img_array = np.array(img)
                img_pixels = img_array.flatten().tolist()

                # display the image using Matplotlib
                if num_top_posts < 5:
                    plt.imshow(img)
                    plt.ion()
                    plt.show()
                    plt.pause(2)
                    plt.close()
            else:
                img_pixels = []

            

            # get the top comments
            if num_comments < 4:
                # faster code if there are less than 3 comments
                comments = post.comments
                comments_sorted = sorted(comments, key=lambda comment: comment.score, reverse=True)[:num_comments]
                top_comments = [comment.body.replace('\n', ' ') for comment in comments_sorted]
            else:
                # slower code if there are more than 3 comments
                comments = post.comments
                comments.replace_more(limit=num_comments)
                comments_sorted = sorted(comments, key=lambda comment: comment.score, reverse=True)[:num_comments]
                top_comments = [comment.body.replace('\n', ' ') for comment in comments_sorted]
            
            # add the data to the dataframe
            df = df.append({'title': title, 'image': img_pixels, 'comments': top_comments}, ignore_index=True)       

        # transfor dataframe to have not object types
        df['image'] = df['image'].apply(lambda x: np.array(x))
        df['comments'] = df['comments'].apply(lambda x: np.array(x))
        
        self.data = df     

        return df

        

def main():
    test = input('General test? (y/n): ')
    
    if test == 'n':
        # create an instance of the scraper class
        reddit_scraper = scraper('client_id', 'client_secret', 'user_agent')
        # user inputs parameters to scrape data
        subreddit_name = input('Enter the name of the subreddit: ')
        num_top_posts = int(input('Enter the number of top posts to scrape: '))
        num_comments = int(input('Enter the number of top comments to scrape: '))
        image_size = (int(input('Enter the width of the image: ')), int(input('Enter the height of the image: ')))
        file_name = input('Enter the name of the CSV file: ')
        # scrape the data
        reddit_scraper.get_all_data(subreddit_name, num_top_posts, num_comments, image_size, file_name)
    else:
        reddit_scraper= scraper()
        reddit_scraper.get_all_data()
        reddit_scraper.store_data()


if __name__ == '__main__':
    main()
