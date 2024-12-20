 % This is a MiniZinc model for solving a problem with 10 discrete variables with domain and constraints. 

int: n = 10;

array[1..n] of var 1..10: x;

constraint
  forall(i in 1..n-1) (
    x[i] < x[i+1]
  );

solve satisfy;