include "alldifferent.mzn";


int: n;  % Number of variables
array[1..n] of var 0..10: x;  % Decision variables

% Example constraint: the sum of x should be equal to a given total
int: total;  
constraint sum(x) = total;

solve satisfy;

