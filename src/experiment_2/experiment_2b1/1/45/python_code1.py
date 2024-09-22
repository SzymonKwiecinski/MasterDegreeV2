import pulp
import json

data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 
        'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 
        'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 
        'unique_clicks': [40, 75, 90]}

# Define the problem
problem = pulp.LpProblem("Ad_Campaign_Optimization", pulp.LpMinimize)

# Define decision variables
A = len(data['young_clicks'])
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=600, cat='Continuous')  # Correct upper bound

# Define the objective function
problem += pulp.lpSum([data['costs'][a] * clicks[a] for a in range(A)])

# Define constraints
problem += pulp.lpSum([data['young_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_young']
problem += pulp.lpSum([data['old_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_old']
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_unique_young']
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_unique_old']

# Solve the problem
problem.solve()

# Extract results
clicks_result = [pulp.value(clicks[a]) for a in range(A)]
total_cost = pulp.value(problem.objective)

# Output the results
output = {
    "clicks": clicks_result,
    "total_cost": total_cost
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')