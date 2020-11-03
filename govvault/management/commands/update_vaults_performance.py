from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import TrackingSetting
from ...chain_db_functions import update_gv_performance


class Command(BaseCommand):
    help = 'Update performance of Vaults'

    def add_arguments(self, parser):
        # mandatory argument
        #parser.add_argument('block', type=int, help='Indicates the block number')

        # Optional argument
        #parser.add_argument('-f', '--from_block', type=int, help='Indicates the block number', )
        #parser.add_argument('-t', '--to_block', type=int, help='Indicates the block number', )
        pass

    def handle(self, *args, **kwargs):
        update_gv_performance()

        self.stdout.write('Finished update command')