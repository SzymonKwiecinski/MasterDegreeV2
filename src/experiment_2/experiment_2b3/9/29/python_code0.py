import pulp

# Data from the problem
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Initialize the LP problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

# Create variables for the intercept and slope
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
deviation = pulp.LpVariable('deviation', lowBound=0, cat='Continuous')

# Objective function: Minimize the maximum deviation
problem += deviation, "Objective: Minimize Maximum Deviation"

# Constraints: |y_k - (bx_k + a)| <= deviation for all k
for i in range(data['NumObs']):
    x_k = data['X'][i]
    y_k = data['Y'][i]
    problem += y_k - (b * x_k + a) <= deviation, f"Deviation_Upper_{i}"
    problem += (b * x_k + a) - y_k <= deviation, f"Deviation_Lower_{i}"

# Solve the problem
problem.solve()

# Capture the results
intercept = pulp.value(a)
slope = pulp.value(b)

# Output the results
output = {"intercept": intercept, "slope": slope}
print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')