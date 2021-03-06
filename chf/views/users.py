__author__ = 'Cody'

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import HttpRequest
from django_mako_plus.controller import view_function
from django.shortcuts import render
from django_mako_plus.controller.router import get_renderer
import chf.models as chfmod
from django.shortcuts import render
from django_mako_plus.controller.router import get_renderer
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import permission_required

templater = get_renderer('chf')

@view_function
#@permission_required('chf.add_user')
def process_request(request):

    params = {}

    users = chfmod.User.objects.all()
    params['users'] = users


    return templater.render_to_response(request, '/users.html', params)


###############################################################

@view_function
def edit(request):

    params = {}

    try:
        user = chfmod.User.objects.get(id=request.urlparams[0])
    except:
        return HttpResponseRedirect('/users')

    form = UserEditForm(initial={
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,

    })
    if request.method == 'POST':
        form = UserEditForm(request.POST)
        form.userid = user.id
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()
            return HttpResponseRedirect('/users')


    params['form'] = form
    return templater.render_to_response(request, '/users.edit.html', params)

class UserEditForm(forms.Form):
    username = forms.CharField(required=True, max_length=100)
    email = forms.CharField(required=True, max_length=100)
    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)


    def clean_username(self):
        user_count = chfmod.User.objects.filter(username=self.cleaned_data['username']).exclude(id=self.userid).count()
        if user_count >=1:
            raise forms.ValidationError("This username is already taken.")
        username=self.cleaned_data['username']
        if len(username) < 4:
            raise forms.ValidationError("Username needs to have at least 4 characters.")

        return self.cleaned_data['username']


@view_function
def create(request):
    '''Create new user'''
    user = chfmod.User()
    user.first_name = ""
    user.last_name = ""
    user.email = ""
    user.username = ""
    user.set_password("password")
    user.is_superuser = False
    user.is_staff = False
    user.is_active = True
    user.save()

    return HttpResponseRedirect('/users.edit/{}'.format(user.id))


###########################################################################

@view_function
def delete(request):

    params = {}

    try:
        user = chfmod.User.objects.get(id=request.urlparams[0])
    except:
        return HttpResponseRedirect('/users')

    user.delete()
    return HttpResponseRedirect('/users')


