
int: num_floors;
array[1..num_floors] of var 1..num_floors: floors; % floors assigned to individuals

% Individuals
var int: baker = floors[1];
var int: cooper = floors[2];
var int: fletcher = floors[3];
var int: miller = floors[4];
var int: smith = floors[5];

% Constraints
constraint baker != 5;                      % Baker does not live on the fifth floor
constraint cooper != 1;                     % Cooper does not live on the first floor
constraint fletcher != 1 /\ fletcher != 5; % Fletcher does not live on the fifth or first floor
constraint miller > cooper;                  % Miller lives on a higher floor than Cooper
constraint abs(smith - fletcher) > 1;       % Smith does not live on a floor adjacent to Fletcher"s
constraint abs(fletcher - cooper) > 1;      % Fletcher does not live on a floor adjacent to Cooper"s
constraint all_different([baker, cooper, fletcher, miller, smith]); % All live on different floors

solve satisfy;

