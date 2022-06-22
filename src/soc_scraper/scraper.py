import facebook_scraper
import json
import csv
from datetime import datetime
import os

# Keyword list
keyword_list = ['sleep', 'sleep_training']

# Minimum amount of comments
comment_minimum = 50

# Names that need may need censored from comment replies
censor_names = []

def scrape():
    now = datetime.now()
    posts_dir = '{keywords}_{time}'.format(keywords='-'.join(keyword_list), time=now.strftime("%m-%d_%H-%M-%S"))

    os.makedirs(posts_dir)

    print('Created results directory:', posts_dir)

    # Get posts from facebook-scraper
    posts = facebook_scraper.get_posts(group='babysleeptrainingtips', pages=3, cookies="/Users/justenstall/Downloads/facebook.com_cookies.txt", options={"comments": True})

    # Loop through posts to create list
    for post in posts:
        # Filter by comment count
        if post['comments'] < comment_minimum:
            continue

        # Filter for keyword matches
        keyword_match = False
        for keyword in keyword_list:
            if keyword.lower() in post['text'].lower():
                keyword_match = True

        if not keyword_match:
            continue

        post_and_comments = parse_post(post)

        for item in post_and_comments:
            for name in censor_names:
                item['text'].replace(name, '[NAME REDACTED]')

        # TODO: write to JSON file named post ID

        keys = post_and_comments[0].keys()

        with open(os.path.join(posts_dir, '{}.csv'.format(post['post_id'])), 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(post_and_comments)

    # TODO: change output shape to two dimensional array (flatten comments and replies into single list)
    # TODO: remove names from comment text

    # with open('result.json', 'w') as fp:
    #     json.dump(formatted_posts, fp)
            

# text stores the post's text
# comments_full stores a list of comment dicts for each post
# comment_text stores the comment's text
# replies stores a list of comments responding to that comment
# commenter_id stores a number that refers to the user
# comment_time is the time the comment was made

# Considerations: remove commenter name from replies to their comment

def parse_post(post):
    post_and_comments = []

    # Create post and add to list
    post_dict = {
        'id': post['post_id'],
        'url': post['post_url'],
        'text': post['text'],
        'time': post['time'].strftime("%m/%d/%Y, %H:%M:%S"),
        'reply_to': '',
    }
    post_and_comments.append(post_dict)

    print("Scraped post:", post_dict['url'])

    # Store poster name to censor
    censor_names.append(post['username'])

    for comment in post['comments_full']:
        comment_and_replies = parse_comment(post['post_id'], comment)
        post_and_comments.extend(comment_and_replies)
    
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
    censor_names.append(comment['commenter_name'])

    for reply in comment['replies']:
        reply_dict = parse_reply(comment['comment_id'], reply)
        comment_and_replies.extend(iterable)(reply_dict)
    
    return comment_and_replies

def parse_reply(comment_id, reply):
    reply_dict = create_post_dict(
        reply['comment_id'], 
        reply['comment_url'], 
        comment_id, 
        reply['comment_text'], 
        reply['comment_time']
    )

    censor_names.append(reply['commenter_name'])

    return reply_dict

def create_post_dict(id, url, reply_to, text, time):
    return {
        'id': id,
        'url': url,
        'reply_to': reply_to,
        'text': text,
        'time': time.strftime("%m/%d/%Y, %H:%M:%S"),
    }

if __name__ == "__main__":
    scrape()