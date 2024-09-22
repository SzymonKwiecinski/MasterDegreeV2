import json
import pulp

# Input data
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

# Problem Setup
A = len(data['young_clicks'])
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision Variables
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=[max_click / 1000 for max_click in data['max_clicks']], cat='Continuous')

# Objective Function
total_unique_clicks = pulp.lpSum([clicks[a] * (data['unique_clicks'][a] / 1000) for a in range(A)])
problem += total_unique_clicks, "Total_Unique_Clicks"

# Constraints
problem += pulp.lpSum([clicks[a] * (data['costs'][a] / 1000) for a in range(A)]) <= data['budget'], "Budget_Constraint"
problem += pulp.lpSum([clicks[a] * (data['young_clicks'][a] / 1000) for a in range(A)]) >= data['goal_young'], "Young_Clicks_Constraint"
problem += pulp.lpSum([clicks[a] * (data['old_clicks'][a] / 1000) for a in range(A)]) >= data['goal_old'], "Old_Clicks_Constraint"
problem += pulp.lpSum([clicks[a] * (data['unique_clicks'][a] / 1000) for a in range(A)]) >= data['goal_unique_young'], "Unique_Young_Clicks_Constraint"
problem += pulp.lpSum([clicks[a] * (data['unique_clicks'][a] / 1000) for a in range(A)]) >= data['goal_unique_old'], "Unique_Old_Clicks_Constraint"

# Solve the problem
problem.solve()

# Prepare the output
clicks_result = [pulp.value(clicks[a]) for a in range(A)]
total_unique_clicks_value = pulp.value(total_unique_clicks)

output = {
    "clicks": clicks_result,
    "total_unique_clicks": total_unique_clicks_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')