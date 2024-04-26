from django.db import models
import numpy as np
from django.contrib.auth.models import User
class Wine(models.Model):
    name = models.CharField(max_length=200)

    def average_rating(self):
        all_ratings = list(map(lambda x: x.rating, self.review_set.all()))
        return np.mean(all_ratings)

    def __unicode__(self):
        return self.name
class Review(models.Model):
    RATING_CHOICES=(
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5'),
    )
    wine = models.ForeignKey(Wine,on_delete = models.DO_NOTHING)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)
class Cluster(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def get_members(self):
        return "\n".join([u.username for u in self.users.all()])


""" 
# Trong model Wine
def __str__(self):
    return self.name

def average_rating(self):
    all_ratings = [review.rating for review in self.review_set.all()]
    if all_ratings:
        return sum(all_ratings) / len(all_ratings)
    return 0

# Trong model Review
def is_valid_rating(self):
    return self.rating in range(1, 6)

def __str__(self):
    return f"{self.wine.name} - {self.rating}"

# Trong model Cluster
def get_member_count(self):
    return self.users.count()

def __str__(self):
    return self.name
"""