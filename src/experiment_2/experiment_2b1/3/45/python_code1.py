import pulp
import json

# Input data
data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 
        'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 
        'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 
        'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90]}

# Define the problem
problem = pulp.LpProblem("Minimize_Advertising_Cost", pulp.LpMinimize)

# Decision Variables
A = len(data['young_clicks'])
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=0, cat='Continuous')

# Set the upper bounds correctly
for a in range(A):
    clicks[a].upBound = data['max_clicks'][a] / 1000  # convert max_clicks to thousands

# Objective Function
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A)), "Total Cost"

# Constraints
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young'], "Young Clicks Goal"
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old'], "Old Clicks Goal"
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_young'], "Unique Young Clicks Goal"
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_old'], "Unique Old Clicks Goal"

# Solve the problem
problem.solve()

# Output results
results = {
    "clicks": [pulp.value(clicks[a]) * 1000 for a in range(A)],  # Convert back to original scale
    "total_cost": pulp.value(problem.objective)
}

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')