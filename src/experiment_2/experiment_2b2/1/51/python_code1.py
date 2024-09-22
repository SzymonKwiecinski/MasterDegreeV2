from pulp import LpProblem, LpVariable, lpSum, LpMaximize, value

# Data from the problem
data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 
        'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 
        'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}

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

A = len(young_clicks)  # Number of ad types

# Create a problem variable
problem = LpProblem("Ad_Campaign_Optimization", LpMaximize)

# Decision variables
clicks = [LpVariable(f'clicks_{a}', lowBound=0, upBound=max_clicks[a]) for a in range(A)]

# Objective function: Maximize unique clicks
problem += lpSum(unique_clicks[a] * clicks[a] for a in range(A))

# Constraints
# Total number of young clicks target
problem += lpSum(young_clicks[a] * clicks[a] for a in range(A)) >= goal_young

# Total number of old clicks target
problem += lpSum(old_clicks[a] * clicks[a] for a in range(A)) >= goal_old

# Total number of unique young clicks target
problem += lpSum(unique_clicks[a] * clicks[a] * (young_clicks[a]/100) for a in range(A)) >= goal_unique_young

# Total number of unique old clicks target
problem += lpSum(unique_clicks[a] * clicks[a] * (old_clicks[a]/100) for a in range(A)) >= goal_unique_old

# Budget constraint
problem += lpSum(costs[a] * clicks[a] for a in range(A)) <= budget

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "clicks": [clicks[a].varValue for a in range(A)],
    "total_unique_clicks": value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')