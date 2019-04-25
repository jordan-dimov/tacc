from collections import defaultdict

from tacc import T


class TJournal:
    def __init__(self, TClass=T):
        self.TClass = TClass
        self.T0 = TClass()
        self._journal = defaultdict(TClass)

    def add_t(self, account_id, t):
        self._journal[account_id] += t

    @property
    def balance(self):
        return sum(self._journal.values(), self.T0)

    def is_balanced(self):
        return not bool(self.balance)

    def auto_balance(self, account_id):
        self.add_t(account_id, -self.balance)
