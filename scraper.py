from requests import get, codes
from bs4 import BeautifulSoup
# product_code = input("Please enter product code: ")
product_code = "36991221"
class Opinion:
        def __init__(self, author, recomendation, stars, content, pros, cons, upvotes, downvotes, published, purchased) -> None:
            self.author = author
            self.recomendations = recomendation
            self.stars = stars
            self.content = content
            self.pros = pros
            self.cons = cons
            self.upvotes = upvotes
            self.downvotes = downvotes
            self.published = published 
            self.purchased = purchased
        


# url = "https://www.ceneo.pl/" + product_code + "#tab=reviews"
# url = "https://www.ceneo.pl/{}#tab=reviews".format(product_code)
url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
response = get(url)
if response.status_code != codes['ok']:
    print('Not ok')
    exit(0)
page = BeautifulSoup(response.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib


try:    
    element = page.select_one('#form_body_opinion > div > div > div.review-header__score > div > div:nth-child(1) > div.score-extend__review')
    opinions = int(element.text.replace(' opinie', ''))
    print(opinions)
except:
    exit(0)
if opinions == 0:
    print('no opinions')
    exit(0)

op_all = []

opinions = page.select('#reviews > div > div.js_product-reviews.js_reviews-hook.js_product-reviews-container > div')
for op in  opinions:
    name = op.select_one('span.user-post__author-name').text
    try:
        recomendation = op.select_one('span.user-post__author-recomendation > em').text
    except:
         recomendation = None
    stars = op.select_one('span.user-post__score > span.user-post__score-count').text
    content = op.select_one('div.user-post__text').text
    pros = op.select('div.review-feature__title--positives ~ div.review-feature__item')
    pros = [p.text.strip() for p in pros ]
    cons = op.select('div.review-feature__title--negatives ~ div.review-feature__item')
    cons = [p.text.strip() for p in cons ]
    upvotes = op.select_one('button.vote-yes.js_product-review-vote.js_vote-yes[data-total-vote]').text
    downvotes = op.select_one('button.vote-no.js_product-review-vote.js_vote-no[data-total-vote]').text
    published = op.select_one('span.user-post__published > time:nth-child(1)')['datetime']
    try:
        purchased = op.select_one('span.user-post__published > time:nth-child(2)')['datetime']
    except:
         purchased = None    
    op_all.append({
        Opinion(name, recomendation, stars, content, pros, cons, upvotes, downvotes, published, purchased)
    })
input()