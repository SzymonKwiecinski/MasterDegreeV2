import pulp
import json

# Input data
data = {'goal_young': 500, 
        'goal_old': 600, 
        'goal_unique_young': 250, 
        'goal_unique_old': 300, 
        'young_clicks': [40, 30, 70], 
        'old_clicks': [60, 70, 30], 
        'costs': [75, 100, 120], 
        'max_clicks': [600, 300, 300], 
        'unique_clicks': [40, 75, 90], 
        'budget': 105000}

# Problem setup
A = len(data['young_clicks'])
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

# Objective function: maximize total unique clicks
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)])

# Constraints
problem += pulp.lpSum([data['costs'][a] * clicks[a] for a in range(A)]) <= data['budget'], "BudgetConstraint"
problem += pulp.lpSum([data['young_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_young'], "YoungClicksConstraint"
problem += pulp.lpSum([data['old_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_old'], "OldClicksConstraint"
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_unique_young'] + data['goal_unique_old'], "UniqueClicksConstraint"

# Solve the problem
problem.solve()

# Collecting results
clicks_result = [pulp.value(clicks[a]) for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

# Output
output = {
    "clicks": clicks_result,
    "total_unique_clicks": total_unique_clicks
}

print(f' (Objective Value): <OBJ>{total_unique_clicks}</OBJ>')