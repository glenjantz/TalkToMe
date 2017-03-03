from __future__ import unicode_literals
import re
from django.db import models
import bcrypt
from datetime import datetime
import datetime
from django.db.models import Count


class RoomManager(models.Manager):

    def makeroom(self, postData, user):
        if len(postData['location']) < 1:
            return {'error': 'Nothing written!'}
        else:
            check = Room.objects.annotate(count = (Count('users'))).filter(count = 1).filter(users__location=postData['location'], name = user.location)
            if len(check) > 0:
                this_room = check[0]
                User.objects.filter(id=user.id).update(room=this_room)
                return {'room': this_room }
            else:
                new_room = Room.objects.create(name=postData['location'])
                User.objects.filter(id=user.id).update(room=new_room)
                Room.objects.filter(id=new_room.id).update(roomname=user.location + " and " + new_room.name)
                return {'room': new_room }

class Room(models.Model):
      roomname = models.CharField(max_length=100, blank=True, null=True)
      name = models.CharField(max_length=100)
      created_at = models.DateTimeField(auto_now_add = True, blank=True, null=True)
      updated_at = models.DateTimeField(auto_now = True)
      objects = RoomManager()


class UserManager(models.Manager):

    def register(self, postData):
        status = True
        errorlist = []
        if postData['password'] != postData['confirm']:
            errorlist.append('Confirm Password does not match Password!')
            status = False
        if len(postData['username']) < 3:
            errorlist.append('Username must be more than 3 characters!')
            status = False
        if len(postData['password']) < 1:
            errorlist.append('Must fill in a password!')
            status = False
        elif len(postData['password']) < 8:
            errorlist.append('Password must be more than 8 characters.')
            status = False
        if len(postData['confirm']) < 1:
            errorlist.append('Must fill in a password confirmation!')
            status = False
        if len(User.objects.filter(username = postData['username'])) > 0:
            errorlist.append('Username already registered!')
            status = False
        if status == False:
            return {'errors': errorlist}
        else:
            password = postData['password']
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            User.objects.create(username= postData['username'], password = hashed, location=postData['location'])
            return {'register': True}

    def login(self, postData):
        status = True
        errorlist = []
        user = User.objects.filter(username = postData['username'])
        if len(postData['username']) < 1:
            errorlist.append('Must fill in Username!')
            status = False
        if len(postData['password']) < 1:
            errorlist.append('Must fill in Password!')
            status = False
        else:
            if len(user) < 1:
                errorlist.append('Username not registered!')
                status = False
        if status == False:
            return {'errors': errorlist}
        else:
            if bcrypt.hashpw(postData['password'].encode(), user[0].password.encode()) == user[0].password:
                return {'login': True}
            else:
                status = False
                errorlist.append('Password does not match username!')
                return {'errors': errorlist}

class User(models.Model):
      username = models.CharField(max_length=200,  blank=True, null=True)
      password = models.CharField(max_length=200,  blank=True, null=True)
      location = models.CharField(max_length=200, blank=True, null=True)
      room = models.ForeignKey(Room, related_name="users", blank=True, null = True, on_delete=models.SET_NULL)
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)
      objects = UserManager()


class MessageManager(models.Manager):

    def addmessage(self, postData, roomid, user):
        if len(postData) < 1:
            return {'error': 'Nothing written!'}
        else:
            this_room = Room.objects.get(id = roomid)
            Message.objects.create(content=postData, message_room = this_room, creator = user)
            return {}

class Message(models.Model):
      content = models.TextField(max_length=1000)
      creator = models.ForeignKey(User, blank=True, null=True)
      message_room = models.ForeignKey(Room, related_name="messages", blank=True, null = True)
      created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
      updated_at = models.DateTimeField(auto_now = True)
      objects = MessageManager()
