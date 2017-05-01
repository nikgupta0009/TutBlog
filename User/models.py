from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from image_cropping import ImageRatioField
import os
# Create your models here.
def get_image_path(instance, filename):
    return os.path.join('user', str(instance.id), filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    cropping = ImageRatioField('profile_image', '700x700', size_warning=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)
    contribution = models.IntegerField(default=0)
    organization = models.CharField(max_length=200, null=True, blank=True)
    facebook_url = models.URLField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    googleplus = models.URLField(max_length=200, null=True, blank=True)
    mobile = models.BigIntegerField(null = True, blank = True)
    relationships = models.ManyToManyField('self', through='Relationship', symmetrical=False, 
    	related_name='related_to')
    following_cnt=models.IntegerField(default=0)
    follower_cnt=models.IntegerField(default=0)
    def image_url(self):
        """
        Returns the URL of the image associated with this Object.
        If an image hasn't been uploaded yet, it returns a stock image
        :returns: str -- the image url
        """
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
        else:
            return '../static/material-dashboard/img/faces/marc.jpg'

    def __str__(self):              # __unicode__ on Python 2
        return "%s" % (self.user.username)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
)

class Relationship(models.Model):
	from_person = models.ForeignKey(Profile, related_name='from_people')
	to_person = models.ForeignKey(Profile, related_name='to_people')
	status = models.IntegerField(choices=RELATIONSHIP_STATUSES)

def add_relationship(self, person, status):
	relationship, created = Relationship.objects.get_or_create(
		from_person=self,
		to_person=person,
		status=status)
	return relationship

def remove_relationship(self, person, status):
	Relationship.objects.filter(
		from_person=self,
        to_person=person,
        status=status).delete()
	return

def get_relationships(self, status):
    return self.relationships.filter(
        to_people__status=status,
        to_people__from_person=self)

def get_related_to(self, status):
	return self.related_to.filter(
        from_people__status=status,
        from_people__to_person=self)

def get_following(self):
	return get_relationships(self, RELATIONSHIP_FOLLOWING)

def get_followers(self):
	return get_related_to(self, RELATIONSHIP_FOLLOWING)

def is_following(self, person):
    return Relationship.objects.filter(
        from_person=self,
        to_person=person,
        status=RELATIONSHIP_FOLLOWING).exists()