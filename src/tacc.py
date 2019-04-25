from collections import namedtuple
from decimal import Decimal
from enum import Enum
from typing import Any, Tuple


DEFAULT_UNIT = 'GBP'

D0 = Decimal('0.00')
ZERO_TUPLE = (D0, )


class BalanceType(Enum):
    DEBIT = -1
    CREDIT = 1


class MDT:
    """
    Multi-dimensional T-account
    """

    def __init__(
        self,
        drs: Tuple[Any] = ZERO_TUPLE,
        crs: Tuple[Any] = ZERO_TUPLE,
        balance_type: BalanceType = BalanceType.DEBIT,
        account_name: str = '',
        labels: Tuple[str] = None,
    ) -> None:
        self.cardinality = max(len(drs), len(crs), len(labels))
        self.labels = labels or (
            [DEFAULT_UNIT] + [f'label_{i}' for i in range(self.cardinality-1)]
        )
        defaults = [D0] * self.cardinality
        self.AmountVector = namedtuple(
            'AmountVector',
            self.labels,
            defaults=defaults,
        )
        self.drs = self.AmountVector(*(abs(Decimal(dr)) for dr in drs))
        self.crs = self.AmountVector(*(abs(Decimal(cr)) for cr in crs))
        self._tuple: Tuple[Decimal, Decimal] = (self.drs, self.crs)
        self.balance_type: BalanceType = balance_type
        self.account_name = account_name
        return None

    def clone(self, drs: Tuple[Any] = None, crs: Tuple[Any] = None) -> 'MDT':
        return MDT(
            drs or self.drs, crs or self.crs,
            balance_type=self.balance_type,
            labels=self.labels,
        )

    def __str__(self) -> str:
        return "[({}) // ({})]".format(
                ", ".join("{:.2f}".format(d) for d in self.drs),
                ", ".join("{:.2f}".format(c) for c in self.crs),
        )

    def __repr__(self) -> str:
        return str(self)

    def __getitem__(self, idx) -> Decimal:
        return (self.drs[idx], self.crs[idx])

    def as_tuple(self) -> Tuple[Decimal, Decimal]:
        return self._tuple

    def __neg__(self) -> 'MDT':
        return self.clone(self.crs, self.drs)

    def __pos__(self) -> 'MDT':
        return self.clone(self.drs, self.crs)

    def __add__(self, other: 'MDT') -> 'MDT':
        return self.clone(
            tuple(d1 + d2 for d1, d2 in zip(self.drs, other.drs)),
            tuple(c1 + c2 for c1, c2 in zip(self.crs, other.crs)),
        )

    def __sub__(self, other: 'MDT') -> 'MDT':
        return self.clone(
            tuple(d1 - d2 for d1, d2 in zip(self.drs, other.drs)),
            tuple(c1 - c2 for c1, c2 in zip(self.crs, other.crs)),
        )

    def __eq__(self, other: 'MDT') -> 'MDT':
        if self.cardinality != other.cardinality:
            return False
        return all((self.drs[i] + other.crs[i]) == (self.crs[i] + other.drs[i])
                   for i in range(self.cardinality))

    def __bool__(self):
        return self != T0

    @property
    def debit_balance(self) -> Decimal:
        return self.AmountVector(d - c for d, c in zip(self.drs, self.crs))

    @property
    def credit_balance(self) -> Decimal:
        return self.AmountVector(c - d for d, c in zip(self.drs, self.crs))

    @property
    def balance(self) -> Decimal:
        if self.balance_type == BalanceType.DEBIT:
            return self.debit_balance
        return self.credit_balance

    def is_disjoint(self) -> bool:
        return all(d == D0 for d in self.drs) or all(c == D0 for c in self.crs)

    def reduce(self) -> 'MDT':
        # TODO: How do you *actually* reduce a multi-dimensional T?
        drs = []
        crs = []
        for d, c in zip(self.drs, self.crs):
            min_a = min(d, c)
            drs.append(d - min_a)
            crs.append(c - min_a)
        return self.clone(tuple(drs), tuple(crs))


class T(MDT):
    """
    Traditional (one-dimensional) T account
    """
    def __init__(
        self,
        dr=D0,
        cr=D0,
        balance_type: BalanceType = BalanceType.DEBIT,
        account_name: str = '',
        label: str = DEFAULT_UNIT,
    ):
        super().__init__(
            (dr,), (cr,),
            balance_type=balance_type,
            account_name=account_name,
            labels=(label,),
        )

    @property
    def dr(self) -> 'T':
        return self.drs[0]

    @property
    def cr(self) -> 'T':
        return self.crs[0]

    def __str__(self) -> str:
        return "[{:.2f} // {:.2f}]".format(self.dr, self.cr)

    @property
    def debit_balance(self) -> Decimal:
        return self.dr - self.cr

    @property
    def credit_balance(self) -> Decimal:
        return self.cr - self.dr


T0 = T(0, 0)
