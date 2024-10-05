import pulp

# Data
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Parameters
K = data['NumObs']
Y = data['Y']
X = data['X']

# Problem
problem = pulp.LpProblem('LinearRegressionMinMaxDeviation', pulp.LpMinimize)

# Variables
a = pulp.LpVariable('Intercept', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('Slope', lowBound=None, upBound=None, cat='Continuous')
D = pulp.LpVariable('MaxDeviation', lowBound=0, cat='Continuous')
d = [pulp.LpVariable(f'Deviation_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective
problem += D, "Minimize_Maximum_Deviation"

# Constraints
for k in range(K):
    # d_k >= y_k - (bx_k + a)
    problem += d[k] >= Y[k] - (b * X[k] + a), f"Deviation_Pos_{k}"
    # d_k >= -(y_k - (bx_k + a))
    problem += d[k] >= -(Y[k] - (b * X[k] + a)), f"Deviation_Neg_{k}"
    # d_k <= D
    problem += d[k] <= D, f"Max_Deviation_{k}"

# Solve
problem.solve()

# Output
print(f"Intercept (a): {pulp.value(a)}")
print(f"Slope (b): {pulp.value(b)}")
print(f"(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")