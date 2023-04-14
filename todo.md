# Insult Generator
## By Liam Salass

## 1 - Data scraping

Data scrape: using reddit api
- r/roastme
- Look into more r/ with img to roast 
- make script for pulling image and responses from top voters and placing into csv file

## 2 - Data storage and training location

- find a resource to store all images 
- - (maybe reduce img size when downloading if doing on computer)
- attempt with small dataset to begin
- store datasets in hdf5

## 3 - Data classification

- look for common words between posts and filter out non-insult words (the, and, etc)
- perform clustering on data
- apply PCA output tags for each image of a person
- apply the PCA output tags to 

## 4 - Plit training into CNN part and NLP part

- create CNN that will predict PCA labels
- create NLP that will use the PCA labels to predict roasts

## 5 - Fine tune

- create GUI where I go through each image 
- GUI allows user to see comments and image
- buttons and color picker and race picker to determine more fine tuned labels