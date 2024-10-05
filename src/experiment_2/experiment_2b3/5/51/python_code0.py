import pulp

# Define the problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Parse the input data
data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}

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

A = len(young_clicks)  # Number of ad types

# Define decision variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=max_clicks[a], cat='Continuous') for a in range(A)]

# Define the objective function
problem += pulp.lpSum(unique_clicks[a] / 100 * clicks[a] for a in range(A)), "Total Unique Clicks"

# Define the constraints
# Constraint for budget
problem += pulp.lpSum(costs[a] * clicks[a] for a in range(A)) <= budget, "Budget Constraint"

# Constraint for young clicks
problem += pulp.lpSum(young_clicks[a] / 100 * clicks[a] for a in range(A)) >= goal_young, "Young Clicks Constraint"

# Constraint for old clicks
problem += pulp.lpSum(old_clicks[a] / 100 * clicks[a] for a in range(A)) >= goal_old, "Old Clicks Constraint"

# Constraint for unique young clicks
problem += pulp.lpSum(young_clicks[a] / 100 * unique_clicks[a] / 100 * clicks[a] for a in range(A)) >= goal_unique_young, "Unique Young Clicks Constraint"

# Constraint for unique old clicks
problem += pulp.lpSum(old_clicks[a] / 100 * unique_clicks[a] / 100 * clicks[a] for a in range(A)) >= goal_unique_old, "Unique Old Clicks Constraint"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "clicks": [pulp.value(clicks[a]) for a in range(A)],
    "total_unique_clicks": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')