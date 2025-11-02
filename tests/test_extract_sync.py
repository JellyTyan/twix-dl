from twix_dl import TwitterClient

def main():
    print("Getting post info")
    client = TwitterClient()
    response = client.get_tweet_info(1984589347073769877)
    print(response)
    print("Getting user info")
    response = client.get_user_by_username("chetom_")
    print(response)

if __name__ == "__main__":
    main()
