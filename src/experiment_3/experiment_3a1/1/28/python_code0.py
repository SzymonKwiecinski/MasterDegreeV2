import pulp
import json

# Data input
data_json = '{"K": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'
data = json.loads(data_json)

K = data['K']
Y = data['Y']
X = data['X']

# Create a linear programming problem
problem = pulp.LpProblem("Least_Squares_Fit", pulp.LpMinimize)

# Decision Variables
b = pulp.LpVariable("b", lowBound=None)  # slope
a = pulp.LpVariable("a", lowBound=None)  # intercept
e = [pulp.LpVariable(f"e_{k}", lowBound=0) for k in range(K)]  # auxiliary variables for deviations

# Objective Function
problem += pulp.lpSum(e[k] for k in range(K)), "Minimize_Deviation"

# Constraints
for k in range(K):
    problem += e[k] >= Y[k] - (b * X[k] + a), f"Upper_Bound_{k}"
    problem += e[k] >= -(Y[k] - (b * X[k] + a)), f"Lower_Bound_{k}"

# Solve the problem
problem.solve()

# Print the outputs
print(f'Slope (b): {b.varValue}')
print(f'Intercept (a): {a.varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')