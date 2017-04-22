from django.db import models

# Create your models here.


from django.db import models

# a model describing a tweet from emergency responders idfk


class MyTweet(models.Model):
    created_at = models.CharField(max_length=200)  # TODO: datetime
    # the message id, separate from DB id
    twitter_msg_id = models.CharField(max_length=20, unique=True)  # TODO: unique, ignore?
    # twitter account username
    screen_name = models.CharField(max_length=200)
    text = models.TextField()
    # is the tweet in reply to some other tweet posted by themselves
    reply_to = models.CharField(max_length=20, blank=True, null=True, default=None)
    keywords = models.ForeignKey('Keyword', null=True, default=None)

    def __str__(self):
        return self.twitter_msg_id


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
    created_at = models.DateTimeField('created at')
    tweets = models.ForeignKey('MyTweet')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=REPORTED)
    danger = models.CharField(max_length=20, choices=THREAT_CHOICES, default=UNKNOWN)


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
