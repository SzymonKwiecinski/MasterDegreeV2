import pulp

# Define the data
data = {
    'goal_young': 500,
    'goal_old': 600,
    'goal_unique_young': 250,
    'goal_unique_old': 300,
    'young_clicks': [40, 30, 70],
    'old_clicks': [60, 70, 30],
    'costs': [75, 100, 120],
    'max_clicks': [600, 300, 300],
    'unique_clicks': [40, 75, 90],
    'budget': 105000
}

# Number of ad types
A = len(data['young_clicks'])

# Define the problem
problem = pulp.LpProblem("Online_Advertising_Campaign", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(A)]

# Objective function
problem += pulp.lpSum(data['unique_clicks'][i] * x[i] for i in range(A))

# Constraints
# 1. Clicks for young visitors
problem += pulp.lpSum(data['young_clicks'][i] * x[i] for i in range(A)) >= data['goal_young']

# 2. Clicks for old visitors
problem += pulp.lpSum(data['old_clicks'][i] * x[i] for i in range(A)) >= data['goal_old']

# 3. Unique clicks for young visitors
problem += pulp.lpSum(data['unique_clicks'][i] * x[i] for i in range(A)) >= data['goal_unique_young']

# 4. Unique clicks for old visitors
problem += pulp.lpSum(data['unique_clicks'][i] * x[i] for i in range(A)) >= data['goal_unique_old']

# 5. Budget constraint
problem += pulp.lpSum(data['costs'][i] * x[i] for i in range(A)) <= data['budget']

# 6. Maximum clicks constraints
for i in range(A):
    problem += x[i] <= data['max_clicks'][i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print the solution
clicks = [pulp.value(x[i]) for i in range(A)]
print("Optimal Clicks (in thousands):", clicks)