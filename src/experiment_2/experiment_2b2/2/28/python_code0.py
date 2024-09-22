import pulp
import json

# Data Input
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Extract the number of data points, and the lists X and Y
K = data['K']
Y = data['Y']
X = data['X']

# Define the LP problem
problem = pulp.LpProblem("Fit_Line", pulp.LpMinimize)

# Define the decision variables: slope (b), intercept (a), and deviations (d+ and d-)
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
d_plus = pulp.LpVariable.dicts('d_plus', range(K), lowBound=0, cat='Continuous')
d_minus = pulp.LpVariable.dicts('d_minus', range(K), lowBound=0, cat='Continuous')

# Objective function: Minimize the sum of deviations
problem += pulp.lpSum([d_plus[k] + d_minus[k] for k in range(K)])

# Constraints: For each data point, ensure that the deviation is correctly calculated
for k in range(K):
    problem += Y[k] - (a + b * X[k]) == d_plus[k] - d_minus[k]

# Solve the problem
problem.solve()

# Collect the results
intercept = a.varValue
slope = b.varValue

# Output results in the requested format
output = {
    "intercept": intercept,
    "slope": slope
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')