# Project Specifications

The University of Dayton Sociology Department is conducting qualitative research on public Facebook Pages. They need an automated way to gather post/comment data for text analysis in external analysis programs. This project's goal is to provide a user-friendly way to scrape public Facebook Pages for the post and comment data that is necessary and ethical for analysis.

## Features

### Keywords

Need to be able to provide a keyword list to filter posts by. This keywords list needs to be user-editable and intuitive.

### Comments

- Need to include comments with the posts.
- Posts should be able to be filtered by the amount of comments on them.

### Location

Look into what profile information is accessible to see if the tool could return a region location for each post/comment/user

## Scraping

The goal is to use an open-source Facebook scraper.

Open source scraper options:

- [facebook-scraper](https://github.com/kevinzg/facebook-scraper)
  - Most popular option on GitHub
  - Seems full featured
  - Provides a CLI
- [facebook-post-scraper](https://github.com/brutalsavage/facebook-post-scraper)
  - Contains limited comments support

## Concerns

- Need to be careful with the scraping quantity and speed to avoid getting IP addresses temporarily banned or any sort of consequences for the user's Facebook account.
  - Possibly implement timeouts, maximum posts per run
  - If we are limiting returned posts, maybe we can limit requests by only accessing posts of interest and sorting by relevance
- Need to consider privacy and ethics. Avoid preserving user information for the sake of privacy. Might need to come up with an anonymized user identification scheme so conversations can be tracked and active users do not sway location analysis
  - Map user email/id to a UUID with sha256 hash?

## Analysis Program

The analysis program being used is [QDA Miner](https://provalisresearch.com/products/qualitative-data-analysis-software/). The program needs to output files that are easily imported into QDA Miner and do as much work for the researchers as possible.
