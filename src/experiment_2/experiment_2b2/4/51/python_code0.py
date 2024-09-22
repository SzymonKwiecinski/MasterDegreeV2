import pulp

# Load the data from JSON
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

# Extract parameters from data
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

# Number of ad types
A = len(young_clicks)

# Define the LP problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision variables: number of clicks for each ad type
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=max_clicks[a-1], cat='Continuous') for a in range(1, A+1)]

# Objective function: maximize the total number of unique clicks
problem += pulp.lpSum([unique_clicks[a] * clicks[a] for a in range(A)])

# Constraints
# Budget constraint
problem += pulp.lpSum([costs[a] * clicks[a] for a in range(A)]) <= budget

# Click goals for the age range 18-25
problem += pulp.lpSum([young_clicks[a] * clicks[a] for a in range(A)]) >= goal_young

# Click goals for the age range older than 25
problem += pulp.lpSum([old_clicks[a] * clicks[a] for a in range(A)]) >= goal_old

# Unique click goals for the age range 18-25
problem += pulp.lpSum([young_clicks[a] * unique_clicks[a] * clicks[a]/100 for a in range(A)]) >= goal_unique_young

# Unique click goals for the age range older than 25
problem += pulp.lpSum([old_clicks[a] * unique_clicks[a] * clicks[a]/100 for a in range(A)]) >= goal_unique_old

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "clicks": [pulp.value(clicks[a]) for a in range(A)],
    "total_unique_clicks": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')