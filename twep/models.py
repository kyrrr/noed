from django.db import models


# a model describing a tweet from emergency responders idfk

class MyTweet(models.Model):
    # twitter msg id, used as primary key
    twitter_msg_id = models.CharField(max_length=20, unique=True, primary_key=True)
    # string timestamp
    created_at = models.DateTimeField(null=True, default=None)
    # twitter screen name (after / in the user page url)
    screen_name = models.CharField(max_length=200)
    text = models.TextField()
    # used to check if the tweet in reply to some other tweet posted by themselves
    reply_to_id_str = models.CharField(max_length=20, null=True, default=None)
    parent = models.ForeignKey('self', null=True, default=None, related_name='+')
    child = models.ForeignKey('self', null=True, default=None)
    keyword = models.ManyToManyField('Keyword', default=None)

    def __str__(self):
        # prints the msg id when the object itself is print()-ed, etc
        return self.twitter_msg_id

    # magic recursion
    # TODO: limit?
    def get_all_children(self, include_self=True):
        r = []
        if include_self:
            r.append(self)
        for c in MyTweet.objects.filter(parent=self):
            _r = c.get_all_children(include_self=True)
            if 0 < len(_r):
                r.extend(_r)
        return r

    def is_last_child(self):
        return self.child is None and self.parent is not None


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
    # TODO: is this timezone ok?
    base_tweet = models.ForeignKey('MyTweet', verbose_name='base_mytweet_id', null=True, default=None)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=UNKNOWN)
    danger_level = models.CharField(max_length=20, choices=THREAT_CHOICES, default=UNKNOWN)

    def __str__(self):
        return str(self.id)


class Keyword(models.Model):
    ACTOR = 'A'
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
        (ACTOR, 'Actor'),
        (UNKNOWN, 'Unknown')
    )
    word = models.CharField(max_length=200)
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES, default=UNKNOWN)

    def __str__(self):
        return str(self.id)
