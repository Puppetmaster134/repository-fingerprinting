## create-repo-list
Uses PyGithub to scrape the top starred repos. Combines with a curated list of censorship circumvention tool repositories.

## scrape-repo-traffic
Contains the tool to record network traffic and scrape each repository. There's also a dockerfile to dockerize the whole process.

## clean-data
Swaps the order of the timing data and packet lengths because I fucked it up in the scraper and saved them in reverse order. Additionally, names the files in a consistent format expected by the wfes scripts.

## kfp-features-extract
Contains code I copied from Cherubin's wfes repo but I removed all of the other attacks because I couldn't be arsed to figure out the Weka stuff. Additionally, I modified some of the feature extraction code and updated it to work with Python 3.

## paper
Contains the course paper explaining the project.
