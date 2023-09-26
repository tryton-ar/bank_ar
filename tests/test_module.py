# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.modules.company.tests import CompanyTestMixin
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool


class BankArTestCase(CompanyTestMixin, ModuleTestCase):
    'Test bank_ar module'
    module = 'bank_ar'

    @with_transaction()
    def test_cbu_format(self):
        'Test CBU format'
        pool = Pool()
        Party = pool.get('party.party')
        Bank = pool.get('bank')
        Account = pool.get('bank.account')
        Number = pool.get('bank.account.number')

        party = Party(name='Test')
        party.save()
        bank = Bank(party=party)
        bank.save()
        account, = Account.create([{
                    'bank': bank.id,
                    'numbers': [('create', [{
                                    'type': 'cbu',
                                    'number': '2850590940090418135201'
                                    }, {
                                    'type': 'other',
                                    'number': 'not CBU',
                                    }])],
                    }])

        cbu_number, other_number = account.numbers
        self.assertEqual(cbu_number.type, 'cbu')
        self.assertEqual(other_number.type, 'other')

        # Test format on create
        self.assertEqual(cbu_number.number, '28505909 40090418135201')
        self.assertEqual(other_number.number, 'not CBU')

        # Test format on write
        cbu_number.number = '2850590940090418135201'
        cbu_number.type = 'cbu'
        cbu_number.save()
        self.assertEqual(cbu_number.number, '28505909 40090418135201')

        other_number.number = 'still not CBU'
        other_number.save()
        self.assertEqual(other_number.number, 'still not CBU')

        Number.write([cbu_number, other_number], {
                'number': '2850590940090418135201',
                })
        self.assertEqual(cbu_number.number, '28505909 40090418135201')
        self.assertEqual(other_number.number, '2850590940090418135201')


del ModuleTestCase
