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
import praw



class scraper:
    def __init__(self, client_id='1xk7tjG6z2mAYOL8cPEWEg', client_secret='WbFmtLt970ZnlguOqAaXGNUFu5XzrQ', username='SandInMyHoles', user_agent='test', hdf5_file_name='data.hdf5'):
        self.hdf5_file_name = hdf5_file_name


        # authenticate with Reddit

        while True:
            password = input('Enter your Reddit password: ')

            if password == '':
                print('Error: Password is required')
                continue
            
            try:
                self.reddit = praw.Reddit(client_id=client_id,
                                        client_secret=client_secret,
                                        username=username,
                                        password=password,
                                        user_agent=user_agent)
                break
            except Exception as e:
                print(e)
                print('Error: Could not authenticate with Reddit')
                exit()

        self.data = None


 
        
    def get_all_data(self, subreddit_name='RoastMe', num_top_posts=3, num_comments=5, image_size=(100,100), show_images=False):
        print('Scraping data from subreddit: ' + subreddit_name)
        print('Number of top posts to scrape: ' + str(num_top_posts))
        print('Number of top comments to scrape: ' + str(num_comments))
        print('Image size: ' + str(image_size))
        print('=' * 50)

        df = pd.DataFrame(columns=['title'] + ['comment_' + str(i) for i in range(num_comments)] + ['p' + str(i) for i in range(image_size[0] * image_size[1] * 3)])


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
                if show_images:
                    plt.imshow(img)
                    plt.ion()
                    plt.show()
                    plt.pause(2)
                    plt.close()
            else:
                img_pixels = [0] * image_size[0] * image_size[1] * 3
            

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
            row_data = [title] + top_comments + img_pixels
            row_length = len(row_data)
            if row_length == len(df.columns):
                df.loc[len(df)] = row_data       

        # store the data in the class
        self.data = df     
        return df

    def return_img(self, index):
        # get the image from the dataframe
        img = self.data.iloc[index, 3:].values
        img = img.reshape((100, 100, 3))
        return img
    
    def return_comments(self, index, num_comments=5):
        # get the comments from the dataframe
        comments = self.data.iloc[index, 1:num_comments+1].values
        return comments
    
    def return_title(self, index):
        # get the title from the dataframe
        title = self.data.iloc[index, 0]
        return title
    
    def save_data(self, file_name='data.csv'):
        # save the data to a CSV file
        self.data.to_csv(file_name, index=False)
        print('Data saved to ' + file_name)

    def save_data_hdf5(self, file_name='data.hdf5'):
        # save the data to an HDF5 file
        self.data.to_hdf(file_name, key='df', mode='w')
        print('Data saved to ' + file_name)

    def load_data(self, file_name='data.csv'):
        # load the data from a CSV file
        self.data = pd.read_csv(file_name)
        print('Data loaded from ' + file_name)

    def load_data_hdf5(self, file_name='data.hdf5'):
        # load the data from an HDF5 file
        self.data = pd.read_hdf(file_name)
        print('Data loaded from ' + file_name)

    def show_data(self):
        # display the data
        print(self.data)
        

        

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
    


if __name__ == '__main__':
    main()
