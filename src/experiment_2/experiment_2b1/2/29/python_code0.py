import pulp
import json

# Data input
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Model
problem = pulp.LpProblem("Minimize_Max_Deviation", pulp.LpMinimize)

# Variables
a = pulp.LpVariable("a", lowBound=None)  # Intercept
b = pulp.LpVariable("b", lowBound=None)  # Slope
deviations = [pulp.LpVariable(f"deviation_{k}", lowBound=0) for k in range(data['NumObs'])]

# Objective function: minimize the maximum deviation
problem += pulp.lpSum(deviations)

# Constraints
for k in range(data['NumObs']):
    problem += deviations[k] >= data['Y'][k] - (b * data['X'][k] + a)
    problem += deviations[k] >= -(data['Y'][k] - (b * data['X'][k] + a))

# Solve the problem
problem.solve()

# Retrieve results
intercept = a.varValue
slope = b.varValue

# Output
output = {
    "intercept": intercept,
    "slope": slope
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')