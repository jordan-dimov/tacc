from decimal import Decimal

from tacc import BalanceType, T


def test_t_initialised_correctly_without_arguments():
    t = T()
    assert(t.dr == 0)
    assert(t.cr == 0)
    assert(t.balance_type == BalanceType.DEBIT)
    assert(str(t) == "[0.00 // 0.00]")


def test_t_initialised_correctly_with_basic_arguments():
    t = T(5, 10)
    assert(t.dr == Decimal('5.00'))
    assert(t.cr == Decimal('10.00'))
    assert(t.balance_type == BalanceType.DEBIT)
    assert(str(t) == "[5.00 // 10.00]")
