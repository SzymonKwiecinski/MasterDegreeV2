import pulp

# Data from the input
data = {
    'K': 19, 
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

# Create the Linear Program
problem = pulp.LpProblem("Absolute_Deviation_Minimization", pulp.LpMinimize)

# Decision variables
a = pulp.LpVariable("a", lowBound=None)  # intercept
b = pulp.LpVariable("b", lowBound=None)  # slope
e = pulp.LpVariable.dicts("e", range(data['K']), lowBound=0)  # error variables

# Objective function
problem += pulp.lpSum(e[k] for k in range(data['K'])), "Total_Absolute_Deviation"

# Constraints
for k in range(data['K']):
    problem += data['Y'][k] - (b * data['X'][k] + a) <= e[k], f"Error_Positive_{k}"
    problem += -(data['Y'][k] - (b * data['X'][k] + a)) <= e[k], f"Error_Negative_{k}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')