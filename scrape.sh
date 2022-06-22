# Scrape the babysleeptrainingtips group for posts with more than 50 comments and containing the keyword
facebook-scraper --cookies ~/facebook.com_cookies.txt --sleep --group babysleeptrainingtips 
facebook-scraper --cookies from_browser --sleep 90000 -fmt csv --matching ^[.\n]sleep[.\n] --pages 1 --comments --group babysleeptrainingtips
facebook-scraper --cookies ~/Downloads/facebook.com_cookies.txt --sleep 1 -fmt csv --verbose --matching ^[.\n]sleep[.\n] --pages 3 --comments --group babysleeptrainingtips
facebook-scraper --cookies ~/Downloads/facebook.com_cookies.txt --sleep 1 -fmt csv --verbose --pages 3 --comments --group babysleeptrainingtips
facebook-scraper --cookies ~/Downloads/facebook.com_cookies.txt --sleep 1 --matching [.\n]*sleep[.\n]* --verbose --pages 3 --comments --group babysleeptrainingtips

regex: ^[.\n]sleep[.\n]