include "alldifferent.mzn";


int: num_floors; % from dzn
int: num_people; % from dzn

array[1..num_people] of int: floors; % from dzn
array[1..num_people] of set of int: cannot_occupy; % from dzn
array[1..num_people, 1..num_people] of bool: higher_than; % from dzn
array[1..num_people, 1..num_people] of bool: cannot_be_adjacent; % from dzn

% Each person must occupy a specific floor
array[1..num_people] of var 1..num_floors: assigned_floors;

% Constraint: Each person cannot occupy certain floors
constraint forall(p in 1..num_people)(
    assigned_floors[p] not in cannot_occupy[p]
);

% Constraint: Relative positions must be maintained
constraint forall(p1, p2 in 1..num_people where p1 != p2)(
    (higher_than[p1, p2] -> assigned_floors[p1] > assigned_floors[p2]) /\
    (higher_than[p2, p1] -> assigned_floors[p2] > assigned_floors[p1])
);

% Constraint: No adjacency between certain individuals
constraint forall(p1, p2 in 1..num_people where p1 != p2)(
    (cannot_be_adjacent[p1, p2] -> abs(assigned_floors[p1] - assigned_floors[p2]) > 1)
);

solve satisfy;

