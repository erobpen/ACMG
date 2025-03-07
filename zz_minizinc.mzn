include "alldifferent.mzn";


int: num_floors = 5;
set of int: Floors = 1..num_floors;
set of string: Individuals = {"Baker", "Cooper", "Fletcher", "Miller", "Smith"};

array[Individuals] of var Floors: floor_assignment;

% Each person lives on a different floor
constraint forall(i, j in Individuals where i != j) (
    floor_assignment[i] != floor_assignment[j]
);

% Adjacency conditions (example conditions can be added based on the problem specifics)
% This is just a placeholder for adjacency constraints
% constraint abs(floor_assignment["Baker"] - floor_assignment["Cooper"]) == 1; 

% Relative floor position conditions (example conditions can be added based on the problem specifics)
% constraint floor_assignment["Fletcher"] < floor_assignment["Miller"];

solve satisfy;

