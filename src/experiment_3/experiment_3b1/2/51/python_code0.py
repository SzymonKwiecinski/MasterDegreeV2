import pulp
import json

# Data from the provided JSON
data_json = '''{
    "goal_young": 500,
    "goal_old": 600,
    "goal_unique_young": 250,
    "goal_unique_old": 300,
    "young_clicks": [40, 30, 70],
    "old_clicks": [60, 70, 30],
    "costs": [75, 100, 120],
    "max_clicks": [600, 300, 300],
    "unique_clicks": [40, 75, 90],
    "budget": 105000
}'''

data = json.loads(data_json)

# Define the problem
A = len(data['young_clicks'])
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(A), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Young_Visitors_Clicks"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Old_Visitors_Clicks"
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Unique_Young_Visitors_Clicks"
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Unique_Old_Visitors_Clicks"
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)) <= data['budget'], "Budget_Constraint"

# Maximum clicks constraints
for a in range(A):
    problem += x[a] <= data['max_clicks'][a], f"Max_Clicks_{a}"

# Solve the problem
problem.solve()

# Output the results
clicks = [x[a].varValue for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

print(f'Clicks purchased for each ad type: {clicks}')
print(f' (Objective Value): <OBJ>{total_unique_clicks}</OBJ>')