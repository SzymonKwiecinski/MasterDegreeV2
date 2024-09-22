import pulp
import json

# Input data
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Initialize the problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

# Variables for slope (b) and intercept (a)
b = pulp.LpVariable("slope", lowBound=None)
a = pulp.LpVariable("intercept", lowBound=None)

# Deviation variables
deviations = [pulp.LpVariable(f"deviation_{k}", lowBound=0) for k in range(data['NumObs'])]

# Objective function: minimize the maximum deviation
problem += pulp.lpSum(deviations), "Objective"

# Constraints for each observation
for k in range(data['NumObs']):
    problem += deviations[k] >= data['Y'][k] - (b * data['X'][k] + a), f"Upper_deviation_{k}"
    problem += deviations[k] >= -(data['Y'][k] - (b * data['X'][k] + a)), f"Lower_deviation_{k}"

# Solve the problem
problem.solve()

# Extracting results
intercept = a.varValue
slope = b.varValue

# Output result in required format
result = {
    "intercept": intercept,
    "slope": slope
}

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')