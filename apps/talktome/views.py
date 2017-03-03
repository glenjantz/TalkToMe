from django.shortcuts import render, HttpResponse, redirect
from .models import User, Message, Room
from django.contrib import messages
from django.db.models import Count

def index(request):
    request.session['success'] = False
    return render(request, 'talktome/index.html')

def register(request):
    if request.method == "GET":
        messages.error(request, "Nice try. Register first.")
        return redirect('/')
    user = User.objects.register(request.POST)
    if 'errors' in user:
        error = user['errors']
        for one in error:
            messages.error(request, one)
        return redirect('/')
    if user['register'] == True:
        user = User.objects.filter(username = request.POST['username'])
        request.session['userid'] = user[0].id
        request.session['success'] = 'success'
    return redirect('/success')

def success(request):
    if ('userid' not in request.session) or ('success' not in request.session) or (request.session['success'] == False):
        messages.error(request, "Register or log in first.")
        return redirect('/')
    context= {'user': User.objects.get(id=request.session['userid']),
            'countUS': len(User.objects.filter(location = "United States of America")),
            'countRussia': len(User.objects.filter(location = "Russia")),
            'countGreenland': len(User.objects.filter(location = "Greenland")),
            'countCanada': len(User.objects.filter(location = "Canada")),
            'countChina': len(User.objects.filter(location = "China")),
            'countIndia': len(User.objects.filter(location = "India")),
            'countKorea': len(User.objects.filter(location = "Korea")),
            'countJapan': len(User.objects.filter(location = "Japan")),
            'countAustralia': len(User.objects.filter(location = "Australia")),
            'countBrazil': len(User.objects.filter(location = "Brazil")),
            }
    return render(request, 'talktome/success.html', context)

def login(request):
    if request.method == "GET":
        messages.error(request, "Nice try. Log in first.")
        return redirect('/')
    user = User.objects.login(request.POST)
    if 'errors' in user:
        error = user['errors']
        for one in error:
            messages.error(request, one)
        return redirect('/')
    if user['login'] == True:
        user = User.objects.filter(username = request.POST['username'])
        request.session['userid'] = user[0].id
        request.session['success'] = 'success'
    return redirect('/success')

def chatroom(request):
    if "userid" not in request.session:
        messages.error(request, 'Not logged in.')
        return redirect('/')
    rooms = Room.objects.filter(id=request.session['roomid'])
    if len(rooms) == 0:
        messages.error(request, 'the other user left you')
        return redirect('/success')
    context = {'room': Room.objects.annotate(count=Count('users')).get(id = request.session['roomid']),
                'user': User.objects.get(id = request.session['userid'])}
    return render(request, 'talktome/chat.html', context)

def makeroom(request):
    if "userid" not in request.session:
        return redirect('/')
    if request.method == "GET":
        return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    new_room = Room.objects.makeroom(request.POST, user)
    if 'error' in new_room:
        messages.error(request, message['error'])
        return redirect('/success')
    if 'room' in new_room:
        request.session['roomid'] = new_room['room'].id
    return redirect('/chatroom')

def deleteroom(request,roomid):
    if request.method == "GET":
        return redirect('/')
    rooms = Room.objects.filter(id=request.session['roomid'])
    if len(rooms) == 0:
        messages.error(request, 'the other user left you')
        return redirect('/success')
    Room.objects.get(id = roomid).delete()
    return redirect('/success')

def addmessage(request, roomid):
    if request.method == "GET":
        return redirect('/')
    rooms = Room.objects.filter(id=request.session['roomid'])
    if len(rooms) == 0:
        messages.error(request, 'the other user left you')
        return redirect('/success')
    user = User.objects.get(id=request.session['userid'])
    message = Message.objects.addmessage(request.POST['message'], roomid, user)
    if 'error' in message:
        messages.error(request, message['error'])
    return redirect('/chatroom')

def logout(request):
    if request.method == "GET":
        messages.error(request, "You need to log in to log out")
        return redirect('/')
    if "roomid" in request.session:
        del request.session['userid']
    if "roomid" in request.session:
        rooms = Room.objects.filter(id=request.session['roomid'])
        if len(rooms) == 1:
            Room.objects.get(id = request.session['roomid']).delete()
        del request.session['roomid']
    return redirect('/')
