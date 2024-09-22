import pulp
import json

# Input data
data = {'goal_young': 500, 'goal_old': 600, 
        'goal_unique_young': 250, 'goal_unique_old': 300, 
        'young_clicks': [40, 30, 70], 
        'old_clicks': [60, 70, 30], 
        'costs': [75, 100, 120], 
        'max_clicks': [600, 300, 300], 
        'unique_clicks': [40, 75, 90]}

# Define the problem
problem = pulp.LpProblem("Advertising_Campaign", pulp.LpMinimize)

# Number of ad types
A = len(data['young_clicks'])

# Decision variables for clicks purchased for each ad type
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=data['max_clicks'], cat='Continuous')

# Objective function: Minimize the total cost
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A)), "Total_Cost"

# Constraints
# Total clicks from young visitors
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young'], "Young_Clicks_Req"

# Total clicks from old visitors
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old'], "Old_Clicks_Req"

# Unique clicks from young visitors
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_young'], "Unique_Young_Clicks_Req"

# Unique clicks from old visitors
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_old'], "Unique_Old_Clicks_Req"

# Solve the problem
problem.solve()

# Output results
output = {
    "clicks": [clicks[a].varValue for a in range(A)],
    "total_cost": pulp.value(problem.objective)
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')