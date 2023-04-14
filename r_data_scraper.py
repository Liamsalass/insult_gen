import praw
import csv
from PIL import Image
import requests
from io import BytesIO
from base64 import b64encode
from tqdm import tqdm


class scraper:
    def __init__(self, client_id, client_secret, user_agent):
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)



    def get_all_data(self, subreddit_name, num_top_posts, num_comments, image_size, file_name):

        if not file_name.endswith('.csv'):
            file_name += '.csv'


        # create a CSV file and write the headers
        csv_file = open(file_name, 'w', newline='', encoding='utf-8')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Title', 'Image URL', 'Top Comment 1', 'Top Comment 2', 'Top Comment 3', 'Top Comment 4', 'Top Comment 5'])

        # get the top posts from the subreddit
        subreddit = self.reddit.subreddit(subreddit_name)
        top_posts = subreddit.top(limit=num_top_posts)

        

        # loop through the top posts and write the data to the CSV file
        for post in tqdm(top_posts):
            # get the post title
            title = post.title.replace('\n', ' ')
            
            # get the post image URL and resize the image
            image_url = post.url if post.url.endswith(('jpg', 'png', 'gif')) else ''


            try:
                response = requests.get(image_url)
                image = Image.open(BytesIO(response.content))
                image = image.resize(image_size)
                buffered = BytesIO()
                image.save(buffered, format="JPEG")
                image_bytes = buffered.getvalue()
                image_data = 'data:image/jpeg;base64,' + str(b64encode(image_bytes), 'utf-8')

            except Exception as e:
                print(e, image_url)
                image_data = ''
                
            
            # get the comments and their scores
            comments = post.comments
            comments_sorted = sorted(comments, key=lambda comment: comment.score, reverse=True)[:num_comments]
            top_comments = [comment.body.replace('\n', ' ') for comment in comments_sorted]
            
            # write the data to the CSV file
            csv_writer.writerow([title, image_data] + top_comments)
        # close the CSV file
        csv_file.close()

def main():
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


if __name__ == '__main__':
    main()
