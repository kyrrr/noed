from django.core.management.base import BaseCommand, CommandError
from twep.tweepyImpl import UserTweetsThing
from twep.settings import CSV_TIMESTAMP
import datetime


class Command(BaseCommand):

    help = 'Checks for new tweets by user and updates data'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str)

    def handle(self, *args, **options):
        now = datetime.datetime.now()
        u = UserTweetsThing(options['username'])


