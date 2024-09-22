import pulp
import json

data = json.loads('{"K": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

K = data['K']
Y = data['Y']
X = data['X']

# Create the problem
problem = pulp.LpProblem("Minimize_Deviation", pulp.LpMinimize)

# Decision Variables
z_k_plus = pulp.LpVariable.dicts("z_plus", range(K), lowBound=0, cat='Continuous')
z_k_minus = pulp.LpVariable.dicts("z_minus", range(K), lowBound=0, cat='Continuous')
b = pulp.LpVariable("b", cat='Continuous')  # Slope
a = pulp.LpVariable("a", cat='Continuous')  # Intercept

# Objective Function
problem += pulp.lpSum(z_k_plus[k] + z_k_minus[k] for k in range(K))

# Constraints
for k in range(K):
    problem += (Y[k] - (b * X[k] + a) == z_k_plus[k] - z_k_minus[k])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')