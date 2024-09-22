import pulp

# Data
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

# Decision Variables
num_ads = len(data['costs'])
x = [pulp.LpVariable(f'x_{a}', lowBound=0, upBound=data['max_clicks'][a]) for a in range(num_ads)]

# Problem
problem = pulp.LpProblem("Minimize_Advertising_Costs", pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum([data['costs'][a] * x[a] for a in range(num_ads)])

# Constraints
problem += pulp.lpSum([data['young_clicks'][a] * x[a] for a in range(num_ads)]) >= data['goal_young']
problem += pulp.lpSum([data['old_clicks'][a] * x[a] for a in range(num_ads)]) >= data['goal_old']
problem += pulp.lpSum([data['unique_clicks'][a] * data['young_clicks'][a] * x[a] for a in range(num_ads)]) >= data['goal_unique_young']
problem += pulp.lpSum([data['unique_clicks'][a] * data['old_clicks'][a] * x[a] for a in range(num_ads)]) >= data['goal_unique_old']

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')