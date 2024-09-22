import pulp
import numpy as np

# Data input
data = {
    'NumObs': 19, 
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Problem definition
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

# Variables
a = pulp.LpVariable("a", lowBound=None)  # Intercept
b = pulp.LpVariable("b", lowBound=None)  # Slope
M = pulp.LpVariable("M", lowBound=0)     # Maximum deviation
e_plus = [pulp.LpVariable(f"e_plus_{k}", lowBound=0) for k in range(data['NumObs'])]
e_minus = [pulp.LpVariable(f"e_minus_{k}", lowBound=0) for k in range(data['NumObs'])]

# Objective function
problem += M, "Minimize_Max_Deviation"

# Constraints
for k in range(data['NumObs']):
    problem += e_plus[k] >= data['Y'][k] - (b * data['X'][k] + a), f"Pos_Deviation_{k}"
    problem += e_minus[k] >= -(data['Y'][k] - (b * data['X'][k] + a)), f"Neg_Deviation_{k}"
    problem += e_plus[k] <= M, f"Max_Pos_Deviation_{k}"
    problem += e_minus[k] <= M, f"Max_Neg_Deviation_{k}"

# Solve the problem
problem.solve()

# Output results
intercept = a.varValue
slope = b.varValue
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print({'intercept': intercept, 'slope': slope})