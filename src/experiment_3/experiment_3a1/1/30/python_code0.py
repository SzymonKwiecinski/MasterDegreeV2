import pulp
import json

# Given data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Set up the problem
K = len(data['y'])
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Decision variables
c = pulp.LpVariable("c", cat='Real')
b = pulp.LpVariable("b", cat='Real')
a = pulp.LpVariable("a", cat='Real')
u = [pulp.LpVariable(f'u_{k}', lowBound=0) for k in range(K)]
v = [pulp.LpVariable(f'v_{k}', lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum(u[k] + v[k] for k in range(K)), "Minimize_Total_Deviation"

# Constraints
for k in range(K):
    problem += u[k] - v[k] == data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a), f"Deviations_Constraint_{k}"

# Solve the problem
problem.solve()

# Output results
results = {
    "quadratic": c.varValue,
    "linear": b.varValue,
    "constant": a.varValue
}

print(json.dumps(results, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')