import pulp

# Data from JSON
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

# Define the problem
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMaximize)

# Decision Variables
A = len(data['young_clicks'])  # Number of ad types
x = pulp.LpVariable.dicts("x", range(1, A + 1), lowBound=0, upBound=None)

# Objective Function
problem += pulp.lpSum(data['unique_clicks'][a - 1] * x[a] for a in range(1, A + 1)), "Total_Unique_Clicks"

# Constraints
# Budget Constraint
problem += pulp.lpSum(data['costs'][a - 1] * x[a] for a in range(1, A + 1)) <= data['budget'], "Budget_Constraint"

# Click Constraints for Visitors Aged 18-25
problem += pulp.lpSum(data['young_clicks'][a - 1] * x[a] for a in range(1, A + 1)) >= data['goal_young'], "Goal_Young_Constraint"

# Click Constraints for Visitors Older than 25
problem += pulp.lpSum(data['old_clicks'][a - 1] * x[a] for a in range(1, A + 1)) >= data['goal_old'], "Goal_Old_Constraint"

# Unique Clicks for Visitors Aged 18-25
problem += pulp.lpSum(data['unique_clicks'][a - 1] * x[a] for a in range(1, A + 1)) >= data['goal_unique_young'], "Unique_Young_Constraint"

# Unique Clicks for Visitors Older than 25
problem += pulp.lpSum(data['unique_clicks'][a - 1] * x[a] for a in range(1, A + 1)) >= data['goal_unique_old'], "Unique_Old_Constraint"

# Maximum Click Constraints
for a in range(1, A + 1):
    problem += x[a] <= data['max_clicks'][a - 1], f"Max_Click_Constraint_{a}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')