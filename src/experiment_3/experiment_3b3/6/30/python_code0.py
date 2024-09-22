import pulp

# Data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

x = data['x']
y = data['y']
K = len(x)

# Problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

# Variables
c = pulp.LpVariable('c', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
a = pulp.LpVariable('a', cat='Continuous')
d = [pulp.LpVariable(f'd_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective
problem += pulp.lpSum(d), "Sum of Absolute Deviations"

# Constraints
for k in range(K):
    x_k = x[k]
    y_k = y[k]
    problem += d[k] >= y_k - (c * x_k**2 + b * x_k + a), f"Deviation_Pos_{k}"
    problem += d[k] >= -(y_k - (c * x_k**2 + b * x_k + a)), f"Deviation_Neg_{k}"

# Solve
problem.solve()

# Results
print({
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
})

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')