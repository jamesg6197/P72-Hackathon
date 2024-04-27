from django.core.management.base import BaseCommand
from ...stream_processing import main_graph
import csp
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Logic to populate the database
        csp.run(main_graph, realtime = True, starttime = datetime.datetime.utcnow())
