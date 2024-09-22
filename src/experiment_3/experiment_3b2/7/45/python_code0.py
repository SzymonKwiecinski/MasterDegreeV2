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
    'unique_clicks': [40, 75, 90]
}

# Define the problem
problem = pulp.LpProblem("Advertising_Campaign", pulp.LpMinimize)

# Decision Variables
A = len(data['costs'])
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A)), "Total_Cost"

# Constraints
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young'], "Young_Audience_Clicks"
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old'], "Old_Audience_Clicks"
problem += pulp.lpSum(data['unique_clicks'][a] * data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_young'], "Unique_Young_Clicks"
problem += pulp.lpSum(data['unique_clicks'][a] * data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_old'], "Unique_Old_Clicks"
for a in range(A):
    problem += clicks[a] <= data['max_clicks'][a], f"Max_Clicks_{a}"

# Solve the problem
problem.solve()

# Output the results
for a in range(A):
    print(f'Clicks for ad type {a + 1}: {clicks[a].varValue} (in thousands)')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')