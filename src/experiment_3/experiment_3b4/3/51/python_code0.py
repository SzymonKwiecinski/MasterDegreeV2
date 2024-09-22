import pulp

# Data from JSON
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
A = len(data['unique_clicks'])

# Define the problem
problem = pulp.LpProblem("Custom_Tees_Advertising", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{a+1}", lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

# Objective function
objective = pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A))
problem += objective

# Constraints
# Budget Constraint
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)) <= data['budget'], "Budget_Constraint"

# Young Visitors Clicks Goal
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Young_Clicks_Goal"

# Older Visitors Clicks Goal
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Old_Clicks_Goal"

# Young Unique Visitors Clicks Goal
problem += pulp.lpSum(data['unique_clicks'][a] * data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Young_Unique_Clicks_Goal"

# Older Unique Visitors Clicks Goal
problem += pulp.lpSum(data['unique_clicks'][a] * data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Old_Unique_Clicks_Goal"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')