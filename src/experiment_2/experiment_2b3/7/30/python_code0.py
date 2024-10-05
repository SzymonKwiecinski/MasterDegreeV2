import pulp

# Data Input
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

y_values = data["y"]
x_values = data["x"]
K = len(y_values)

# Problem
problem = pulp.LpProblem("Quadratic_Fit", pulp.LpMinimize)

# Decision Variables
c = pulp.LpVariable("quadratic_term", lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable("linear_term", lowBound=None, upBound=None, cat='Continuous')
a = pulp.LpVariable("constant_term", lowBound=None, upBound=None, cat='Continuous')
deviations = [pulp.LpVariable(f"deviation_{k}", lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function: Minimize the sum of absolute deviations
objective = pulp.lpSum(deviations)
problem += objective

# Constraints: Control absolute deviation |y_k - (c * x_k^2 + b * x_k + a)|
for k, (y_k, x_k) in enumerate(zip(y_values, x_values)):
    predicted_y = c * (x_k**2) + b * x_k + a
    problem += deviations[k] >= y_k - predicted_y
    problem += deviations[k] >= predicted_y - y_k

# Solve Problem
problem.solve()

# Extract Solution
result = {
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')