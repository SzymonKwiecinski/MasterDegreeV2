import pulp
import json

data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 
        'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 
        'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 
        'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 
        'budget': 105000}

# Parameters from the data
goal_young = data['goal_young']
goal_old = data['goal_old']
goal_unique_young = data['goal_unique_young']
goal_unique_old = data['goal_unique_old']
young_clicks = data['young_clicks']
old_clicks = data['old_clicks']
costs = data['costs']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']
budget = data['budget']
A = len(young_clicks)

# Create the LP problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision variables
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=None, cat='Continuous')

# Objective function: maximize total unique clicks
problem += pulp.lpSum([unique_clicks[a] * clicks[a] for a in range(A)])

# Constraints
# Budget constraint
problem += pulp.lpSum([costs[a] * clicks[a] for a in range(A)]) <= budget

# Click goals for young and old demographics
problem += pulp.lpSum([young_clicks[a] * clicks[a] for a in range(A)]) >= goal_young
problem += pulp.lpSum([old_clicks[a] * clicks[a] for a in range(A)]) >= goal_old

# Uniqueness goals
problem += pulp.lpSum([unique_clicks[a] * clicks[a] for a in range(A)]) >= (goal_unique_young + goal_unique_old)

# Max clicks constraints
for a in range(A):
    problem += clicks[a] <= max_clicks[a]

# Solve the problem
problem.solve()

# Prepare the output
clicks_result = [pulp.value(clicks[a]) for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

output = {
    "clicks": clicks_result,
    "total_unique_clicks": total_unique_clicks
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')