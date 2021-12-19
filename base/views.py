from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Service, User, Offer, Messages
from .forms import OfferForm, UserForm



def registerPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Por favor, revisa los campos')

    context = {'form': form}
    return render(request, 'base/login_register.html', context)

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrecta')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    offers = Offer.objects.filter(Q(service__name__icontains=q)|
                            Q(title__icontains=q)|
                            Q(description__icontains=q))

    offer_count = offers.count()
    services = Service.objects.all()
    context = {'offers': offers, 'offer_count': offer_count, 'services': services}
    return render(request, 'base/home.html', context)

def offer(request, pk):
    offer = Offer.objects.get(id=pk)

    offer_messages = offer.messages_set.all()

    if request.method == 'POST':
        message = Messages.objects.create(
            offer=offer,
            sender=request.user,
            content=request.POST.get('content')
        )
        return redirect('offer', pk=offer.id)

    context = {'offer': offer, 'offer_messages': offer_messages}
    return render(request, 'base/offer.html', context)

@login_required(login_url='login')
def createOffer(request):
    form = OfferForm()
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/offer_form.html', context)

@login_required(login_url='login')
def updateOffer(request, pk):
    offer = Offer.objects.get(id=pk)
    form = OfferForm(instance=offer)

    if request.user != offer.user:
        messages.error(request, 'No tienes permisos para editar esta oferta')
        return redirect('home')

    if request.method == 'POST':
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}

    return render(request, 'base/offer_form.html', context)

@login_required(login_url='login')
def deleteOffer(request, pk):
    offer = Offer.objects.get(id=pk)

    if request.user != offer.user:
        messages.error(request, 'No tienes permisos para eliminar esta oferta')
        return redirect('home')

    if request.method == 'POST':
        offer.delete()
        return redirect('home')

    context = {'obj': offer}

    return render(request, 'base/delete_offer.html', context)