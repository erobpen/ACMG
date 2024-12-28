 % This is a MiniZinc model for a problem with 10 discrete variables with domain and with the constraint all_different.

int: n = 10;

array[1..n] of var 1..n: x;

constraint all_different(x);

solve satisfy;
