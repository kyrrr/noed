from django.db import models

# Create your models here.


from django.db import models

# a model describing a tweet from emergency responders idfk


class MyTweet(models.Model):
    created_at = models.CharField(max_length=200)
    # the message id, separate from DB id
    twitter_msg_id = models.CharField(max_length=20, unique=True)  # TODO: unique, ignore?
    # twitter account username
    screen_name = models.CharField(max_length=200)
    text = models.TextField()
    # is the tweet in reply to some other tweet posted by themselves
    reply_to = models.CharField(max_length=20, blank=True, null=True)
    # found_keywords = models... TODO: what keywords affected this tweet? keywords in db?
    # string representation of what the current situation is e.g reported, pending, resolved, follow-up.
    # it's cheesy
    situation_status = models.CharField(max_length=200)

    def __str__(self):
        return self.twitter_msg_id
