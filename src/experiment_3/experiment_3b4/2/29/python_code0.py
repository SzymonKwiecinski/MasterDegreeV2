import pulp

# Data from JSON
data = {
    'NumObs': 19, 
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Initialize the problem
problem = pulp.LpProblem("Minimize_Max_Deviation", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
d = pulp.LpVariable('d', lowBound=0, upBound=None, cat='Continuous')

# Objective function
problem += d, "Minimize maximum deviation"

# Constraints
for k in range(data['NumObs']):
    xk = data['X'][k]
    yk = data['Y'][k]
    problem += d >= yk - (b * xk + a), f"Constraint_upper_bound_{k}"
    problem += d >= (b * xk + a) - yk, f"Constraint_lower_bound_{k}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')