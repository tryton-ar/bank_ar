# This file is part of the bank_ar module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import PoolMeta

__all__ = ['Party', 'Address', 'Category', 'PartyCategory']


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    @classmethod
    def check_xml_record(cls, records, values):
        return True


class Address(metaclass=PoolMeta):
    __name__ = 'party.address'

    @classmethod
    def check_xml_record(cls, records, values):
        return True


class Category(metaclass=PoolMeta):
    __name__ = 'party.category'

    @classmethod
    def check_xml_record(cls, records, values):
        return True


class PartyCategory(metaclass=PoolMeta):
    __name__ = 'party.party-party.category'

    @classmethod
    def check_xml_record(cls, records, values):
        return True
