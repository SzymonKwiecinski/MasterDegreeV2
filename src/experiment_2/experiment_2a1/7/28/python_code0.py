import pulp
import json

# Input data in JSON format
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Create the linear programming problem
problem = pulp.LpProblem("Least_Absolute_Deviation", pulp.LpMinimize)

# Variables
intercept = pulp.LpVariable("Intercept", cat='Continuous')
slope = pulp.LpVariable("Slope", cat='Continuous')
deviations = [pulp.LpVariable(f"deviation_{k}", cat='Continuous') for k in range(data['K'])]

# Objective function: Minimize the sum of deviations
problem += pulp.lpSum(deviations), "Total_Deviation"

# Constraints for each data point
for k in range(data['K']):
    problem += deviations[k] >= data['Y'][k] - (slope * data['X'][k] + intercept), f"Upper_Bound_{k}"
    problem += deviations[k] >= -(data['Y'][k] - (slope * data['X'][k] + intercept)), f"Lower_Bound_{k}"

# Solve the problem
problem.solve()

# Output the results
intercept_value = pulp.value(intercept)
slope_value = pulp.value(slope)

result = {
    "intercept": intercept_value,
    "slope": slope_value
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')