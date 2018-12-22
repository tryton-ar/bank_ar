# This file is part of the bank_ar module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from . import bank
from . import party


def register():
    Pool.register(
        bank.Bank,
        bank.BankAccount,
        bank.BankAccountNumber,
        party.Party,
        party.Address,
        party.Category,
        party.PartyCategory,
        module='bank_ar', type_='model')
