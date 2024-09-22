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
    'unique_clicks': [40, 75, 90],
    'budget': 105000
}

# Create a problem variable
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f'x_{a}', lowBound=0, upBound=data['max_clicks'][a], cat='Integer') for a in range(len(data['unique_clicks']))]

# Objective function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(len(data['unique_clicks'])))

# Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(len(data['young_clicks']))) >= data['goal_young'], "Young_Age_Clicks"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(len(data['old_clicks']))) >= data['goal_old'], "Old_Age_Clicks"
problem += pulp.lpSum(data['unique_clicks'][a] * data['young_clicks'][a] * x[a] for a in range(len(data['young_clicks']))) >= data['goal_unique_young'], "Unique_Young_Age_Clicks"
problem += pulp.lpSum(data['unique_clicks'][a] * data['old_clicks'][a] * x[a] for a in range(len(data['old_clicks']))) >= data['goal_unique_old'], "Unique_Old_Age_Clicks"
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(len(data['costs']))) <= data['budget'], "Budget_Constraint"

# Solve the problem
problem.solve()

# Display the results
for var in x:
    print(f'{var.name} = {var.varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')