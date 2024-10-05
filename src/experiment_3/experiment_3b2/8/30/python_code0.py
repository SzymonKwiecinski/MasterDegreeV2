import pulp
import json

# Data from the provided JSON
data_json = '{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'
data = json.loads(data_json)

# Extracting x and y values
x_values = data['x']
y_values = data['y']
K = len(x_values)

# Create the problem variable
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Create decision variables
a = pulp.LpVariable("a", lowBound=None)
b = pulp.LpVariable("b", lowBound=None)
c = pulp.LpVariable("c", lowBound=None)
e_k_plus = [pulp.LpVariable(f"e_{k}_plus", lowBound=0) for k in range(K)]
e_k_minus = [pulp.LpVariable(f"e_{k}_minus", lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum(e_k_plus[k] + e_k_minus[k] for k in range(K))

# Constraints
for k in range(K):
    problem += y_values[k] == c * x_values[k]**2 + b * x_values[k] + a + e_k_plus[k] - e_k_minus[k]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')