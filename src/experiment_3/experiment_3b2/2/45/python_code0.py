import pulp

# Data from the provided JSON
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

# Number of ad types
A = len(data['costs'])

# Initialize the problem
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=data['max_clicks'], cat='Continuous')

# Objective function
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)), "Total_Cost"

# Constraints
problem += (pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Goal_Young_Clicks")
problem += (pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Goal_Old_Clicks")
problem += (pulp.lpSum(data['unique_clicks'][a] * data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Goal_Unique_Young_Clicks")
problem += (pulp.lpSum(data['unique_clicks'][a] * data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Goal_Unique_Old_Clicks")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')