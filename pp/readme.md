The math formula and graph representation of each individual in CGP are presented.

Note that
1. The math formulas have been simplified, which thus do not correspond to the graphs directly. Each graph essentially encodes a non-simplified formula, though the weight of an edge is not shown for readability purpose.
2. In (MU, LAMBDA)-ES, only the MU parents have been evaluated at the end of each game run. Thus, only the first MU individuals have valid scores.
3. The `PP_FORMULA_NUM_DIGITS` parameter in [settings.py](../settings.py) controls the number of digits in math formulae.
4. The formulae can become very long and the generated graph can be very huge if `N_COLS` parameter is large.