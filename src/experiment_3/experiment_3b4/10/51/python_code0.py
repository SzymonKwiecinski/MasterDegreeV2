import pulp

# Data extracted from JSON
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

# Number of ad types
A = len(data['young_clicks'])

# Initialize the Linear Programming problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision Variables: number of clicks for each ad type
clicks = [pulp.LpVariable(f"clicks_{a}", lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

# Objective function: Maximize the total number of unique clicks
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)])

# Constraints
# Constraint 1: Age group 18-25 click goal
problem += pulp.lpSum([data['young_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_young']

# Constraint 2: Age group older than 25 click goal
problem += pulp.lpSum([data['old_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_old']

# Constraint 3: Unique clicks goal for age group 18-25
problem += pulp.lpSum([data['unique_clicks'][a] * data['young_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_unique_young']

# Constraint 4: Unique clicks goal for age group older than 25
problem += pulp.lpSum([data['unique_clicks'][a] * data['old_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_unique_old']

# Constraint 5: Budget constraint
problem += pulp.lpSum([data['costs'][a] * clicks[a] for a in range(A)]) <= data['budget']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')