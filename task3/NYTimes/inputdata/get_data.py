import json
import requests
import sys

api_key = sys.argv[1] # You can get your key from https://developer.nytimes.com/get-started

def download_metadata_from_api(month):
    url = "http://api.nytimes.com/svc/archive/v1/2020/{}.json?api-key={}".format(month, api_key)
    r = requests.get(url)
    return r

def process_api_response(response):
    response = response.json()
    docs = response["response"]["docs"]

    data = []
    for doc in docs:
        d = {}
        d["pub_date"] = doc["pub_date"][:10]
        d["abstract"] = doc["abstract"]
        d["snippet"] = doc["snippet"]
        d["lead_paragraph"] = doc["lead_paragraph"]
        d["url"] = doc["web_url"]
        data.append(d)

    return data

if __name__ == "__main__":
    # Download 2020/06 news metadata from nyt api
    response = download_metadata_from_api("6")
    if response.status_code != 200:
        raise("Could not download metadata from NYTimes api for some reason!")

    june_data = process_api_response(response)

    # Download 2020/05 news metadata from nyt api
    response = download_metadata_from_api("5")
    if response.status_code != 200:
        raise("Could not download metadata from NYTimes api for some reason!")

    may_data = process_api_response(response)
    # Since our gold data is between 2020/05/25 and 2020/06/30, we discard most of this data
    may_data = [d for d in may_data if int(d["pub_date"][-2:]) >= 25]

    # Combine two months
    all_data = may_data + june_data

    # Write to file
    with open("out.json", "w", encoding="utf-8") as f:
        f.write("\n".join([json.dumps(d) for d in all_data]))
