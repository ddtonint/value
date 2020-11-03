from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import TrackingSetting
from ...chain_db_functions import update_gvValue_holders_tables


class Command(BaseCommand):
    help = 'Update Gov Vault v2 holders tables'

    def add_arguments(self, parser):
        # mandatory argument
        #parser.add_argument('block', type=int, help='Indicates the block number')

        # Optional argument
        parser.add_argument('-f', '--from_block', type=int, help='Indicates the block number', )
        parser.add_argument('-t', '--to_block', type=int, help='Indicates the block number', )

    def handle(self, *args, **kwargs):
        from_block_number = kwargs['from_block']
        if from_block_number:
            pass
        else:
            settings = TrackingSetting.load()
            from_block_number = settings.gv_latest_block_number
        print('Updated from block: ' + str(from_block_number))

        to_block_number = kwargs['to_block']
        if to_block_number:
            print('to block: ' + str(to_block_number))
            update_gvValue_holders_tables(from_block_number, to_block_number)
        else:
            print('to latest block')
            update_gvValue_holders_tables(from_block_number)

        self.stdout.write('Finished update command')