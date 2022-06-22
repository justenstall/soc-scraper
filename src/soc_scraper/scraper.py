import facebook_scraper
import json

# Keyword lists
keyword_list = ['sleep']

comment_minimum = 50


# Global lists for output
# posts_json_list = []
posts_flat_list = []

censor_names = []

def scrape():
    now = datetime.now()
    results_folder = 'results-{}'.format()

    posts = facebook_scraper.get_posts(group='babysleeptrainingtips', pages=3, cookies="/Users/justenstall/Downloads/facebook.com_cookies.txt", options={"comments": True})
    for post in posts:

        # TODO: filtering based on post['comments'] count and keyword presence in post['text']

        if post['comments'] < comment_minimum:
            continue

        keyword_match = false
        for keyword in keyword_list:
            if keyword in post['text']:
                keyword_match = True

        if not keyword_match:
            continue

        # Create post and add to list
        post_dict = {
            'id': post['post_id'],
            'url': post['post_url'],
            'text': post['text'],
            'time': post['time'].strftime("%m/%d/%Y, %H:%M:%S"),
        } 
        posts_flat_list.append(post_dict)

        # Store poster name to censor
        censor_names.append(post['username'])

        for comment in post['comments_full']:

            # Create comment and add to list
            comment_dict = {
                'id': comment['comment_id'],
                'url': comment['comment_url'],
                'text': comment['comment_text'],
                'time': comment['comment_time'].strftime("%m/%d/%Y, %H:%M:%S"),
            }
            posts_flat_list.append(comment_dict)

            # Store commenter name to censor
            censor_names.append(comment['commenter_name'])

        for item in posts_flat_list:
            for name in censor_names:
                item['text'].replace(name, '[NAME REDACTED]')

        
        # TODO: write to JSON file named post ID
        

        with open(os.path.join('results-{}'.format, '{}.json'.format(post['post_id'])), 'w') as fp:
            json.dump(posts_flat_list, fp)

    # TODO: change output shape to two dimensional array (flatten comments and replies into single list)
    # TODO: remove names from comment text

    with open('result.json', 'w') as fp:
        json.dump(formatted_posts, fp)
            

# text stores the post's text
# comments_full stores a list of comment dicts for each post
# comment_text stores the comment's text
# replies stores a list of comments responding to that comment
# commenter_id stores a number that refers to the user
# comment_time is the time the comment was made

# Considerations: remove commenter name from replies to their comment

# recursively get all replies to a comment
def get_replies(comment):
    replies = []
    if 'replies' in comment:
        for reply in comment['replies']:
            comment_dict = {
                'url': reply['comment_url'],
                'text': reply['comment_text'],
                'time': reply['comment_time'].strftime("%m/%d/%Y, %H:%M:%S"),
                'replied_to': reply['comment_url'],
                'replies': get_replies(reply)
            }

            censor_names.append(reply['commenter_name'])
            replies.append(comment_dict)
    return replies

if __name__ == "__main__":
    scrape()


def format_output(post_list):
    output_posts = []
    for post in post_list:
        post_dict = 