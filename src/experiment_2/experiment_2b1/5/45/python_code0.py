import pulp
import json

data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 
        'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 
        'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 
        'unique_clicks': [40, 75, 90]}

# Define the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

A = len(data['young_clicks'])
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=None, cat='Continuous')

# Objective function
problem += pulp.lpSum([data['costs'][a] * clicks[a] for a in range(A)])

# Constraints for total clicks from young and old
problem += pulp.lpSum([data['young_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_young']
problem += pulp.lpSum([data['old_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_old']

# Constraints for unique clicks from young and old
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_unique_young']
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_unique_old']

# Maximum clicks constraints
for a in range(A):
    problem += clicks[a] <= data['max_clicks'][a]

# Solve the problem
problem.solve()

# Output the results
clicks_result = [pulp.value(clicks[a]) for a in range(A)]
total_cost = pulp.value(problem.objective)

output = {
    "clicks": clicks_result,
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')