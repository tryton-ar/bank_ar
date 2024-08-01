# This file is part of the bank_ar module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool

from . import bank
from . import party

__all__ = ['register']

def register():
    Pool.register(
        bank.Bank,
        bank.Account,
        bank.AccountNumber,
        party.Party,
        party.Address,
        party.Category,
        party.PartyCategory,
        module='bank_ar', type_='model')
