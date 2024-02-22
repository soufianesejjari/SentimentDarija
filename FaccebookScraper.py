import facebook_scraper as fs
import pandas as pd

class FacebookScraper:
    def __init__(self):
        self.MAX_COMMENTS = 100

    def getPostData(self, post_url):
        post_id = post_url.split("/")[-2]
        # Assurez-vous que l'ID ne contient pas d'autres caractères
        post_id=post_id.split("?")[0]
        gen = fs.get_posts(post_urls=[post_id], options={"comments": self.MAX_COMMENTS, "progress": True})
        post = next(gen)
        comments = post['comments_full']
        df = pd.json_normalize(comments, sep='_')
        return df

