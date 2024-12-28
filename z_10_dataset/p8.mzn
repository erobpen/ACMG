 % This is a MiniZinc model for an array of discrete variables with domain and without constraints. 

int: n = 5;
array[1..n] of var 1..n: x;

constraint forall(i in 1..n) (x[i] = i);

solve satisfy;
