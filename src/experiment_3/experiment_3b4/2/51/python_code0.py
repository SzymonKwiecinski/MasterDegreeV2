import pulp

# Data
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
A = len(data['unique_clicks'])

# Initialize the problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, upBound=data['max_clicks'][i]) for i in range(A)]

# Objective function
problem += pulp.lpSum(data['unique_clicks'][i] * x[i] for i in range(A))

# Constraints
# Budget constraint
problem += pulp.lpSum(data['costs'][i] * x[i] for i in range(A)) <= data['budget']

# Age-specific click constraints
problem += pulp.lpSum(data['young_clicks'][i] * x[i] for i in range(A)) >= data['goal_young']
problem += pulp.lpSum(data['old_clicks'][i] * x[i] for i in range(A)) >= data['goal_old']

# Unique click constraints for each age group
problem += pulp.lpSum(data['young_clicks'][i] * data['unique_clicks'][i] * x[i] for i in range(A)) >= data['goal_unique_young']
problem += pulp.lpSum(data['old_clicks'][i] * data['unique_clicks'][i] * x[i] for i in range(A)) >= data['goal_unique_old']

# Solve the problem
problem.solve()

# Print the optimal solution and objective value
for i in range(A):
    print(f'x_{i + 1} = {pulp.value(x[i])}')
    
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')