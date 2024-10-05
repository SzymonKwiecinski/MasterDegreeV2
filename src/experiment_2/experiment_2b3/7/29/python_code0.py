import pulp

# Data
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

# Extracting X and Y
num_obs = data['NumObs']
Y = data['Y']
X = data['X']

# Problem
problem = pulp.LpProblem("Minimize_Max_Deviation", pulp.LpMinimize)

# Variables
a = pulp.LpVariable('intercept', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('slope', lowBound=None, upBound=None, cat='Continuous')
d = pulp.LpVariable('deviation', lowBound=0, cat='Continuous')

# Objective
problem += d, "Objective: Minimize max deviation"

# Constraints
for i in range(num_obs):
    y_pred = a + b * X[i]
    problem += y_pred - Y[i] <= d
    problem += Y[i] - y_pred <= d

# Solve
problem.solve()

# Results
output = {
    "intercept": pulp.value(a),
    "slope": pulp.value(b)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')