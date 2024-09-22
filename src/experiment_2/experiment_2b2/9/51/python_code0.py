import pulp

# Data from JSON
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

# Problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Variables
A = len(data['young_clicks'])
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, cat='Continuous') for a in range(A)]

# Objective
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A))

# Constraints
# Budget constraint
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A)) <= data['budget']

# Young clicks constraint
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young']

# Old clicks constraint
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old']

# Unique young clicks constraint
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] * (data['young_clicks'][a] / 100) for a in range(A)) >= data['goal_unique_young']

# Unique old clicks constraint
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] * (data['old_clicks'][a] / 100) for a in range(A)) >= data['goal_unique_old']

# Max clicks constraint for each ad
for a in range(A):
    problem += clicks[a] <= data['max_clicks'][a]

# Solve
problem.solve()

# Output
clicks_values = [pulp.value(clicks[a]) for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

output = {
    "clicks": clicks_values,
    "total_unique_clicks": total_unique_clicks
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')