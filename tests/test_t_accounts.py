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


def test_t_initialised_correctly_with_extra_arguments():
    t = T(
        100.00, 20.00,
        balance_type=BalanceType.CREDIT,
        account_name="Fruit exchange",
        label="apples",
    )
    assert(t.dr == Decimal('100.00'))
    assert(t.cr == Decimal('20.00'))
    assert(t.balance_type == BalanceType.CREDIT)
    assert(t.account_name == "Fruit exchange")
    assert(t.labels == ("apples",))


def test_t_balance_for_debit_balance():
    t = T(100, 20, balance_type=BalanceType.DEBIT)
    assert(t.balance == 100 - 20)


def test_t_balance_for_credit_balance():
    t = T(100, 20, balance_type=BalanceType.CREDIT)
    assert(t.balance == 20 - 100)


def test_t_equality():
    assert(T(100, 100) == T(0, 0))
    assert(T(100, 20) == T(80, 0))
    assert(T(20, 100) == T(0, 80))
    assert(T(10, 20) == T(90, 100))


def test_t_addition():
    assert(T(100, 200) + T(20, 50)) == T(120, 250)


def test_t_substraction():
    assert(T(100, 200) - T(20, 50)) == T(80, 150)


def test_t_bool():
    assert(bool(T(0, 0)) is False)
    assert(bool(T(50, 50)) is False)
    assert(bool(T(50, 0)) is True)
    assert(bool(T(0, 0.1)) is True)


def test_balance_for_debit_balance_t_account():
    class DebitT(T):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.balance_type = BalanceType.DEBIT

    assert(DebitT(0, 0).balance == Decimal('0.00'))
    assert(DebitT(25, 0).balance == Decimal('25.00'))
    assert(DebitT(25, 5).balance == Decimal('20.00'))
    assert(DebitT(5, 25).balance == Decimal('-20.00'))


def test_balance_for_credit_balance_t_account():
    class DebitT(T):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.balance_type = BalanceType.CREDIT

    assert(DebitT(0, 0).balance == Decimal('0.00'))
    assert(DebitT(25, 0).balance == Decimal('-25.00'))
    assert(DebitT(25, 5).balance == Decimal('-20.00'))
    assert(DebitT(5, 25).balance == Decimal('20.00'))


def test_t_account_as_tuple():
    assert(T(23, 34).as_tuple()) == (Decimal('23.00'), Decimal('34.00'))
