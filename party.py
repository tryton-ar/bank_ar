# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import PoolMeta, Pool
from trytond.transaction import Transaction


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


class Address(metaclass=PoolMeta):
    __name__ = 'party.address'

    @classmethod
    def __register__(cls, module_name):
        pool = Pool()
        Data = pool.get('ir.model.data')
        data = Data.__table__()
        cursor = Transaction().connection.cursor()

        super(Address, cls).__register__(module_name)

        table = cls.__table_handler__(module_name)

        # Migration from 5.2: remove bank_ar data
        cursor.execute(*data.delete(where=(data.module == 'bank_ar')
                & (data.model == cls.__name__)))


class Category(metaclass=PoolMeta):
    __name__ = 'party.category'

    @classmethod
    def __register__(cls, module_name):
        pool = Pool()
        Data = pool.get('ir.model.data')
        data = Data.__table__()
        cursor = Transaction().connection.cursor()

        super(Category, cls).__register__(module_name)

        table = cls.__table_handler__(module_name)

        # Migration from 5.2: remove bank_ar data
        cursor.execute(*data.delete(where=(data.module == 'bank_ar')
                & (data.model == cls.__name__)))


class PartyCategory(metaclass=PoolMeta):
    __name__ = 'party.party-party.category'

    @classmethod
    def __register__(cls, module_name):
        pool = Pool()
        Data = pool.get('ir.model.data')
        data = Data.__table__()
        cursor = Transaction().connection.cursor()

        super(PartyCategory, cls).__register__(module_name)

        table = cls.__table_handler__(module_name)

        # Migration from 5.2: remove bank_ar data
        cursor.execute(*data.delete(where=(data.module == 'bank_ar')
                & (data.model == cls.__name__)))
