import pulp
import json

# Input data
data = {'goal_young': 500, 
        'goal_old': 600, 
        'goal_unique_young': 250, 
        'goal_unique_old': 300, 
        'young_clicks': [40, 30, 70], 
        'old_clicks': [60, 70, 30], 
        'costs': [75, 100, 120], 
        'max_clicks': [600, 300, 300], 
        'unique_clicks': [40, 75, 90]}

# Problem setup
A = len(data['young_clicks'])
problem = pulp.LpProblem("Minimize_Advertising_Cost", pulp.LpMinimize)

# Decision variables
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=None, cat='Continuous')

# Objective function
total_cost = pulp.lpSum([data['costs'][a] * clicks[a] for a in range(A)])
problem += total_cost

# Constraints
problem += pulp.lpSum([data['young_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_young'], "YoungClicks"
problem += pulp.lpSum([data['old_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_old'], "OldClicks"
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_unique_young'], "UniqueYoungClicks"
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_unique_old'], "UniqueOldClicks"

# Max clicks constraints
for a in range(A):
    problem += clicks[a] <= data['max_clicks'][a], f"MaxClicks_{a}"

# Solve the problem
problem.solve()

# Prepare output
result_clicks = [clicks[a].varValue for a in range(A)]
total_cost_value = pulp.value(problem.objective)

output = {
    "clicks": result_clicks,
    "total_cost": total_cost_value
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')