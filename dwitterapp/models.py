# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Dweeter(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user',blank=True,null=True)
    follows = models.ManyToManyField('self', blank=True,symmetrical=False)

    def __str__(self):
        return self.user.username


class Dweets(models.Model):

    dweeter = models.ForeignKey(Dweeter, on_delete=models.CASCADE)
    dweet = models.TextField(null=True,blank=True)
    likes = models.ManyToManyField(Dweeter, blank=True, related_name='likes')

    def __str__(self):
        return self.dweet



class DweetComments(models.Model):
    dweet = models.ForeignKey(Dweets,on_delete=models.CASCADE)
    dweeter = models.ForeignKey(Dweeter,on_delete=models.CASCADE)
    comment = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.dweeter.username

