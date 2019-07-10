import datetime
import random

from django.core.paginator import Paginator


class RandomizablePaginator(Paginator):
    @property
    def random_page_number(self):
        random.seed(datetime.datetime.now())
        return random.randint(0, self.count)
