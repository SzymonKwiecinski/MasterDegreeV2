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

# Initialize the Linear Program
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Number of ad types
A = len(data['young_clicks'])

# Decision Variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

# Objective function: Maximize total unique clicks
problem += pulp.lpSum([clicks[a] * data['unique_clicks'][a] for a in range(A)])

# Constraints
# Budget constraint
problem += pulp.lpSum([clicks[a] * data['costs'][a] for a in range(A)]) <= data['budget']

# Young clicks goal constraint
problem += pulp.lpSum([clicks[a] * data['young_clicks'][a] for a in range(A)]) >= data['goal_young']

# Old clicks goal constraint
problem += pulp.lpSum([clicks[a] * data['old_clicks'][a] for a in range(A)]) >= data['goal_old']

# Unique young clicks goal constraint
problem += pulp.lpSum([clicks[a] * data['young_clicks'][a] * data['unique_clicks'][a] / 100 for a in range(A)]) >= data['goal_unique_young']

# Unique old clicks goal constraint
problem += pulp.lpSum([clicks[a] * data['old_clicks'][a] * data['unique_clicks'][a] / 100 for a in range(A)]) >= data['goal_unique_old']

# Solve the problem
problem.solve()

# Prepare the output
clicks_purchased = [pulp.value(clicks[a]) for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

output = {
    "clicks": clicks_purchased,
    "total_unique_clicks": total_unique_clicks
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')