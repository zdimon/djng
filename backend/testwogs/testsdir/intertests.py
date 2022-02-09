""""
BaseTests - base class (interface) for all application tests
"""

from abc import ABCMeta, abstractmethod


class BaseTests(metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def run_test(self, domain_name, account):
        pass