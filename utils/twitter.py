from pytwitter import Api


class Twitter:
    def __init__(self, api_key: str):
        pass

    def post_tweet(self, message: str) -> None:
        pass
    
    def get_posted_tweets(self, username):
        pass

    def delete_tweet(self, tweet_id: str) -> None:
        pass


# Example usage:
api = Api(consumer_key="i3Eg1ZpIQPeHSZAYq1JmfGfhl", consumer_secret='ZFmTztAHNsexVhhxrhvknRHHmdxFtUElaCJFqAzk007I99Pjh3', oauth_flow=True)
print(api.get_authorize_url())