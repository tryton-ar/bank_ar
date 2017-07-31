# This file is part of the bank_ar module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import PoolMeta

__all__ = ['Party', 'Address', 'Category', 'PartyCategory']


class Party:
    __name__ = 'party.party'
    __metaclass__ = PoolMeta

    @classmethod
    def check_xml_record(cls, records, values):
        return True


class Address:
    __name__ = 'party.address'
    __metaclass__ = PoolMeta

    @classmethod
    def check_xml_record(cls, records, values):
        return True


class Category:
    __name__ = 'party.category'
    __metaclass__ = PoolMeta

    @classmethod
    def check_xml_record(cls, records, values):
        return True


class PartyCategory:
    __name__ = 'party.party-party.category'
    __metaclass__ = PoolMeta

    @classmethod
    def check_xml_record(cls, records, values):
        return True
