import pulp
import json

# Input data
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

K = data['NumObs']
Y = data['Y']
X = data['X']

# Create the problem
problem = pulp.LpProblem("Line_Fitting", pulp.LpMinimize)

# Variables: slope (b) and intercept (a)
b = pulp.LpVariable("slope", lowBound=None)
a = pulp.LpVariable("intercept", lowBound=None)

# Deviation variables
deviations = [pulp.LpVariable(f"deviation_{k}", lowBound=0) for k in range(K)]

# Objective function: minimize the maximum deviation
problem += pulp.lpSum(deviations)

# Constraints: |y_k - (b * x_k + a)| <= deviations[k]
for k in range(K):
    problem += (Y[k] - (b * X[k] + a) <= deviations[k])
    problem += ((b * X[k] + a) - Y[k] <= deviations[k])

# Solve the problem
problem.solve()

# Output results
intercept = a.varValue
slope = b.varValue
print(json.dumps({"intercept": intercept, "slope": slope}))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')