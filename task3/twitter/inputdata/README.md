# Data

## Description

We release tweet ids from May 25 and June 30, 2020. The folders `05-2020` and `06-2020` contain tweets from May and June, respectively. Each month's tweets are split into 10 equally sized csv files. Each csv contains the following fields:

* *tweet-id*: the unique numeric identifier for each tweet
* *blacklivesmatter*: binary variable, 1 if the tweet contains a Black Lives Matter keyword, 0 otherwise
* *alllivesmatter*: binary variable, 1 if the tweet contains an All Lives Matter keyword, 0 otherwise
* *bluelivesmatter*:binary variable, 1 if the tweet contains a Blue Lives Matter keyword, 0 otherwise

## Downloading Tweet Content

Due to Twitter's Terms of Service we are only able to distribute the numeric tweet id. Here we give brief instructions on how to populate the full tweet data from the list of ids. To do this we will use the Python command line tool [Twarc](https://github.com/DocNow/twarc). The following steps assume you have Twarc installed as well as a [Twitter Developer account](https://developer.twitter.com/en/apply-for-access). To install Twarc, please run

```
pip3 install twarc
```

Next, you must configure Twarc with your [Twitter API tokens](https://developer.twitter.com/en/apply-for-access). 

```
twarc configure
```

Next, download the data from GitHub (we will use the first file from May as an example):

```
git clone https://github.com/sjgiorgi/case_shared_task_private.git
cd case_shared_task_private/twitter
gunzip 05-2020.01.csv.gz
```

This file contains the following fields: *tweet-id*, *blacklivesmatter*, *alllivesmatter*, *bluelivesmatter*. Next, we create a file containing only tweet ids:

```
cut -d, -f1 05-2020.01.csv > 05-2020.01.ids.txt
``` 

### Using twarc from the command line

This command will produce a file where each line is a separate json file for each tweet ids. Note that only tweets which are publicly available at the time of your pull will be downloaded. Thus, our numbers might not match the numbers you see. 

```
twarc hydrate 05-2020.01.ids.txt > 05-2020.01.jsonl
```

### Using hydrate Python script

To run this script you must install the Python package tqdm:

```
pip3 install tqdm
```

The script **hydrate.py** assumes you've created the above text files (**.txt**) in the folders `05-2020` and `06-2020`. Then run

```
python3 hydrate.py
```

This will produce the file **blm_tweet_ids.jsonl**.



### Other options 

Besides twarc, there are many other tools available for downloading Twitter data, such as [TwitterMySQL](https://github.com/dlatk/TwitterMySQL) and [hydrator](https://github.com/DocNow/hydrator).
