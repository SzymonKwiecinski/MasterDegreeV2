import pulp
import json

# Sample data
data_json = """{
    "y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
    "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}"""
data = json.loads(data_json)

# Create the linear programming problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Variables
a = pulp.LpVariable("a", cat="Continuous")
b = pulp.LpVariable("b", cat="Continuous")
c = pulp.LpVariable("c", cat="Continuous")

# Deviations
K = len(data['y'])
u = [pulp.LpVariable(f"u_{k}", lowBound=0) for k in range(K)]
v = [pulp.LpVariable(f"v_{k}", lowBound=0) for k in range(K)]

# Objective function: minimize the sum of u_k and v_k
problem += pulp.lpSum(u[k] + v[k] for k in range(K))

# Adding constraints
for k in range(K):
    x_k = data['x'][k]
    y_k = data['y'][k]
    problem += y_k - (c * x_k**2 + b * x_k + a) <= u[k]
    problem += -(y_k - (c * x_k**2 + b * x_k + a)) <= v[k]

# Solve the problem
problem.solve()

# Print the objective value and the coefficients
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(json.dumps({
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}))