import pulp
import json

# Data
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Create LP problem
problem = pulp.LpProblem("Linear_Regression_LP", pulp.LpMinimize)

# Variables
a = pulp.LpVariable("a", lowBound=None)  # intercept
b = pulp.LpVariable("b", lowBound=None)  # slope
T = pulp.LpVariable("T", lowBound=0)     # maximum deviation

# Constraints
for k in range(data['NumObs']):
    problem += (b * data['X'][k] + a + T >= data['Y'][k], f"UpperBound_{k}")
    problem += (b * data['X'][k] + a - T <= data['Y'][k], f"LowerBound_{k}")

# Objective
problem += T

# Solve the problem
problem.solve()

# Output
output = {
    "intercept": a.varValue,
    "slope": b.varValue
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')