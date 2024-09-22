import pulp
import json

# Data input
data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 
        'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 
        'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 
        'unique_clicks': [40, 75, 90]}

# Define the problem
problem = pulp.LpProblem("Minimize_Advertising_Cost", pulp.LpMinimize)

# Decision variables
A = len(data['young_clicks'])
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=data['max_clicks'], cat='Continuous')

# Objective function: Minimize total cost
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A)), "Total_Cost"

# Constraints
problem += (pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young']), "Goal_Young_Clicks"
problem += (pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old']), "Goal_Old_Clicks"
problem += (pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_young']), "Goal_Unique_Young_Clicks"
problem += (pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_old']), "Goal_Unique_Old_Clicks"

# Solve the problem
problem.solve()

# Output results
clicks_result = [clicks[a].varValue for a in range(A)]
total_cost = pulp.value(problem.objective)

output = {
    "clicks": clicks_result,
    "total_cost": total_cost
}

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')