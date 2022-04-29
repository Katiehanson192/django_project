from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model): #profile create for each user and stores these attributes
    first_name = models.CharField(max_length=200,blank=True)
    last_name = models.CharField(max_length=200,blank=True)
    email = models.EmailField(max_length=300,blank=True)
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE) #1-to-1 field to the user entity. associates each profile w/ a user
    friends = models.ManyToManyField(User,blank=True, related_name='friends') #many-to-many field w/ user entity
    created = models.DateTimeField(auto_now=True) #date profile created
    updated = models.DateTimeField(auto_now_add=True)#date profile updated


    def __str__(self):
        return f"{self.user.username}" #returns user name from user
                                    #b/c user field points to user, can check actual name of user profile instead of just username

STATUS_CHOICES = (
    ('sent','sent'),
    ('accepted','accepted')
)

class Relationship(models.Model): #establish relationship b/t 2 profiles
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender') #FK to profile class
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')#FK to profile class
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="send") #default status = "send" once request is sent --> "accepted" once accepted
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    

class Post(models.Model): #posts made by the users
    description = models.CharField(max_length=255, blank=True) #
    username = models.ForeignKey(User, on_delete=models.CASCADE) #FK to user entity
    image = models.ImageField(upload_to='images',blank=True) #need to have "pillow" installed. All images will be stored in 'images' folder. 
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description #returns descrip of post

class Comment(models.Model): #comment associated w/ a post
    post = models.ForeignKey(Post, on_delete=models.CASCADE) #FK to post class
    username = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE) #FK to user model
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.text
    
    
class Like(models.Model): #keep track of how many likes to a post
	username = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE) #FK to user model
	post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE) #FK to post model


