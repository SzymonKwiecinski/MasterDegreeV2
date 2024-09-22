import pulp

# Input data
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
A = len(data['young_clicks'])
problem = pulp.LpProblem("Minimize_Ad_Campaign_Cost", pulp.LpMinimize)

# Decision variables
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=data['max_clicks'], cat='Continuous')

# Objective function
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A)), "Total_Cost"

# Constraints
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young'], "Young_Click_Constraint"
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old'], "Old_Click_Constraint"
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_young'], "Unique_Young_Click_Constraint"
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_old'], "Unique_Old_Click_Constraint"

# Solve the problem
problem.solve()

# Prepare output
clicks_solution = [clicks[a].varValue for a in range(A)]
total_cost = pulp.value(problem.objective)

# Output
output = {
    "clicks": clicks_solution,
    "total_cost": total_cost
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')