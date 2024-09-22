import pulp

# Data from the provided JSON format
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

# Extracting data for easier access
A = len(data['young_clicks'])  # Number of ad types
young_clicks = data['young_clicks']
old_clicks = data['old_clicks']
costs = data['costs']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']
budget = data['budget']
goal_young = data['goal_young']
goal_old = data['goal_old']
goal_unique_young = data['goal_unique_young']
goal_unique_old = data['goal_unique_old']

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(A), lowBound=0)

# Set up upper bounds for decision variables
for a in range(A):
    x[a].upBound = max_clicks[a]

# Objective Function
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
# Budget constraint
problem += pulp.lpSum(costs[a] * x[a] for a in range(A)) <= budget, "Budget_Constraint"

# Age group click constraints
problem += pulp.lpSum(young_clicks[a] * x[a] for a in range(A)) >= goal_young, "Goal_Young_Constraint"
problem += pulp.lpSum(old_clicks[a] * x[a] for a in range(A)) >= goal_old, "Goal_Old_Constraint"

# Unique click constraints
problem += pulp.lpSum(unique_clicks[a] * young_clicks[a] * x[a] for a in range(A)) >= goal_unique_young, "Goal_Unique_Young_Constraint"
problem += pulp.lpSum(unique_clicks[a] * old_clicks[a] * x[a] for a in range(A)) >= goal_unique_old, "Goal_Unique_Old_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')