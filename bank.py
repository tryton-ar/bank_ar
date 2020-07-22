# This file is part of the bank_ar module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from stdnum.ar import cbu
import stdnum.exceptions

from trytond.i18n import gettext
from trytond.model import fields
from trytond.pyson import Eval, If, In
from trytond.pool import PoolMeta, Pool
from trytond.transaction import Transaction

from .exceptions import CBUValidationError


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    @classmethod
    def __register__(cls, module_name):
        pool = Pool()
        Data = pool.get('ir.model.data')
        data = Data.__table__()
        cursor = Transaction().connection.cursor()

        super(Party, cls).__register__(module_name)

        table = cls.__table_handler__(module_name)

        # Migration from 5.2: remove bank_ar data
        cursor.execute(*data.delete(where=(data.module == 'bank_ar')
                & (data.model == cls.__name__)))


class Bank(metaclass=PoolMeta):
    __name__ = 'bank'

    bcra_code = fields.Char('BCRA code')

    @classmethod
    def __register__(cls, module_name):
        pool = Pool()
        Data = pool.get('ir.model.data')
        data = Data.__table__()
        cursor = Transaction().connection.cursor()

        super(Bank, cls).__register__(module_name)

        table = cls.__table_handler__(module_name)

        # Migration from 5.2: remove bank_ar data
        cursor.execute(*data.delete(where=(data.module == 'bank_ar')
                & (data.model == cls.__name__)))


class Account(metaclass=PoolMeta):
    __name__ = 'bank.account'

    journal = fields.Many2One('account.journal', 'Account Journal',
        states={
            'required': If(In(Eval('party_company'), Eval('owners', [])), True, False),
            },
        depends=['owners', 'party_company'])
    credit_account = fields.Many2One('account.account', 'Credit Account',
        states={
            'required': If(In(Eval('party_company'), Eval('owners', [])), True, False),
            },
        domain=[
            ('kind', '!=', 'view'),
            ('company', '=', Eval('context', {}).get('company', -1)),
            ], depends=['owners', 'party_company'])
    debit_account = fields.Many2One('account.account', 'Debit Account',
        states={
            'required': If(In(Eval('party_company'), Eval('owners', [])), True, False),
            },
        domain=[
            ('kind', '!=', 'view'),
            ('company', '=', Eval('context', {}).get('company', -1)),
            ], depends=['owners', 'party_company'])
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

    def get_cbu_number(self):
        '''
        Return cbu number
        '''
        for account_number in self.numbers:
            if account_number.type == 'cbu':
                return account_number.number_compact


class AccountNumber(metaclass=PoolMeta):
    __name__ = 'bank.account.number'

    @classmethod
    def default_type(cls):
        return 'cbu'

    @classmethod
    def __setup__(cls):
        super(AccountNumber, cls).__setup__()
        for new_type in [('cbu', 'CBU')]:
            if new_type not in cls.type.selection:
                cls.type.selection.append(new_type)

    @classmethod
    def create(cls, vlist):
        vlist = [v.copy() for v in vlist]
        for values in vlist:
            if values.get('type') == 'cbu' and 'number' in values:
                values['number'] = cbu.format(values['number'])
                values['number_compact'] = cbu.compact(values['number'])
        return super(AccountNumber, cls).create(vlist)

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

        super(AccountNumber, cls).write(*args)

        to_write = []
        for number in sum(args[::2], []):
            if number.type == 'cbu':
                formated_number = cbu.format(number.number)
                compacted_number = cbu.compact(number.number)
                if ((formated_number != number.number) or
                        (compacted_number != number.number_compact)):
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
        super(AccountNumber, self).pre_validate()
        if (self.type == 'cbu' and self.number
                and not cbu.is_valid(self.number)):
            raise CBUValidationError(
                gettext('bank_ar.msg_invalid_cbu',
                    number=self.number))
