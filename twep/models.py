from django.db import models
import datetime
from django.utils import timezone


# a model describing a tweet from emergency responders idfk

class MyTweet(models.Model):
    # twitter msg id, used as primary key
    twitter_msg_id = models.CharField(max_length=20, unique=True, primary_key=True)
    # string timestamp
    created_at = models.CharField(max_length=200)  # TODO: datetime
    # twitter screen name (after / in the user page url)
    screen_name = models.CharField(max_length=200)
    text = models.TextField()
    # is the tweet in reply to some other tweet posted by themselves
    # TODO: Actual foreign key to other MyTweet object
    reply_to_id_str = models.CharField(max_length=20, null=True, default=None)
    parent = models.ForeignKey('self', null=True, default=None, related_name='+')
    child = models.ForeignKey('self', null=True, default=None)
    keywords = models.ForeignKey('Keyword', null=True, default=None)
    situation = models.ForeignKey('Situation', null=True, default=None)
    scanned = models.BooleanField(default=False)

    def __str__(self):
        # prints the msg id when the object itself is print()-ed, etc
        return self.twitter_msg_id

    # magic recursion
    def get_all_children(self, include_self=True):
        r = []
        if include_self:
            r.append(self)
        for c in MyTweet.objects.filter(parent=self):
            _r = c.get_all_children(include_self=True)
            if 0 < len(_r):
                r.extend(_r)
        return r


class Situation(models.Model):
    REPORTED = 'RP'
    IN_PROGRESS = 'IP'
    RESOLVED = 'RS'
    UNKNOWN = 'U'
    STATUS_CHOICES = (
        (REPORTED, 'Reported'),
        (IN_PROGRESS, 'In Progress'),
        (RESOLVED, 'Resolved'),
        (UNKNOWN, 'Unknown')
    )
    NO_DANGER = 'ND'
    CAUTION = 'C'
    DANGER = 'D'
    THREAT_CHOICES = (
        (NO_DANGER, 'No Danger'),
        (CAUTION, 'Caution'),
        (DANGER, 'Danger'),
        (UNKNOWN, 'Unknown')
    )
    # TODO: Figure out timezone fuckery!!
    created_at = models.DateTimeField('created at', default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=REPORTED)
    danger_level = models.CharField(max_length=20, choices=THREAT_CHOICES, default=UNKNOWN)

    def __str__(self):
        return str(self.id)


class Keyword(models.Model):
    VIOLATION = 'V'
    DANGER = 'D'
    LOCATION = 'L'
    STATUS = 'S'
    HAPPY = 'H'
    UNKNOWN = 'U'
    CATEGORY_CHOICES = (
        (VIOLATION, 'Violation'),
        (DANGER, 'Danger'),
        (LOCATION, 'Location'),
        (STATUS, 'Status'),
        (HAPPY, 'Happy'),
        (UNKNOWN, 'Unknown')
    )
    word = models.CharField(max_length=200)
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES, default=UNKNOWN)
