import pulp

# Data from the JSON format
data = {
    'goal_young': 500,
    'goal_old': 600,
    'goal_unique_young': 250,
    'goal_unique_old': 300,
    'young_clicks': [40, 30, 70],
    'old_clicks': [60, 70, 30],
    'costs': [75, 100, 120],
    'max_clicks': [600, 300, 300],
    'unique_clicks': [40, 75, 90]
}

# Define the problem
problem = pulp.LpProblem("Custom_Tees_Ad_Campaign", pulp.LpMinimize)

# Decision variables
number_of_ads = len(data['costs'])
clicks = pulp.LpVariable.dicts("clicks", range(number_of_ads), lowBound=0)

# Objective function
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(number_of_ads))

# Constraints
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(number_of_ads)) >= data['goal_young']
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(number_of_ads)) >= data['goal_old']
problem += pulp.lpSum(data['unique_clicks'][a] * data['young_clicks'][a] * clicks[a] for a in range(number_of_ads)) >= data['goal_unique_young']
problem += pulp.lpSum(data['unique_clicks'][a] * data['old_clicks'][a] * clicks[a] for a in range(number_of_ads)) >= data['goal_unique_old']

# Maximum clicks constraint
for a in range(number_of_ads):
    problem += clicks[a] <= data['max_clicks'][a]

# Solve the problem
problem.solve()

# Output the results
results = {a: clicks[a].varValue for a in range(number_of_ads)}
total_cost = pulp.value(problem.objective)

print(f'Clicks: {results}')
print(f'Total Cost: {total_cost}')

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')