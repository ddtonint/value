import datetime

from django.db import models
from django.utils import timezone


class WalletAddress(models.Model):
    wallet_address = models.CharField(max_length=200)
    
    def __str__(self):
        return self.wallet_address

class WalletBalance(models.Model):
    address = models.ForeignKey(WalletAddress, on_delete=models.CASCADE)
    value = models.FloatField(default=0)
    gvValue = models.FloatField(default=0)

    def __str__(self):
        return self.address.wallet_address

class Holder(models.Model):
    timestamp = models.DateTimeField('Date updated')
    # from block
    from_block = models.IntegerField(default=0)
    # to block
    to_block = models.IntegerField(default=0)
    # deposits
    deposits_count = models.IntegerField(default=0)
    # withdraws
    withdraws_count = models.IntegerField(default=0)
    # new wallets
    new_wallets = models.IntegerField(default=0)
    # wallets left value or gov vault
    left_wallets = models.IntegerField(default=0)
    # total wallets that hold value or in gov vault
    total_wallets = models.IntegerField(default=0)
    # total deposit
    total_deposit = models.FloatField(default=0)
    # total withdraw
    total_withdraw = models.FloatField(default=0)
    # total locked
    total_locked = models.FloatField(default=0)

    def __str__(self):
        return str(self.from_block) + ' - ' + str(self.to_block)

class VaultsPerformance(models.Model):
    timestamp = models.DateTimeField('Date updated')
    gov_vault = models.FloatField(default=0)

class SeedPoolHolder(models.Model):
    wallet_address = models.CharField(max_length=200)
    usdt_balance = models.FloatField(default=0)
    usdc_balance = models.FloatField(default=0)
    dai_balance = models.FloatField(default=0)
    
    def __str__(self):
        return self.wallet_address

class SingletonModel(models.Model):
    class Meta:
        abstract = None

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class TrackingSetting(SingletonModel):
    # datetime of latest update
    gv_latest_update = models.DateTimeField('Gov Vault latest update')
    # latest block number
    gv_latest_block_number = models.IntegerField(default=0)