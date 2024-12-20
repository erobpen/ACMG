 % This is a MiniZinc model for a problem with 10 discrete variables with domain and without constraints. 

int: n = 10;

array[1..n] of var 1..n: x;

solve satisfy;