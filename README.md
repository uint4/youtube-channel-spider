# Youtube Channel Spider
A tool that uses the GCP Youtube Data API to scrape relevant data from a channel to a csv

## Setup Instructions
`python3 -m pip install -r requirements.txt`  
Be sure to set the Youtube Data API key in config.py

## Examples:
Download data for the youtube channel PTXofficial  
`python3 bin/scraper.py PTXofficial`  
The results will be under the results folder.  

## References:
https://medium.com/analytics-vidhya/how-to-extract-youtube-video-titles-using-the-youtube-data-api-45d3f4998486  
https://developers.google.com/youtube/v3/docs
