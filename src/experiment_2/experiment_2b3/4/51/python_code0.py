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

A = len(data['young_clicks'])

# Problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision Variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

# Objective Function
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
# Budget constraint
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A)) <= data['budget'], "BudgetConstraint"

# Goal constraints for young and old clicks
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young'], "YoungClicksGoal"
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old'], "OldClicksGoal"

# Goal constraints for unique young and old clicks
problem += pulp.lpSum(data['young_clicks'][a] * data['unique_clicks'][a] / 100 * clicks[a] for a in range(A)) >= data['goal_unique_young'], "UniqueYoungClicksGoal"
problem += pulp.lpSum(data['old_clicks'][a] * data['unique_clicks'][a] / 100 * clicks[a] for a in range(A)) >= data['goal_unique_old'], "UniqueOldClicksGoal"

# Solve the problem
problem.solve()

# Output
clicks_result = [pulp.value(clicks[a]) for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

output = {
    "clicks": clicks_result,
    "total_unique_clicks": total_unique_clicks
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')