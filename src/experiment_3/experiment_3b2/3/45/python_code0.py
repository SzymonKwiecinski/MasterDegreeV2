import pulp

# Data from the problem
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
problem = pulp.LpProblem("Ad_Campaign_Cost_Minimization", pulp.LpMinimize)

# Decision variables
A = len(data['young_clicks'])
x = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)), "Total_Cost"

# Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Goal_Young"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Goal_Old"
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Goal_Unique_Young"
problem += pulp.lpSum((1 - data['unique_clicks'][a]) * x[a] for a in range(A)) >= data['goal_unique_old'], "Goal_Unique_Old"

# Upper bounds on x
for a in range(A):
    problem += x[a] <= data['max_clicks'][a], f"Max_Clicks_{a}"

# Solve the problem
problem.solve()

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')