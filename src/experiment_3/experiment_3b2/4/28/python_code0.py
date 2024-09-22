import pulp
import json

# Data input
data_json = """{'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}"""
data = json.loads(data_json.replace("'", "\""))

K = data['K']
Y = data['Y']
X = data['X']

# Create the problem
problem = pulp.LpProblem("Minimize_Absolute_Deviation", pulp.LpMinimize)

# Variables
b = pulp.LpVariable("b", lowBound=None)
a = pulp.LpVariable("a", lowBound=None)
z_plus = [pulp.LpVariable(f"z_plus_{k}", lowBound=0) for k in range(K)]
z_minus = [pulp.LpVariable(f"z_minus_{k}", lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum(z_plus[k] + z_minus[k] for k in range(K)), "Total_Absolute_Deviation"

# Constraints
for k in range(K):
    problem += Y[k] - (b * X[k] + a) == z_plus[k] - z_minus[k], f"Deviation_Constraint_{k}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')