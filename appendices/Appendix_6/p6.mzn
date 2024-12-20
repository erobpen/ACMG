 % This is a MiniZinc model for an array of discrete variables without domain and without constraints. 

int: n = 3;
array[1..n] of var 0..n: x;

solve satisfy;
