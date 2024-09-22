import pulp
import json

# Input data
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}
Y = data['Y']
X = data['X']

# Define the problem
problem = pulp.LpProblem("Minimize_Maximum_Deviation", pulp.LpMinimize)

# Define variables
a = pulp.LpVariable("intercept", cat='Continuous')
b = pulp.LpVariable("slope", cat='Continuous')
deviations = [pulp.LpVariable(f"deviation_{k}", cat='Continuous') for k in range(len(Y))]

# Objective function: Minimize the maximum deviation
problem += pulp.lpSum(deviations)  # We will minimize the max deviation

# Constraints for each observation
for k in range(len(Y)):
    problem += Y[k] - (b * X[k] + a) <= deviations[k]
    problem += (b * X[k] + a) - Y[k] <= deviations[k]

# Solve the problem
problem.solve()

# Extract the results
intercept = a.varValue
slope = b.varValue

# Output
output = {
    "intercept": intercept,
    "slope": slope
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')