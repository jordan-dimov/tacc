# tacc
## Multi-dimensional T-accounts implementation in Python

This module provides a pure-Python implementation of the T-accounts data strucutre used in Double-Entry accounting, as first described by Luca Pacioli in 1494 ([1]), as well as a multi-dimensional generalisation of the same (MDT), for convenient support of multi-currency / multi-unit bookkeeping. 

Provided is a sample auto-balancing Journal class, using either T or MDT accounts. 

### Multi-what now?

In accounting, _T-accounts_ have historically been used as visual representations of the movement of resources within an account. Think about a sheet in a 15-th century accountant's notebook, where you draw a horisontal line on top and a vertical line down the middle, forming a T-shape. Above the top line, you write the name of the account (e.g. "Assets"). In the left column, you enter debits (what we owe); on the right side you enter credits (what is owed to us). 

         Assets 
    =================
     Dr     | Cr
     500.00 | 
            | 250.00
            | 250.00

Note that the numbers in each column are always positive - or, more precisely, unsigned. We can interpret them differently based on the nature of the account. Let's call this `BalanceType`. In a _debit-balance_ account, debits are interpreted as positive numbers and credits as negative numbers. For example, accountants think of the Assets account as a debit-balance account, because the left side represents an increase in assets and the right side represents a decrease. Conversely, Liabilities and Equity are thought of as _credit-balance_ accounts. 

     Assets       Liabilities      Equity
    =========     ===========     =========
     Dr | Cr       Dr  |  Cr       Dr | Cr 
     +  | -        -   |  +        -  | +


The examples above assume that we are using a single unit of currency across our accounts. It is common for more complex enterprises to require accounting in different currencies or units. T-accounts can be used to represent this with a further sub-division of the columns, like so:


                   Assets 
    =====================================
     Dr              || Cr
    -------------------------------------
    GBP    | BitCoin || GBP    | BitCoin
    500.00 | 0.35    ||        |
           |         || 250.00 | 0.35
           |         || 250.00 |

We call these "_multi-dimensional T-accounts_". 

As noted by D. Ellerman in [2], it turns out that the concept of T-accounts maps very neatly into the mathematical (group theory) concept of the "_group of differences_". A T-account can be mapped to an ordered pair of unsigned real numbers, written (per Luca Pacioli) as: `[ Dr // Cr ]`. We can then construct a number system with additive inverses by using operations on these ordered pairs. This is essentially the same algebra used to work with complex numbers, just with different semantics. 

Also as noted by D. Ellerman, we can easily generalise this mathematical concept by using vectors to represent multi-dimmensional T-accounts, e.g. `[ Dr(GBP, BitCoin) // Cr(GBP, BitCoin) ]`

The `tacc` library defines Python classes that encapsulate both traditional and multi-dimensional T accounts, together with the common algebraic operations one would expect to be able to use with T-accounts in the context of bookkeeping. 

### Python examples

(Coming soon. Meanwhile, review the provided unit tests. )


## Refrences

* [1] Pacioli, Luca. "_Summa de arithmetica, proportioni et proportionalita._" Venecia: Paganino Paganini.
* [2] Ellerman, David. "_On double-entry bookkeeping: The mathematical treatment._" Accounting Education 23.5 (2014): 483-501.
