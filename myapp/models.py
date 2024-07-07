from django.db import models

# Create your models here.


class login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    usertype = models.CharField(max_length=100)

class user(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    pin = models.CharField(max_length=100)
    LOGIN = models.ForeignKey(login,on_delete=models.CASCADE,default=1)



class home(models.Model):
    house_name = models.CharField(max_length=100)
    house_no = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    square_feet = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    no_of_rooms = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    booking_status = models.CharField(max_length=100)
    USER = models.ForeignKey(user, on_delete=models.CASCADE, default=1)


class complaint(models.Model):
    complaint = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    reply = models.CharField(max_length=100)
    reply_date = models.CharField(max_length=100)
    USER = models.ForeignKey(user, on_delete=models.CASCADE, default=1)

class requests(models.Model):
    date = models.CharField(max_length=100)
    pay_date = models.CharField(max_length=100)
    pay_status = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    USER = models.ForeignKey(user, on_delete=models.CASCADE, default=1)
    HOME = models.ForeignKey(home, on_delete=models.CASCADE, default=1)

class document(models.Model):
    documents = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    REQUESTS = models.ForeignKey(requests, on_delete=models.CASCADE, default=1)