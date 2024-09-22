import pulp
import json

# Input data in JSON format
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

# Create the problem
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMaximize)

# Number of ad types
A = len(data['young_clicks'])

# Decision variables
x = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=[max_click / 1000 for max_click in data['max_clicks']], cat='Continuous')

# Objective function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Goal_Young_Clicks"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Goal_Old_Clicks"
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Goal_Unique_Young_Clicks"
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Goal_Unique_Old_Clicks"
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)) <= data['budget'], "Budget_Constraint"

# Solve the problem
problem.solve()

# Output results
total_unique_clicks = pulp.value(problem.objective)
clicks = [pulp.value(x[a]) for a in range(A)]

output = {
    "clicks": clicks,
    "total_unique_clicks": total_unique_clicks
}

print(f'Output: {output}')
print(f' (Objective Value): <OBJ>{total_unique_clicks}</OBJ>')