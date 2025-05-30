from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from ads.forms import RegisterForm, LoginForm, AdForm, ExchangeProposalForm
from ads.models import Ad, Category, ExchangeProposal
from ads.utils import handle_not_found


def ad_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    condition = request.GET.get('condition', '')

    ads = Ad.objects.all()
    categories = Category.objects.all()

    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        ads = ads.filter(category=category)
    if condition:
        ads = ads.filter(condition=condition)

    paginator = Paginator(ads.order_by('-created_at'), 10)
    page = request.GET.get('page')
    ads_paginated = paginator.get_page(page)

    print(ads_paginated.paginator.num_pages)

    return render(request, 'ads/index.html', {'ads': ads_paginated, "categories": categories})


@handle_not_found
def ad_detail(request, ad_id):
    user_ads = []
    ad = get_object_or_404(Ad, pk=ad_id)
    form_proposal = ExchangeProposalForm()
    if request.user.is_authenticated:
        user_ads = Ad.objects.filter(user=request.user)
    return render(request, 'ads/item-detail.html', {'ad': ad, "form": form_proposal, "ads": user_ads})


@login_required
def user_ad_list(request):
    ads = Ad.objects.filter(user=request.user)
    return render(request, 'ads/my-items.html', {"ads": ads})


@login_required
@handle_not_found
def proposal_create(request, ad_receiver_id):
    if request.method == 'POST':
        ad_sender_id = request.POST.get("your-item", '')
        comment = request.POST.get("comment", '')

        ad_sender = get_object_or_404(Ad, pk=ad_sender_id)
        ad_receiver = get_object_or_404(Ad, pk=ad_receiver_id)

        ExchangeProposal.objects.create(ad_sender=ad_sender, ad_receiver=ad_receiver, comment=comment)

        return redirect('ad-detail', ad_id=ad_receiver_id)


@login_required
def user_proposal_list(request):
    proposals = ExchangeProposal.objects.filter(
        Q(ad_sender__user=request.user) | Q(ad_receiver__user=request.user)
    ).select_related('ad_sender', 'ad_receiver').order_by('-created_at')

    status = request.GET.get('status')
    if status:
        proposals = proposals.filter(status=status)

    return render(request, 'proposal/proposals.html', {'proposals': proposals})


@login_required
@handle_not_found
def proposal_accepted(request, proposal_id):

    proposal = get_object_or_404(ExchangeProposal, pk=proposal_id)
    if proposal.ad_receiver.user != request.user:
        return HttpResponseForbidden("Вы не можете обновить это предложение.")

    proposal.status = "accepted"
    proposal.save()
    return redirect('proposals')


@login_required
@handle_not_found
def proposal_rejected(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, pk=proposal_id)
    if proposal.ad_receiver.user != request.user:
        return HttpResponseForbidden("Вы не можете обновить это предложение.")

    proposal.status = "rejected"
    proposal.save()
    return redirect('proposals')


@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad-detail', ad_id=ad.id)
    else:
        form = AdForm()
    return render(request, 'ads/item-form.html', {'form': form})


@login_required
@handle_not_found
def ad_edit(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)
    if ad.user != request.user:
        return HttpResponseForbidden("Вы не можете редактировать это объявление.")
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad-detail', ad_id=ad.id)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/item-form.html', {'form': form})


@login_required
@handle_not_found
def ad_delete(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id)
    if ad.user != request.user:
        return HttpResponseForbidden("Вы не можете удалить это объявление.")
    ad.delete()
    return redirect('index')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматический вход после регистрации
            return redirect('index')  # заменить на нужный url
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form, "error": form.errors})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # заменить на нужный url
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form, "error": form.errors})


def logout_view(request):
    logout(request)
    return redirect('index')


