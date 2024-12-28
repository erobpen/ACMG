include "globals.mzn";

% Number of furniture pieces
int: num_furniture;

% Grid dimensions (n x n)
int: n;

% Compatibility matrix
array[1..num_furniture, 1..num_furniture] of int: compatibility;

% Variables: grid[i, j] is the furniture piece at position (i, j), or 0 if empty
array[1..n, 1..n] of var 0..num_furniture: grid;

% Constraint 1: No two pieces can occupy the same position
constraint
  forall(f1 in 1..num_furniture, f2 in f1+1..num_furniture) (
    (exists(i, j in 1..n)(grid[i, j] = f1) /\ exists(i, j in 1..n)(grid[i, j] = f2)) ->
    compatibility[f1, f2] != 0
  );

% Constraint 2: Adjacency rules based on the compatibility matrix
constraint
  forall(i in 1..n, j in 1..n, f1 in 1..num_furniture, f2 in f1+1..num_furniture where grid[i, j] = f1 /\ compatibility[f1, f2] != 1)(
    (j > 1 /\ grid[i, j-1] = f2) \/  % Left
    (j < n /\ grid[i, j+1] = f2) \/  % Right
    (i > 1 /\ grid[i-1, j] = f2) \/  % Up
    (i < n /\ grid[i+1, j] = f2)     % Down
  );

% Solve the problem by filling the grid
solve satisfy;

% Output the grid
