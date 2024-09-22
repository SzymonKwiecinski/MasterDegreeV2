import pulp
import json

# Input data
data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 
        'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 
        'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 
        'unique_clicks': [40, 75, 90]}

# Define the problem
problem = pulp.LpProblem("Minimize_Ad_Campaign_Cost", pulp.LpMinimize)

# Number of ad types
A = len(data['young_clicks'])

# Decision variables for clicks purchased (in thousands)
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=[x / 1000 for x in data['max_clicks']], cat='Continuous')

# Objective function: minimize total cost
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A)), "Total_Cost"

# Constraints
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young'], "Young_Clicks_Requirement"
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old'], "Old_Clicks_Requirement"
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_young'], "Unique_Young_Clicks_Requirement"
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_old'], "Unique_Old_Clicks_Requirement"

# Solve the problem
problem.solve()

# Output the results
total_cost = pulp.value(problem.objective)
clicks_result = [clicks[a].varValue for a in range(A)]

output = {
    "clicks": clicks_result,
    "total_cost": total_cost
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')