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
A = len(data['young_clicks'])
problem = pulp.LpProblem("Online_Advertising_Campaign", pulp.LpMinimize)

# Decision variables
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=None)

# Objective function
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A)), "Total_Cost"

# Constraints
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young'], "Goal_Young_Clicks"
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old'], "Goal_Old_Clicks"
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_young'], "Goal_Unique_Young_Clicks"
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_old'], "Goal_Unique_Old_Clicks"

for a in range(A):
    problem += clicks[a] <= data['max_clicks'][a], f"Max_Clicks_{a}"

# Solve the problem
problem.solve()

# Print results
clicks_values = [clicks[a].varValue for a in range(A)]
total_cost = pulp.value(problem.objective)

print(f'Clicks: {clicks_values}')
print(f'Total Cost: <OBJ>{total_cost}</OBJ>')