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

# Problem definition
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision variables
clicks = [pulp.LpVariable(f'clicks_{i}', lowBound=0, cat='Continuous') for i in range(len(data['costs']))]

# Objective function
problem += pulp.lpSum(data['unique_clicks'][i] * clicks[i] for i in range(len(data['unique_clicks']))), "Total_Unique_Clicks"

# Constraints
problem += pulp.lpSum(data['costs'][i] * clicks[i] for i in range(len(data['costs']))) <= data['budget'], "Budget_Constraint"

problem += pulp.lpSum(data['young_clicks'][i] * clicks[i] for i in range(len(data['young_clicks']))) >= data['goal_young'], "Goal_Young_Clicks"

problem += pulp.lpSum(data['old_clicks'][i] * clicks[i] for i in range(len(data['old_clicks']))) >= data['goal_old'], "Goal_Old_Clicks"

problem += pulp.lpSum(data['unique_clicks'][i] * data['young_clicks'][i] * clicks[i] for i in range(len(data['unique_clicks']))) >= data['goal_unique_young'], "Goal_Unique_Young_Clicks"

problem += pulp.lpSum(data['unique_clicks'][i] * data['old_clicks'][i] * clicks[i] for i in range(len(data['unique_clicks']))) >= data['goal_unique_old'], "Goal_Unique_Old_Clicks"

for i in range(len(data['max_clicks'])):
    problem += clicks[i] <= data['max_clicks'][i], f"Max_Clicks_Ad_{i+1}"

# Solve
problem.solve()

# Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')