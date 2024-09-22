import pulp
import json

# Input data
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Create a linear programming problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

# Define variables
a = pulp.LpVariable("intercept", lowBound=None)
b = pulp.LpVariable("slope", lowBound=None)
deviations = [pulp.LpVariable(f"deviation_{k}", lowBound=0) for k in range(data['NumObs'])]

# Objective function: Minimize the maximum deviation
problem += pulp.lpSum(deviations)

# Constraints for each observed value
for k in range(data['NumObs']):
    problem += deviations[k] >= data['Y'][k] - (b * data['X'][k] + a)
    problem += deviations[k] >= (b * data['X'][k] + a) - data['Y'][k]

# Solve the problem
problem.solve()

# Get results
intercept = a.varValue
slope = b.varValue

# Output results
output = {
    "intercept": intercept,
    "slope": slope
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')