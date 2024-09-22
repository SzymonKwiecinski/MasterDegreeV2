import pulp

# Data from the provided JSON
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

# Parameters
A = len(data['young_clicks'])  # Number of different ad types
goal_young = data['goal_young']
goal_old = data['goal_old']
goal_unique = data['goal_unique_young'] + data['goal_unique_old']
max_clicks = data['max_clicks']
costs = data['costs']
budget = data['budget']

# Decision Variables
x = pulp.LpVariable.dicts('x', range(A), lowBound=0, upBound=None, cat='Continuous')

# Problem definition
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMaximize)

# Objective Function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)), "Total Unique Clicks"

# Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= goal_young, "Young Age Click Goals"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= goal_old, "Old Age Click Goals"
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= goal_unique, "Unique Click Goals"

for a in range(A):
    problem += x[a] <= max_clicks[a], f"Max Clicks for Ad Type {a+1}"

problem += pulp.lpSum(costs[a] * x[a] for a in range(A)) <= budget, "Budget Constraint"

# Solve the problem
problem.solve()

# Output the results
for a in range(A):
    print(f'Clicks purchased for ad type {a + 1}: {x[a].varValue} (in thousands)')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')