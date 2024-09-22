import pulp
import json

# Input data
data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300,
        'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120],
        'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90]}

# Define the problem
problem = pulp.LpProblem("Advertising_Campaign", pulp.LpMinimize)

# Variables: clicks_a for each ad type a
A = len(data['young_clicks'])
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

# Objective function: Minimize total cost
total_cost = pulp.lpSum([data['costs'][a] * clicks[a] for a in range(A)])
problem += total_cost

# Constraints
problem += pulp.lpSum([data['young_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_young']
problem += pulp.lpSum([data['old_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_old']
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_unique_young']
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_unique_old']

# Solve the problem
problem.solve()

# Prepare the output
clicks_result = [clicks[a].varValue for a in range(A)]
total_cost_value = pulp.value(problem.objective)

output = {
    "clicks": clicks_result,
    "total_cost": total_cost_value
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')