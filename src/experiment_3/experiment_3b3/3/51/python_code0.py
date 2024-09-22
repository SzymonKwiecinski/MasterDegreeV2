import pulp

# Constants and data from the JSON
goal_young = 500
goal_old = 600
goal_unique_young = 250
goal_unique_old = 300
young_clicks = [40, 30, 70]
old_clicks = [60, 70, 30]
costs = [75, 100, 120]
max_clicks = [600, 300, 300]
unique_clicks = [40, 75, 90]
budget = 105000

# Number of ad types
A = len(young_clicks)

# Define the problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Define decision variables
x = [pulp.LpVariable(f'x_{a}', lowBound=0, upBound=max_clicks[a], cat='Continuous') for a in range(A)]

# Objective function
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
problem += pulp.lpSum(young_clicks[a] * x[a] for a in range(A)) >= goal_young, "Young_Clicks_Target"
problem += pulp.lpSum(old_clicks[a] * x[a] for a in range(A)) >= goal_old, "Old_Clicks_Target"
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)) >= (goal_unique_young + goal_unique_old), "Unique_Clicks_Target"
problem += pulp.lpSum(costs[a] * x[a] for a in range(A)) <= budget, "Budget_Constraint"

# Solve the problem
problem.solve()

# Results
clicks = [pulp.value(x_var) for x_var in x]
total_unique_clicks = pulp.value(problem.objective)

print(f'Clicks (in thousands) for each ad type: {clicks}')
print(f'Total Unique Clicks (Objective Value): <OBJ>{total_unique_clicks}</OBJ>')