% This is a MiniZinc model for solving a problem with an array of discrete variables with domain and with the constraint all_different.

int: n;
array[1..n] of var 1..n: x;

constraint all_different(x);

solve satisfy;
