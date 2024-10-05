from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value, LpStatus, LpBinary

# Problem data
data = {
    "goal_young": 500,
    "goal_old": 600,
    "goal_unique_young": 250,
    "goal_unique_old": 300,
    "young_clicks": [40, 30, 70],
    "old_clicks": [60, 70, 30],
    "costs": [75, 100, 120],
    "max_clicks": [600, 300, 300],
    "unique_clicks": [40, 75, 90]
}

# Extracting data
goal_young = data["goal_young"]
goal_old = data["goal_old"]
goal_unique_young = data["goal_unique_young"]
goal_unique_old = data["goal_unique_old"]
young_clicks = data["young_clicks"]
old_clicks = data["old_clicks"]
costs = data["costs"]
max_clicks = data["max_clicks"]
unique_clicks = data["unique_clicks"]
A = len(young_clicks)

# Define the LP problem
problem = LpProblem("Advertising_Campaign", LpMinimize)

# Variables
clicks = [LpVariable(f"clicks_{a}", lowBound=0, upBound=max_clicks[a], cat="Continuous") for a in range(A)]

# Objective function
problem += lpSum([clicks[a] * costs[a] for a in range(A)])

# Constraints
# Total young clicks
problem += lpSum([clicks[a] * young_clicks[a] for a in range(A)]) >= goal_young * 1000

# Total old clicks
problem += lpSum([clicks[a] * old_clicks[a] for a in range(A)]) >= goal_old * 1000

# Unique young clicks
problem += lpSum([clicks[a] * unique_clicks[a] for a in range(A)]) >= goal_unique_young * 1000

# Unique old clicks
problem += lpSum([clicks[a] * unique_clicks[a] for a in range(A)]) >= goal_unique_old * 1000

# Solve the problem
problem.solve()

# Result extraction
clicks_result = [value(clicks[a]) for a in range(A)]
total_cost = value(problem.objective)

# Output
output = {
    "clicks": [round(c) for c in clicks_result],  # Rounding the results for practical interpretation
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')