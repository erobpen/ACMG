 % This is a MiniZinc model for solving a problem with 10 discrete variables without domain and with constraints. 

var int: x1;
var int: x2;
var int: x3;
var int: x4;
var int: x5;
var int: x6;
var int: x7;
var int: x8;
var int: x9;
var int: x10;

% Constraints
constraint x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 = 10;
