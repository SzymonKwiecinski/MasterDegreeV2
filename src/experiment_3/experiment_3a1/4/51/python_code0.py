import pulp

# Data from provided input
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
problem = pulp.LpProblem("CustomTeesAdvertising", pulp.LpMaximize)

# Decision Variables
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A))

# Constraints
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young']
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old']
problem += pulp.lpSum(clicks[a] for a in range(A)) <= data['budget'] / 1000  # converting budget to thousands
for a in range(A):
    problem += clicks[a] <= data['max_clicks'][a]

# Solve the problem
problem.solve()

# Output results
clicks_result = [clicks[a].varValue for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)
print(f'Clicks Purchased: {clicks_result}')
print(f'Total Unique Clicks: {total_unique_clicks}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')