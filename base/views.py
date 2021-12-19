from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Service, User, Offer, Messages
from .forms import OfferForm


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
    context = {'offer': offer}
    return render(request, 'base/offer.html', context)

def createOffer(request):
    form = OfferForm()
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/offer_form.html', context)

def updateOffer(request, pk):
    offer = Offer.objects.get(id=pk)
    form = OfferForm(instance=offer)
    if request.method == 'POST':
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}

    return render(request, 'base/offer_form.html', context)

def deleteOffer(request, pk):
    offer = Offer.objects.get(id=pk)
    if request.method == 'POST':
        offer.delete()
        return redirect('home')

    context = {'obj': offer}

    return render(request, 'base/delete_offer.html', context)