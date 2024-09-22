import pulp

# Data from the problem
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

num_obs = data['NumObs']
Y = data['Y']
X = data['X']

# Problem
problem = pulp.LpProblem("BestFitLine", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable('Intercept', lowBound=None, upBound=None, cat=pulp.LpContinuous)
b = pulp.LpVariable('Slope', lowBound=None, upBound=None, cat=pulp.LpContinuous)
d = pulp.LpVariable('MaxDeviation', lowBound=0, cat=pulp.LpContinuous)

# Objective function
problem += d

# Constraints
for k in range(num_obs):
    problem += Y[k] - (a + b * X[k]) <= d
    problem += (a + b * X[k]) - Y[k] <= d

# Solving the problem
problem.solve()

# Output
output = {
    "intercept": pulp.value(a),
    "slope": pulp.value(b)
}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')