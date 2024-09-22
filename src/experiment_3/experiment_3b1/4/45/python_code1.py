import pulp
import json

# Data provided in JSON format
data = json.loads("""{"goal_young": 500, "goal_old": 600, "goal_unique_young": 250, "goal_unique_old": 300, "young_clicks": [40, 30, 70], "old_clicks": [60, 70, 30], "costs": [75, 100, 120], "max_clicks": [600, 300, 300], "unique_clicks": [40, 75, 90]}""")

# Initialize the problem
problem = pulp.LpProblem("Advertising_Campaign", pulp.LpMinimize)

# Number of ad types
A = len(data['costs'])

# Decision variables
x = pulp.LpVariable.dicts("Clicks", range(A), lowBound=0, upBound=data['max_clicks'], cat='Continuous')

# Objective function
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A))

# Constraints
problem += (pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Young_Clicks_Constraint")
problem += (pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Old_Clicks_Constraint")
problem += (pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Unique_Young_Clicks_Constraint")
problem += (pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Unique_Old_Clicks_Constraint")

# Solve the problem
problem.solve()

# Output the results
clicks = [x[a].varValue for a in range(A)]
total_cost = pulp.value(problem.objective)

print(f'Clicks: {clicks}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')