import pulp

# Data input
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

# Problem: Maximize total unique clicks
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision variables: number of clicks purchased (in thousands) for each ad type
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

# Objective function: maximize total unique clicks
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
# Budget constraint
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A)) <= data['budget'], "Budget_Constraint"

# Age group goals constraints
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] / 100 for a in range(A)) >= data['goal_young'], "Young_Clicks_Goal"
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] / 100 for a in range(A)) >= data['goal_old'], "Old_Clicks_Goal"

# Unique click goals constraints
problem += pulp.lpSum(data['young_clicks'][a] * data['unique_clicks'][a] * clicks[a] / 10000 for a in range(A)) >= data['goal_unique_young'], "Unique_Young_Clicks_Goal"
problem += pulp.lpSum(data['old_clicks'][a] * data['unique_clicks'][a] * clicks[a] / 10000 for a in range(A)) >= data['goal_unique_old'], "Unique_Old_Clicks_Goal"

# Solve the problem
problem.solve()

# Prepare the output
clicks_value = [pulp.value(clicks[a]) for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

# Output format
output = {
    "clicks": clicks_value,
    "total_unique_clicks": total_unique_clicks
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')