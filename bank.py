# This file is part of the bank_ar module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import fields
from trytond.pyson import Eval
from trytond.pool import PoolMeta

__all__ = ['Bank', 'BankAccount']


class Bank:
    __name__ = 'bank'
    __metaclass__ = PoolMeta

    bcra_code = fields.Char('BCRA code')

    @classmethod
    def check_xml_record(cls, records, values):
        return True


class BankAccount:
    __name__ = 'bank.account'
    __metaclass__ = PoolMeta

    journal = fields.Many2One('account.journal', 'Account Journal',
        required=True, states={'readonly': ~Eval('active', True)},
        depends=['active'])
