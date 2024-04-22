from requests_html import HTMLSession
import json
import time

class Reviews:
    def __init__(self, url):
        self.session = HTMLSession()
        self.header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15'}
        self.url = url

    # This Method will give us every review from a Site
    def pagination(self, page):
        r = self.session.get(self.url + str(page))
        r.html.render(sleep=1)
        reviews = r.html.find('div[data-hook=review]')
        if not reviews:
            return [] # Return an empty list, if no reviews are found
        else:
            return reviews

    def parse(self, reviews):
        total = []
        for review in reviews:
            title = review.find('a[data-hook=review-title]', first=True).text
            rating = review.find('i[data-hook=review-star-rating] span', first=True).text
            body = review.find('span[data-hook=review-body] span', first=True).text.replace('\n', '').strip()

            data = {
                'title': title,
                'rating': rating,
                'body': body[:100]
            }
            total.append(data)
        return total

    def save(self, results):
        with open("FOODOKOFINEST-Reviews" + '-reviews.json', 'w') as f:
            json.dump(results, f)


if __name__ == '__main__':
    url = f"https://www.amazon.de/Foodoko-Finest-Balsamico-Geschenkset-Fläschchen/product-reviews/B09C5ZS1WM/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=1&sortBy=recent"
    amz = Reviews(url)
    results = []
    for x in range(1,5):
        print('getting page', x)
        time.sleep(0.3)
        reviews = amz.pagination(x)
        if reviews is not False:
            results.append(amz.parse(reviews))
        else:
            print("No more pages left!")
            break

    amz.save(results)


# TODO: Pagination does not work. Need to fix the "pageNumber" in Link.
