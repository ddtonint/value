import json
import time

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone

from .models import WalletAddress, WalletBalance, Holder, VaultsPerformance, SeedPoolHolder, TrackingSetting

"""
views
"""
def index(request):
    context = {
        'task_info': 'hello',
    }
    return render(request, 'govvault/index.html', context)

def test(request):
    gvHolders_info = Holder.objects.all()
    
    timestamp = []
    total_wallets = []
    for item in gvHolders_info:
        timestamp.append(item.timestamp)
        total_wallets.append(item.total_wallets)

    context = {
        'timestamp': timestamp,
        'total_wallets': total_wallets,
    }
    return render(request, 'govvault/test.html', context)

def pie_chart(request):
    labels = []
    data = []

    queryset = WalletBalance.objects.order_by('-gvValue')[:5]
    for balance in queryset:
        labels.append(balance.address.wallet_address)
        data.append(balance.gvValue)

    return render(request, 'govvault/pie_chart.html', {
        'labels': labels,
        'data': data,
    })

def gv_total_holders(request):
    labels = []
    gv_total_wallets_data = []
    active_wallets_data = []
    new_wallets_data = []
    left_wallets_data = []

    queryset = Holder.objects.all()
    for entry in queryset:
        labels.append(entry.timestamp.date())
        gv_total_wallets_data.append(entry.total_wallets)
        active_wallets_data.append(entry.deposits_count + entry.withdraws_count)
        new_wallets_data.append(entry.new_wallets)
        left_wallets_data.append(entry.left_wallets)
    
    return JsonResponse(data={
        'labels': labels,
        'gv_total_wallets_data': gv_total_wallets_data,
        'active_wallets_data': active_wallets_data,
        'new_wallets_data': new_wallets_data,
        'left_wallets_data': left_wallets_data
    })

def top_gvholders(request):
    labels = []
    top_gvholders_data = []

    queryset = WalletBalance.objects.order_by('-gvValue')[:10]
    for entry in queryset:
        labels.append(entry.address.wallet_address[:6] + '...' + entry.address.wallet_address[-4:])
        top_gvholders_data.append(entry.gvValue)

    return JsonResponse(data={
        'labels': labels,
        'top_gvholders_data': top_gvholders_data,
    })

def value_flow(request):
    labels = []
    diff_value_data = []
    locked_value_data = []

    queryset = Holder.objects.all()
    for entry in queryset:
        diff_amount = entry.total_deposit-entry.total_withdraw
        labels.append(entry.timestamp.date())        
        diff_value_data.append(diff_amount)
        locked_value_data.append(entry.total_locked)
        
    return JsonResponse(data={
        'labels': labels,
        'diff_value_data': diff_value_data,
        'locked_value_data': locked_value_data
    })

def vaults_performance(request):
    labels = []
    gv_price_per_share_data = []

    queryset = VaultsPerformance.objects.all()
    for entry in queryset:
        labels.append(entry.timestamp.date())        
        gv_price_per_share_data.append(entry.gov_vault)
        
    return JsonResponse(data={
        'labels': labels,
        'gv_price_per_share_data': gv_price_per_share_data,
    })

def seedpool_holders(request):
    labels = []
    seedpool_holders_data = []

    queryset = SeedPoolHolder.objects.all()
    for entry in queryset:
        amount = entry.usdt_balance + entry.usdc_balance + entry.dai_balance
        labels.append(entry.wallet_address[:6] + '...' + entry.wallet_address[-4:])
        seedpool_holders_data.append(amount)
        
    return JsonResponse(data={
        'labels': labels,
        'seedpool_holders_data': seedpool_holders_data,
        'chart_title': 'Seed Pool Holders: ' + str(len(queryset))
    })