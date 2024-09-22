import pulp

# Data
data = {
    'NumObs': 19, 
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Constants and variables
K = data['NumObs']
Y = data['Y']
X = data['X']

# Define LP Problem
problem = pulp.LpProblem("Linear_Regression_Minimize_Maximum_Deviation", pulp.LpMinimize)

# Define Variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
D = pulp.LpVariable('D', lowBound=0, cat='Continuous')
d = pulp.LpVariable.dicts('d', range(K), lowBound=0, cat='Continuous')

# Objective Function
problem += D, "Minimize maximum deviation D"

# Constraints
for k in range(K):
    # Constraint: d_k >= y_k - (bx_k + a)
    problem += d[k] >= Y[k] - (b * X[k] + a)
    
    # Constraint: d_k >= (bx_k + a) - y_k
    problem += d[k] >= (b * X[k] + a) - Y[k]
    
    # Constraint: d_k <= D
    problem += d[k] <= D

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')