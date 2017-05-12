from django.db import models
from picklefield.fields import PickledObjectField
# a model describing a tweet from emergency responders idfk


class Tweet(models.Model):
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

    # holds categories as key, keywords as values
    categories_keywords = PickledObjectField(null=True)

    location = models.ForeignKey('Location', null=True, default=None)

    text_summary_title = models.CharField(max_length=40, null=True, default=None)
    text_summary = models.TextField(null=True, default=None)

    # situation = models.ForeignKey('Situation', null=True, default=None)

    def __str__(self):
        # prints the msg id when the object itself is print()-ed, etc
        return self.twitter_msg_id

    # TODO: limit?
    def get_all_children(self, include_self=True):
        r = []
        if include_self:
            r.append(self)
        for c in Tweet.objects.filter(parent=self):
            _r = c.get_all_children(include_self=True)
            if 0 < len(_r):
                r.extend(_r)
        return r

    def get_last_child(self):
        r = [self]
        for c in Tweet.objects.filter(parent=self):
            _r = c.get_all_children()
            if 0 < len(_r):
                r.extend(_r)
        return r[len(r) - 1]

    def get_oldest_parent(self):
        try:
            # find tweet where this is the child
            t = Tweet.objects.get(child=self)
            # if it has a parent
            if t.parent:
                # find the next parent ??
                Tweet.get_oldest_parent(t.parent)
            else:
                # if it does not have a parent
                # it must be the last one ??
                # as a tweet can only have one parent and one child
                return t
        except Tweet.DoesNotExist:
            # print("tweet is not a child??")
            pass

    def is_first_in_series(self):
        return self.is_alone() or self.is_orphan_with_child()

    def is_alone(self):
        return self.parent is None

    def is_orphan_with_child(self):
        return self.parent is None and self.child is not None

    def is_orphan_with_no_child(self):
        return self.parent is None and self.child is not None

    def has_parent_and_child(self):
        return self.parent is not None and self.child is not None

    def is_last_child(self):
        return self.child is None and self.parent is not None


class City(models.Model):
    name = models.CharField(max_length=200)


class District(models.Model):
    city = models.ForeignKey('City', null=False)
    name = models.CharField(max_length=200)


class SubDistrict(models.Model):
    district = models.ForeignKey('District', null=False)
    name = models.CharField(max_length=200)


class Location(models.Model):
    city = models.ForeignKey('City', null=False)
    district = models.ForeignKey('District', null=True, default=None)
    sub_district = models.ForeignKey('SubDistrict', null=True, default=None)


class Timeline(models.Model):
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
    screen_name = models.CharField(max_length=200, null=True, default=None)
    first_tweet = models.ForeignKey('Tweet', related_name="prophet", null=True, default=None)
    children = models.ManyToManyField('Tweet', related_name="apostles", default=None)
    description = models.CharField(max_length=140, null=True, default=None)

    def __str__(self):
        return str(self.id)


class KeywordCategory(models.Model):
    name = models.CharField(max_length=200)
    tweets = models.ManyToManyField('Tweet', default=None)

    def __str__(self):
        return self.name


class User(models.Model):
    screen_name = models.CharField(max_length=200, unique=True)
    blob_data = models.TextField(db_column='data', null=True, default=None)


class Keyword(models.Model):
    word = models.CharField(max_length=200)
    category = models.ForeignKey('KeywordCategory', null=True, default=None)
    tweets = models.ManyToManyField('Tweet', default=None)
    situation = models.ForeignKey('Timeline', null=True, default=None)

    def __str__(self):
        return self.word
