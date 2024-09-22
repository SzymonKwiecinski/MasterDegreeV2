import pulp
import json

# Data input
data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300,
        'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120],
        'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}

# Problem definition
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision variables
A = len(data['young_clicks'])
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=[data['max_clicks'][i] for i in range(A)], cat='Continuous')

# Objective function: maximize total unique clicks
problem += pulp.lpSum([data['unique_clicks'][i] * clicks[i] for i in range(A)]), "Total_Unique_Clicks"

# Constraints for clicks
problem += pulp.lpSum([data['young_clicks'][i] * clicks[i] for i in range(A)]) >= data['goal_young'], "Young_Clicks_Requirement"
problem += pulp.lpSum([data['old_clicks'][i] * clicks[i] for i in range(A)]) >= data['goal_old'], "Old_Clicks_Requirement"
problem += pulp.lpSum([data['costs'][i] * clicks[i] for i in range(A)]) <= data['budget'], "Budget_Constraint"

# Solve the problem
problem.solve()

# Extracting the results
result_clicks = [clicks[i].varValue for i in range(A)]
total_unique_clicks = pulp.value(problem.objective)

# Output
output = {
    "clicks": result_clicks,
    "total_unique_clicks": total_unique_clicks
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')