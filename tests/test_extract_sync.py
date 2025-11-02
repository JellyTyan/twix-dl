from twix_dl import TwitterClient

def main():
    client = TwitterClient()
    response = client.get_tweet(1984589347073769877)
    print(response)

if __name__ == "__main__":
    main()
