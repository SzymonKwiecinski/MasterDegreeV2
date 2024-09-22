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

# Parameters
A = len(data['costs'])  # Number of ad types
goal_young = data['goal_young']
goal_old = data['goal_old']
goal_unique_young = data['goal_unique_young']
goal_unique_old = data['goal_unique_old']
young_clicks = data['young_clicks']
old_clicks = data['old_clicks']
costs = data['costs']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']

# Define the problem
problem = pulp.LpProblem("Tees_Advertising_Campaign", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(A), lowBound=0, upBound=None, cat='Continuous')

# Objective Function
problem += pulp.lpSum(costs[a] * x[a] for a in range(A)), "Total_Cost"

# Constraints
problem += pulp.lpSum(young_clicks[a] * x[a] for a in range(A)) >= goal_young, "Young_Clicks_Constraint"
problem += pulp.lpSum(old_clicks[a] * x[a] for a in range(A)) >= goal_old, "Old_Clicks_Constraint"
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)) >= goal_unique_young, "Unique_Young_Clicks_Constraint"
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)) >= goal_unique_old, "Unique_Old_Clicks_Constraint"
for a in range(A):
    problem += x[a] <= max_clicks[a], f"Max_Clicks_Constraint_{a+1}"

# Solve the problem
problem.solve()

# Output the results
clicks = [x[a].varValue for a in range(A)]
total_cost = pulp.value(problem.objective)

print(f'Clicks: {clicks}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')