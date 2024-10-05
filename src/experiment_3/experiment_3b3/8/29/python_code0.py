import pulp

# Defining the data
data = {'NumObs': 19, 
        'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
       }

# Number of observations
K = data['NumObs']
Y = data['Y']
X = data['X']

# Create a LP Minimization problem
problem = pulp.LpProblem("Linear_Regression_Min_Max_Deviation", pulp.LpMinimize)

# Define Variables
a = pulp.LpVariable('a', lowBound=None, cat='Continuous')  # Intercept
b = pulp.LpVariable('b', lowBound=None, cat='Continuous')  # Slope
D = pulp.LpVariable('D', lowBound=0, cat='Continuous')     # Objective variable
d = [pulp.LpVariable(f'd_{k}', lowBound=0, cat='Continuous') for k in range(K)]  # Deviation variables

# Objective function
problem += D, "Minimize_Max_Deviation"

# Constraints
for k in range(K):
    problem += d[k] >= (Y[k] - (b * X[k] + a)), f"Deviation_Positive_{k}"
    problem += d[k] >= -(Y[k] - (b * X[k] + a)), f"Deviation_Negative_{k}"
    problem += D >= d[k], f"Max_Deviation_{k}"

# Solve the problem
problem.solve()

# Output the results
print(f'Intercept (a): {pulp.value(a)}')
print(f'Slope (b): {pulp.value(b)}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')