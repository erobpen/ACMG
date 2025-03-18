
% MiniZinc model
int: a; % from dzn
int: b; % from dzn

% Constraints
constraint a + b <= 10;

% Solve statement
solve satisfy;

% Output
