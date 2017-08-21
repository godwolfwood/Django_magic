from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from time import gmtime, strftime, localtime
from django.contrib import messages

# Need this in order to run queries
from .models import * 

from django.core.urlresolvers import reverse
import bcrypt

# Create views here.
def index(request):
    if 'user_id' not in request.session:
        request.session['user_id']=0
    return render(request, 'poke/index.html')

# action /login
def login(request):
    result = User.objects.login_validator(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect(reverse('index'))
    request.session['user_id'] = result.id
    return redirect(reverse('success'))

# action /register
def register(request):
    result = User.objects.reg_validator(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect(reverse('index'))
    request.session['user_id'] = result.id
    return redirect(reverse('success'))

def success(request):
    user_id = request.session['user_id']
    user_name = User.objects.get(id = user_id).alias
    poked_me = Poke.objects.filter(receivedPoke = User.objects.get(id = user_id))
    user_list = User.objects.exclude(id = user_id)
    num_pokers = poked_me.count()

    context = {
        'user_name': user_name,
        'user_list': user_list,
        'num_pokers': num_pokers,
        'poke_list': poked_me,
    }

    return render(request, "poke/success.html", context)

def pokes(request):
    if request.method == 'POST':
        new_poke = Poke.objects.create(createdPoke = User.objects.get(id = request.session['user_id']), receivedPoke = User.objects.get(name = request.POST['poker_name']))
        new_poke.save()
        poker = User.objects.get(id = request.session['user_id'])
        poker.poke_time +=1
        poker.save()
    return redirect(reverse('success'))
    
def logout(request):
    try:
        request.session.clear()
        return redirect(reverse('index'))
    except:
        return redirect(reverse('index'))
