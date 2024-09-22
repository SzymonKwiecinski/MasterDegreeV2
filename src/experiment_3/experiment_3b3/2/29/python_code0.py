import pulp

# Parse the data from the JSON format
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Create a linear programming problem
problem = pulp.LpProblem("Line_Fitting_Problem", pulp.LpMinimize)

# Create the variables: intercept (a), slope (b), and maximum deviation (M)
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
M = pulp.LpVariable('M', lowBound=0, cat='Continuous')

# Objective function: Minimize the maximum deviation (M)
problem += M, "Minimize_Max_Deviation"

# Add constraint for each observation
NumObs = data['NumObs']
Y = data['Y']
X = data['X']

for k in range(NumObs):
    problem += Y[k] - (b * X[k] + a) <= M, f"Upper_Deviation_Constraint_{k}"
    problem += -(Y[k] - (b * X[k] + a)) <= M, f"Lower_Deviation_Constraint_{k}"

# Solve the problem
problem.solve()

# Retrieve the results
intercept = pulp.value(a)
slope = pulp.value(b)

# Print the results
print(f'Intercept (a): {intercept}')
print(f'Slope (b): {slope}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')