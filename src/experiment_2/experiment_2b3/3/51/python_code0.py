import pulp

# Load data
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

# Decision Variables
A = len(data['young_clicks'])
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

# Objective
problem += pulp.lpSum([clicks[a] * data['unique_clicks'][a] for a in range(A)])

# Constraints
# Budget Constraint
problem += pulp.lpSum([clicks[a] * data['costs'][a] for a in range(A)]) <= data['budget']

# Age group click constraints
problem += pulp.lpSum([clicks[a] * data['young_clicks'][a] for a in range(A)]) >= data['goal_young']
problem += pulp.lpSum([clicks[a] * data['old_clicks'][a] for a in range(A)]) >= data['goal_old']

# Unique clicks constraints
problem += pulp.lpSum([clicks[a] * data['young_clicks'][a] * data['unique_clicks'][a] / 100 for a in range(A)]) >= data['goal_unique_young']
problem += pulp.lpSum([clicks[a] * data['old_clicks'][a] * data['unique_clicks'][a] / 100 for a in range(A)]) >= data['goal_unique_old']

# Solve the problem
problem.solve()

# Extract results
output = {
    "clicks": [pulp.value(clicks[a]) for a in range(A)],
    "total_unique_clicks": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')