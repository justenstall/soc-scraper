import facebook_scraper
import json
import csv
from datetime import datetime
import os

# Path to facebook cookies
cookies_path = '/Users/justenstall/Downloads/facebook.com_cookies.txt'

# Name of group to scrape
group_name = 'babysleeptrainingtips'

# Keyword list: keywords are checked against all possible variations of the word 
keyword_list = ['sleep', 'sleep train', 'co-sleep']

# Minimum amount of comments
comment_minimum = 50

# Names that need may need censored from comment replies
redact_list = []

# scrape the specified group for posts
# output is a collection of CSV files, in a folder named by the group and the time requested, and organized into one subfolder per keyword
def scrape():
    # Get posts from facebook-scraper
    posts = facebook_scraper.get_posts(group=group_name, pages=10, sleep=5,cookies=cookies_path, options={"comments": True, "progress": True})

    # Create result directory for data to output to
    result_dir = '{group}_{time}'.format(group=group_name, time=datetime.now().strftime("%m-%d_%H-%M-%S"))
    os.makedirs(result_dir)
    print('Created results directory:', result_dir)

    # Filter for keyword matches
    for keyword in keyword_list:
        os.makedirs(os.path.join(result_dir, keyword))

    posts_json = []

    # Loop through posts to create list
    for post in posts:
        posts_json.append(post)

        keyword_match_list = []
        for keyword in keyword_list:
            if check_keyword(keyword, post['text']):
                keyword_match_list.append(keyword)

        # Filter by comment count
        if post['comments'] < comment_minimum:
            continue

        post_and_comments = []
        post_and_comments = parse_post(post)

        post_and_comments = redact_posts(post_and_comments)
 
        if len(post_and_comments) > 0:
            keys = post_and_comments[0].keys()

            for keyword in keyword_match_list:
                with open(os.path.join(result_dir, keyword, '{}.csv'.format(post['post_id'])), 'w', encoding='utf-8-sig', newline='') as output_file:
                    dict_writer = csv.DictWriter(output_file, keys)
                    dict_writer.writeheader()
                    dict_writer.writerows(post_and_comments)

    # Dump full content before parsing more
    with open(os.path.join(result_dir, "posts_full.json"), "w", encoding ='utf8') as output_file:
        json.dump(posts_json, output_file, ensure_ascii=False, indent=4)

# Return true if keyword is found
def check_keyword(keyword, text):
    return string_sanitize(keyword) in string_sanitize(text)

# Remove all non-alphanumeric characters and cast to lowercase
def string_sanitize(string):
    return ''.join(e for e in string if e.isalnum()).lower()

# Parse post and all of its comments
def parse_post(post):
    post_and_comments = []

    # Create post and add to list
    post_dict = create_post_dict(
        post['post_id'], 
        post['post_url'], 
        '', 
        post['text'], 
        post['time'],
    )
    post_and_comments.append(post_dict)

    print("Scraped post:", post_dict['url'])

    # Store poster name to censor
    redact_list.append(post['username'])

    for comment in post['comments_full']:
        comment_and_replies = parse_comment(post['post_id'], comment)
        post_and_comments.extend(comment_and_replies) # use extend because this is list concatenation
    
    return post_and_comments

def parse_comment(post_id, comment):
    comment_and_replies = []

    # Create comment and add to list
    comment_dict = create_post_dict(
        comment['comment_id'], 
        comment['comment_url'], 
        post_id, 
        comment['comment_text'], 
        comment['comment_time']
    )
    comment_and_replies.append(comment_dict)

    # Store commenter name to censor
    redact_list.append(comment['commenter_name'])

    for reply in comment['replies']:
        reply_dict = parse_reply(comment['comment_id'], reply)
        comment_and_replies.append(reply_dict)
    
    return comment_and_replies

def parse_reply(comment_id, reply):
    reply_dict = create_post_dict(
        reply['comment_id'], 
        reply['comment_url'], 
        comment_id, 
        reply['comment_text'], 
        reply['comment_time']
    )

    redact_list.append(reply['commenter_name'])

    return reply_dict

def create_post_dict(id, url, reply_to, text, time):
    return {
        'id': id,
        'url': url,
        'reply_to': reply_to,
        'text': text,
        'time': time.strftime("%m/%d/%Y, %H:%M:%S"),
    }

def redact_posts(posts):
    print(posts)
    for item in posts:
        for name in redact_list:
            item['text'].replace(name, '[NAME REDACTED]')
    return posts

if __name__ == "__main__":
    scrape()