import pulp
import json

# Data provided in JSON format
data = json.loads('{"NumObs": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

# Number of observations
K = data['NumObs']
Y = data['Y']
X = data['X']

# Create the linear programming problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

# Variables: slope (b), intercept (a), and the maximum deviation (D)
b = pulp.LpVariable("b", lowBound=None)  # slope
a = pulp.LpVariable("a", lowBound=None)  # intercept
D = pulp.LpVariable("D", lowBound=0)     # maximum deviation

# Objective function: minimize D
problem += D, "Minimize_Max_Deviation"

# Constraints for the model
for k in range(K):
    problem += -(b * X[k] + a - Y[k]) <= D, f"Lower_Bound_Constraint_{k}"
    problem += (b * X[k] + a - Y[k]) <= D, f"Upper_Bound_Constraint_{k}"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')