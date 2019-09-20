# This file is part of the bank_ar module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from stdnum.ar import cbu

from trytond.model import fields
from trytond.pyson import Eval, If, In
from trytond.pool import PoolMeta, Pool
from trytond.transaction import Transaction

__all__ = ['Bank', 'BankAccount', 'BankAccountNumber']

NUMBERTYPE = [
    ('cbu', 'CBU'),
    ('iban', 'IBAN'),
    ('other', 'Other'),
    ]


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
    party_company = fields.Function(fields.Many2One('party.party', 'party_company'),
        'on_change_with_party_company')

    @staticmethod
    def default_party_company():
        Company = Pool().get('company.company')
        if Transaction().context.get('company'):
            company = Company(Transaction().context['company'])
            return company.party.id

    def on_change_with_party_company(self, name=None):
        Company = Pool().get('company.company')
        if Transaction().context.get('company'):
            company = Company(Transaction().context['company'])
            return company.party.id

    def get_cbu_number(self, name):
        for account_number in self.numbers:
            if account_number.type == 'cbu':
                return account_number.number_compact


class BankAccountNumber:
    __metaclass__ = PoolMeta
    __name__ = 'bank.account.number'

    @classmethod
    def default_type(cls):
        return 'cbu'

    @classmethod
    def __setup__(cls):
        super(BankAccountNumber, cls).__setup__()
        cls.type.selection = NUMBERTYPE

        cls._error_messages.update({
                'invalid_cbu': 'Invalid CBU "%s".',
                })

    @classmethod
    def create(cls, vlist):
        vlist = [v.copy() for v in vlist]
        for values in vlist:
            if values.get('type') == 'cbu' and 'number' in values:
                values['number'] = cbu.format(values['number'])
                values['number_compact'] = cbu.compact(values['number'])
        return super(BankAccountNumber, cls).create(vlist)

    @classmethod
    def write(cls, *args):
        actions = iter(args)
        args = []
        for numbers, values in zip(actions, actions):
            values = values.copy()
            if values.get('type') == 'cbu' and 'number' in values:
                values['number'] = cbu.format(values['number'])
                values['number_compact'] = cbu.compact(values['number'])
            args.extend((numbers, values))

        super(BankAccountNumber, cls).write(*args)

        to_write = []
        for number in sum(args[::2], []):
            if number.type == 'cbu':
                formated_number = cbu.format(number.number)
                compacted_number = cbu.compact(number.number)
                if ((formated_number != number.number)
                        or (compacted_number != number.number_compact)):
                    to_write.extend(([number], {
                                'number': formated_number,
                                'number_compact': compacted_number,
                                }))
        if to_write:
            cls.write(*to_write)

    @property
    def compact_cbu(self):
        return (cbu.compact(self.number) if self.type == 'cbu'
            else self.number)

    @fields.depends('type', 'number')
    def pre_validate(self):
        super(BankAccountNumber, self).pre_validate()
        if (self.type == 'cbu' and self.number
                and not cbu.is_valid(self.number)):
            self.raise_user_error('invalid_cbu', self.number)
