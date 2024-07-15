import json

from dataset_generator.ticket_fields.queue import Queue
from dataset_generator.ticket_fields.random_collection import IRandomCollection, RandomCollection


def get_hardware_products():
    return json.load(open("../input/hardware_products.json", encoding="utf-8"))


hardware_collection = RandomCollection.from_value_list(get_hardware_products())


def get_software_products():
    return json.load(open("../input/software_products.json", encoding="utf-8"))


software_collection = RandomCollection.from_value_list(get_software_products())


def get_accounting_products():
    return json.load(open("../input/accounting_categories.json", encoding="utf-8"))


accounting_collection = RandomCollection.from_value_list(get_accounting_products())


class SubCategoryRandomCollection(IRandomCollection):
    def __init__(self):
        self.collection_dict = {
            Queue.HARDWARE: hardware_collection,
            Queue.SOFTWARE: software_collection,
            Queue.ACCOUNTING: accounting_collection
        }

    def get_random_value(self, queue, **kwargs):
        return self.collection_dict[queue].get_random_value()
