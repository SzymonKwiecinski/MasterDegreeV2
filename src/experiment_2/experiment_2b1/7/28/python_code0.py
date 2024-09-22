import pulp
import json

# Input data
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Create the LP problem
problem = pulp.LpProblem("Least_Absolute_Deviation_Regression", pulp.LpMinimize)

# Variables
a = pulp.LpVariable("a", lowBound=None)  # intercept
b = pulp.LpVariable("b", lowBound=None)  # slope
d = pulp.LpVariable.dicts("d", range(data['K']), lowBound=0)  # deviations

# Objective function: Minimize the sum of deviations
problem += pulp.lpSum(d[k] for k in range(data['K'])), "Minimize_Absolute_Deviation"

# Constraints: y_k = bx_k + a + d_k (for each observed point)
for k in range(data['K']):
    problem += data['Y'][k] - (b * data['X'][k] + a) <= d[k]
    problem += -(data['Y'][k] - (b * data['X'][k] + a)) <= d[k]

# Solve the problem
problem.solve()

# Extract the results
intercept = a.varValue
slope = b.varValue

# Output result
output = {
    "intercept": intercept,
    "slope": slope
}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')