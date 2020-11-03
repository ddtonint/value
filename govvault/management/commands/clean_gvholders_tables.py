from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import GovVaultWalletAddress, GovVaultWalletBalance, GovVaultHolders, GovVaultTrackingSetting


class Command(BaseCommand):
    help = 'Clear all records'

    def handle(self, *args, **kwargs):
        GovVaultWalletAddress.objects.all().delete()
        GovVaultWalletBalance.objects.all().delete()
        GovVaultHolders.objects.all().delete()
        GovVaultTrackingSetting.objects.all().delete()

        # create settings
        GovVaultTrackingSetting.objects.create(gv_latest_update=timezone.now(), gv_latest_block_number=0)

        self.stdout.write('Finished command')