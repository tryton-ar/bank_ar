#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import fields
from trytond.pyson import Eval
from trytond.pool import PoolMeta


__all__ = ['Bank', 'BankAccount']
__metaclass__ = PoolMeta


class Bank:
    __name__ = 'bank'

    bcra_code = fields.Char('BCRA code')

    @classmethod
    def check_xml_record(cls, records, values):
        return True


class BankAccount:
    __name__ = 'bank.account'
    journal = fields.Many2One('account.journal', 'Account Journal',
        required=True, states={'readonly': ~Eval('active', True)},
        depends=['active'])
