import pulp

# Input data
data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}

# Number of ad types
A = len(data['young_clicks'])

# LP Problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

# Objective function
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)]), "Total Unique Clicks"

# Constraints
# Budget constraint
problem += pulp.lpSum([data['costs'][a] * clicks[a] for a in range(A)]) <= data['budget'], "Budget"

# Young visitor click goal
problem += pulp.lpSum([data['young_clicks'][a] * clicks[a] / 100 for a in range(A)]) >= data['goal_young'], "Young Clicks Goal"

# Old visitor click goal
problem += pulp.lpSum([data['old_clicks'][a] * clicks[a] / 100 for a in range(A)]) >= data['goal_old'], "Old Clicks Goal"

# Unique young visitor click goal
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] / 100 for a in range(A) if data['young_clicks'][a] != 0]) >= data['goal_unique_young'], "Unique Young Clicks Goal"

# Unique old visitor click goal
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] / 100 for a in range(A) if data['old_clicks'][a] != 0]) >= data['goal_unique_old'], "Unique Old Clicks Goal"

# Solve the problem
problem.solve()

# Prepare the output
clicks_solution = [pulp.value(clicks[a]) for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

output = {
    "clicks": clicks_solution,
    "total_unique_clicks": total_unique_clicks
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')