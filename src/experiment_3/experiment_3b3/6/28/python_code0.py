import pulp

# Data
data = {'K': 19, 
        'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

K = data['K']
Y = data['Y']
X = data['X']

# Problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

# Decision Variables
a = pulp.LpVariable('Intercept', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('Slope', lowBound=None, upBound=None, cat='Continuous')
e = [pulp.LpVariable(f'e_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(e), "Minimize_Sum_of_Absolute_Deviations"

# Constraints
for k in range(K):
    problem += e[k] >= Y[k] - (b * X[k] + a), f"Constraint_positive_deviation_{k}"
    problem += e[k] >= -(Y[k] - (b * X[k] + a)), f"Constraint_negative_deviation_{k}"

# Solve the problem
problem.solve()

# Output
intercept = pulp.value(a)
slope = pulp.value(b)

print(f"Intercept: {intercept}, Slope: {slope} (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")