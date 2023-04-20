from requests import get, codes
from bs4 import BeautifulSoup
import json
# product_code = input("Please enter product code: ")
product_code = "36991221"
class Opinion:
        def __init__(self,id, author, recomendation, stars, content, pros, cons, upvotes, downvotes, published, purchased) -> None:
            self.id = id
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
selectors = {
        "id":[None, "data-entry-id"],
        "name":['span.user-post__author-name'],
        "recomendation": ['span.user-post__author-recommendation > em'],
        "stars": ['span.user-post__score > span.user-post__score-count'],
        "content":['div.user-post__text'],
        "pros":['div.review-feature__title--positives ~ div.review-feature__item', None, True],
        "cons":['div.review-feature__title--negatives ~ div.review-feature__item', None, True],
        "upvote":['button.vote-yes.js_product-review-vote.js_vote-yes', 'data-total-vote'],
        "downvote":['button.vote-no.js_product-review-vote.js_vote-no','data-total-vote'],
        "published":['span.user-post__published > time:nth-child(1)','datetime'],
        "purchased":["span.user-post__published > time:nth-child(2)", 'datetime']
    }
def get_element(opinion, selector = None, attr = None, is_list = False):
    try:
        if is_list:
            return [tag.text.strip() for tag in opinion.select(selector) ]
        if not selector and attr:
            return opinion[attr]
        if attr:
            return opinion.select_one(selector)[attr].strip()
        return opinion.select_one(selector).text.strip()
    except (AttributeError, TypeError):
        return None

url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
op_all = []
while url:
    response = get(url)
    if response.status_code != codes['ok']:
        print('Not ok')
        exit(0)
    page = BeautifulSoup(response.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib

    try:    
        element = page.select_one('#form_body_opinion > div > div > div.review-header__score > div > div:nth-child(1) > div.score-extend__review')
        opinions = int(element.text.replace(' opinie', ''))
    except:
        exit(0)
    if opinions == 0:
        print('no opinions')
        exit(0)

    opinions = page.select('#reviews > div > div.js_product-reviews.js_reviews-hook.js_product-reviews-container > div')
    for op in  opinions:
        single_opinions = {}
        for k,v in selectors.items():
            single_opinions[k] = get_element(op, *v)
        op_all.append(single_opinions)
    try:    
        url = "https://www.ceneo.pl/" + get_element(page, 'a.pagination__item.pagination__next', "href")
    except:
        url = None
with open('./opinions/opinions.json', "w", encoding='UTF-8') as file:
    json.dump(op_all, file ,indent=4, ensure_ascii=False)
print('success')