import pulp

# Input data
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

# Variables
a = pulp.LpVariable('Intercept', lowBound=-float('inf'), cat='Continuous')
b = pulp.LpVariable('Slope', lowBound=-float('inf'), cat='Continuous')
max_deviation = pulp.LpVariable('Max_Deviation', lowBound=0, cat='Continuous')

# Constraints
for i in range(data['NumObs']):
    y_k = data['Y'][i]
    x_k = data['X'][i]
    problem += y_k - (b*x_k + a) <= max_deviation
    problem += -y_k + (b*x_k + a) <= max_deviation

# Objective
problem += max_deviation

# Solve
try:
    problem.solve(pulp.PULP_CBC_CMD(msg=1))  # Using the default solver with output messages
except Exception as e:
    print(f"An error occurred during solving: {e}")

# Results
intercept_value = pulp.value(a)
slope_value = pulp.value(b)

output = {
    "intercept": intercept_value,
    "slope": slope_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')