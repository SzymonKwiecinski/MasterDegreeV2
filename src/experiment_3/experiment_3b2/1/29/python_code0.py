import pulp
import json

# Data as provided
data = json.loads("{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}")

# Extract data
num_obs = data['NumObs']
Y = data['Y']
X = data['X']

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Max_Deviation", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable("a", lowBound=None)  # Intercept
b = pulp.LpVariable("b", lowBound=None)  # Slope
Delta = pulp.LpVariable("Delta", lowBound=0)  # Maximum deviation

# Objective function
problem += Delta, "Objective"

# Constraints
for k in range(num_obs):
    problem += Y[k] - (b * X[k] + a) <= Delta, f"Upper_Deviation_Constraint_{k+1}"
    problem += (b * X[k] + a) - Y[k] <= Delta, f"Lower_Deviation_Constraint_{k+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')