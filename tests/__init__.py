try:
    from trytond.modules.bank_ar.tests.tests import suite
except ImportError:
    from .tests import suite

__all__ = ['suite']
