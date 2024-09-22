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
    'unique_clicks': [40, 75, 90]
}

# Define the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Number of alternatives
A = len(data['costs'])

# Define decision variables
x = pulp.LpVariable.dicts("x", range(A), lowBound=0)

# Objective function
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)), "Total Cost"

# Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Young Clicks Goal"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Old Clicks Goal"
problem += pulp.lpSum(data['young_clicks'][a] * data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Unique Young Clicks Goal"
problem += pulp.lpSum(data['old_clicks'][a] * data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Unique Old Clicks Goal"

# Max clicks constraints
for a in range(A):
    problem += x[a] <= data['max_clicks'][a], f"Max Clicks {a}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')