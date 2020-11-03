from django.contrib import admin

from .models import WalletAddress, WalletBalance, Holder, SeedPoolHolder, TrackingSetting

admin.site.register(WalletAddress)
admin.site.register(WalletBalance)
admin.site.register(Holder)
admin.site.register(SeedPoolHolder)
admin.site.register(TrackingSetting)
