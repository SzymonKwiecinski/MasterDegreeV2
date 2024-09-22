import pulp
import json

data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 
        'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 
        'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 
        'unique_clicks': [40, 75, 90], 'budget': 105000}

# Define the problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Define variables
A = len(data['young_clicks'])  # number of ad types
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a] / 1000) for a in range(A)]

# Objective function: maximize total unique clicks
total_unique_clicks = pulp.lpSum([clicks[a] * data['unique_clicks'][a] for a in range(A)])
problem += total_unique_clicks

# Constraints
problem += pulp.lpSum([clicks[a] * data['costs'][a] for a in range(A)]) <= data['budget'], "BudgetConstraint"
problem += pulp.lpSum([clicks[a] * data['young_clicks'][a] for a in range(A)]) >= data['goal_young'] / 1000, "YoungClicksGoal"
problem += pulp.lpSum([clicks[a] * data['old_clicks'][a] for a in range(A)]) >= data['goal_old'] / 1000, "OldClicksGoal"
problem += pulp.lpSum([clicks[a] * data['unique_clicks'][a] for a in range(A)]) >= data['goal_unique_young'] / 1000, "UniqueYoungClicksGoal"
problem += pulp.lpSum([clicks[a] * data['unique_clicks'][a] for a in range(A)]) >= data['goal_unique_old'] / 1000, "UniqueOldClicksGoal"

# Solve the problem
problem.solve()

# Collect results
result_clicks = [pulp.value(clicks[a]) for a in range(A)]
total_unique_clicks_value = pulp.value(total_unique_clicks)

# Output
output = {
    "clicks": result_clicks,
    "total_unique_clicks": total_unique_clicks_value
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')