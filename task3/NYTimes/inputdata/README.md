To receive the data run the below code, changing "your_api_key" with your NYTimes api key. You can get a key from https://developer.nytimes.com/get-started

`python get_data.py your_api_key`

After you run this, a file named "out.json" will be created. Each line of this file will be JSON object containing information about an article. The keys are as follows:
* pub_date -> Publication date of the article
* abstract -> Abstract of the article
* snippet -> A snippet from the article text
* lead_paragraph -> The lead paragraph from the article
* url -> The URL of the article
