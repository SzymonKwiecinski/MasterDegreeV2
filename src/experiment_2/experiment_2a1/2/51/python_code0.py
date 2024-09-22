import pulp
import json

data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300,
        'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120],
        'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}

goal_young = data['goal_young']
goal_old = data['goal_old']
goal_unique_young = data['goal_unique_young']
goal_unique_old = data['goal_unique_old']
young_clicks = data['young_clicks']
old_clicks = data['old_clicks']
costs = data['costs']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']
budget = data['budget']

A = len(young_clicks)  # number of ad types

# Create the LP problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Define decision variables
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=[max_clicks[i] for i in range(A)], cat='Continuous')

# Objective function
problem += pulp.lpSum([unique_clicks[a] * clicks[a] for a in range(A)])

# Constraints for total clicks from young and old
problem += pulp.lpSum([young_clicks[a] * clicks[a] for a in range(A)]) >= goal_young
problem += pulp.lpSum([old_clicks[a] * clicks[a] for a in range(A)]) >= goal_old

# Constraints for unique clicks from young and old
problem += pulp.lpSum([unique_clicks[a] * clicks[a] for a in range(A)]) >= (goal_unique_young + goal_unique_old)

# Budget constraint
problem += pulp.lpSum([costs[a] * clicks[a] for a in range(A)]) <= budget

# Solve the problem
problem.solve()

# Prepare the output
total_unique_clicks = pulp.value(problem.objective)
clicks_result = [pulp.value(clicks[a]) for a in range(A)]

output = {
    "clicks": clicks_result,
    "total_unique_clicks": total_unique_clicks
}

# Print the results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')