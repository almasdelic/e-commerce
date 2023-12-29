from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages # for pop up messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
from django.core.mail import send_mail # For Email in Contact Form  
# from .models import Message

from django.db.models import Q


# Import Pagination Stuff
from django.core.paginator import Paginator


def thank_you(request):
    return render(request, 'thank_you.html', {})


def home(request):
    products = Product.objects.all()
    
    # Set up Pagination
    p = Paginator(Product.objects.all(), 8)
    page = request.GET.get('page')
    products_list = p.get_page(page)
    
    return render(request, 'index.html', {'products':products, 'products_list':products_list})


def about(request):
    return render(request, 'about.html', {})


def contact(request):
    if request.method == 'POST':
        message_name = request.POST['name']
        message_email = request.POST['email']
        message = request.POST['message']
        
        # Send an email
        '''send_mail(
            message_name, # subject
            message, # message
            message_email, # from email
            ['delic.almas2023@gmail.com'], # to email
        )
        '''
        return render(request, 'contact.html', {'message_name':message_name})
    
    else:
        return render(request, 'contact.html', {})



def login_user(request):
    if request.method == "POST":
        username = request.POST['username'] # taking username from login.html name username
        password = request.POST['password'] # taking password from login.html name password
        user = authenticate(request, username = username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in!"))
            return redirect('home')
        else:
            messages.success(request, ("You have entered a wrong username or password, please try again!"))
            return redirect('login')
        
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out!"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have registered successfully!"))
            return redirect('home')
        else:
            messages.success(request, ("There was a problem with Registering, please try again!"))
            return redirect('register')
        
    else:
        return render(request, 'register.html', {'form':form})
    
    
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})


def category(request, foo):
    # Replace hyphens with spaces
    foo = foo.replace('-',' ')
    # Grab the category from the url
    try:
        # Look up the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, ("That category doesn't exist..."))
        return redirect('home')
    
    
def search_results(request):
    query = request.GET.get('q', '')
    
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) # Koristi se Django ORM (Object-Relational Mapping) za pretragu objekata tipa Product. Pretraga se vrši po imenu 
        )
    else:
        results = []

    return render(request, 'search_results.html', {'results': results, 'query': query})
    

'''
def thankyou(request):
    submission_message = None

    if request.method == 'POST':

        message_content = request.POST.get('message')
        recipient = request.user
        message = Message.objects.create(sender=request.user, recipient=recipient, content=message_content)
        message.save()

        submission_message = "Thank you for your message!"  

    return render(request, 'templates/contact.html', {'submission_message': submission_message})
'''  
    
