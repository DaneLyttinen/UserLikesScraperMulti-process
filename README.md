# UserLikesScraperMulti-process
I wanted to scrape the data from profiles on the website allrecipes.com to see if there could be any insight gained from what users like with association rule mining.
To gather this data I chose to use Selenium only due to the fact that the data I needed to gather would not load through pure scrapy as it is dynamically loaded content through Angular Javascript. I tried a solution with scrapy and splash but the content I required (just the titles of what they had liked) would not load there either. 

So as I have had prior knowledge with Selenium I chose to use it for this project but it is a terribly slow framework, especially for scraping loads of data. So to mitigate this, I added multiprocessing to speed up the data scraping which sped up the process by far.
