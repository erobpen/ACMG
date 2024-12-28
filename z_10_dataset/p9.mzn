 % This is a MiniZinc model for solving an array of discrete variables with domain and constraints. 

int: n = 5;
array[1..n] of var 1..n: x;

constraint forall(i in 1..n-1) (x[i] != x[i+1]);

solve satisfy;
