import pulp
import json

# Data in JSON format
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Initialize the problem
problem = pulp.LpProblem("Minimize_Max_Deviation", pulp.LpMinimize)

# Variables
a = pulp.LpVariable("a", lowBound=None)  # intercept
b = pulp.LpVariable("b", lowBound=None)  # slope
z = pulp.LpVariable("z", lowBound=0)     # maximum deviation

# Constraints for each observation
for k in range(data['NumObs']):
    x_k = data['X'][k]
    y_k = data['Y'][k]
    
    # y_k - (b*x_k + a) <= z
    problem += (y_k - (b * x_k + a) <= z)
    
    # (b*x_k + a) - y_k <= z
    problem += ((b * x_k + a) - y_k <= z)

# Objective function
problem += z  # we want to minimize z

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')