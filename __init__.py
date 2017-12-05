# This file is part of the bank_ar module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from .bank import *
from .party import *


def register():
    Pool.register(
        Bank,
        BankAccount,
        BankAccountNumber,
        Party,
        Address,
        Category,
        PartyCategory,
        module='bank_ar', type_='model')
