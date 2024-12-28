include "alldifferent.mzn";

include "globals.mzn";

% Declare variables for the prices of the four items
var 0.0..10.0: x1;
var 0.0..10.0: x2;
var 0.0..10.0: x3;
var 0.0..10.0: x4;

% Constraint 1: The incorrect multiplication as stated by the cashier
constraint x1 * x2 * x3 * x4 = 7.11;

% Constraint 2: The correct addition of the prices
constraint x1 + x2 + x3 + x4 = 7.11;

% Solve the constraints
solve satisfy;

% Output the prices of the four items
