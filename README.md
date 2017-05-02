# MSM V17

Twep is a thing that has

  - Classes
  - Commands
  - Models
  - ... and so much more!


### Installation

Twep is a Django 1.1 project and was developed using Python 3.6
Do some magic

Set up twitter app

Get keys from twitter

In settings.py, enter your keys and secrets

Database setup:

```sh
$ python manage.py makemigrations
$ python manage.py migrate
```

# Doing things
Before getting any tweets, use this command and follow the prompts to read keywords.py into the database.
```
$ python manage.py fillkw
```

Getting, scanning, and presenting tweets:
```sh
$ python manage.py get my_twitter_screen_name
$ python manage.py scan my_twitter_screen_name
$ python manage.py present my_twitter_screen_name
```

You can store the output of these by using
```sh
$ python manage.py present my_twitter_screen_name > file.txt
```

# Classes

# Models
### MyTweet
### Situation
### Keyword
### Location
#### City
#### District
#### Sub-district
### Keyword Category
### Keyword

## Entity Relationship



[kyrrr]: <https://github.com/kyrrr/>
[caterpiethug]: <https://github.com/caterpiethug/>
[git-repo-url]: <https://github.com/kyrrr/twep.git>

