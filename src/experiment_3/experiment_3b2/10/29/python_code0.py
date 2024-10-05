import pulp
import json

# Input data
data = json.loads('{"NumObs": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

# Extract data
X = data['X']
Y = data['Y']
K = data['NumObs']

# Create the problem
problem = pulp.LpProblem("Minimize_Max_Deviation", pulp.LpMinimize)

# Define decision variables
a = pulp.LpVariable("a", lowBound=None)  # Intercept
b = pulp.LpVariable("b", lowBound=None)  # Slope
D = pulp.LpVariable("D", lowBound=0)     # Maximum deviation

# Objective function
problem += D, "Objective"

# Constraints
for k in range(K):
    problem += Y[k] - (b * X[k] + a) <= D, f"Upper_Bound_Constraint_{k}"
    problem += (b * X[k] + a) - Y[k] <= D, f"Lower_Bound_Constraint_{k}"

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')