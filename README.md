# MSM V17
### Kyrre Bugge & Tobias Bergman

Twep is a Python package containing

 - A minimal implentation of the Tweepy Python Api, which lets you interact with Twitter data
 - A collection of classes and commands, aiming to gather, categorize, analyze and present tweets posted by any single Twitter account, linking a user's tweets and self-replies eachother. 
 - The keywords that are searched for in this applications as-is (twep/keywords.py) are aimed at picking up Tweets by Norwegian emergency services, as well as locations (in Oslo as-is) mentioned by these. 
 
Once the project is installed, try scanning some of these accounts:
*oslopolitiops*, *politiostfldops*, *romerikepoliti*, etc..
 

### Installation

Twep is a Django 1.1 project and was developed using Python 3.6.

To run the project, first clone it into a directory of your choosing:
```sh
$ git clone https://github.com/kyrrr/noed.git
```

Set up a twitter app (you will need a twitter account)

In settings.py, enter the keys, tokens and secrets for your twitter app:
```
API_KEYS = [
    {
        'TWITTER': {
            'CONSUMER_KEY': 'your consumer key',
            'CONSUMER_SECRET': 'your consumer secret',
            'ACCESS_TOKEN': 'your access token',
            'ACCESS_SECRET': 'your access secret'
        }
    }
]
```
Database setup:

```sh
$ python manage.py makemigrations
$ python manage.py migrate
```

# Doing things
Before getting any tweets, use the following command and follow the prompts to read keywords.py into the database.
```
$ python manage.py fillkw
```

Getting, scanning, and presenting tweets:
```sh
$ python manage.py get my_twitter_screen_name
$ python manage.py scan my_twitter_screen_name
```

Store the output of any of these by using:
```sh
$ python manage.py scan my_twitter_screen_name > overwritten_file.txt
```
or:
```sh
$ python manage.py get my_twitter_screen_name >> appended_file.txt
```
to append to (or create) the file.


# Web
 
To start the server, do:
```sh
$ python manage.py runserver
```
 
Then navigate to:
```url
localhost:8000/twep?screen_name=my_twitter_screen_name
``` 
To see tweets by a Twitter user presented in markdown

# Util
## Text
#### MarkDown
## Tweets
#### TweetSeeker
 ```python
print()
 ```
#### TweetTransformer
- Identifies relationships between Tweets
- Creates database objects for MyTweet and Situation objects to hold these
# Commands
### get
- T
### scan


# Models
#### MyTweet
This object is populated by the Tweepy Api and manipulated
to populate other objects.
#### Situation
This object contains tweets
#### Keyword
#### Location
- ##### City
- ##### District
- ##### Sub-district
#### Keyword Category
#### Keyword

## Entity Relationship



[kyrrr]: <https://github.com/kyrrr/>
[caterpiethug]: <https://github.com/caterpiethug/>
[git-repo-url]: <https://github.com/kyrrr/twep.git>
[tweepy]: <http://www.tweepy.org/>
