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

# Decision variables
ad_types = range(len(data['young_clicks']))
x = pulp.LpVariable.dicts("clicks", ad_types, lowBound=0, upBound=None, cat='Continuous')  # Fixed upBound to None

# Define the problem
problem = pulp.LpProblem("Tees_Advertising_Campaign", pulp.LpMaximize)

# Objective function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in ad_types), "Total_Unique_Clicks"

# Constraints
# Budget Constraint
problem += pulp.lpSum(data['costs'][a] * x[a] for a in ad_types) <= data['budget'], "Budget_Constraint"

# Age Group Click Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in ad_types) >= data['goal_young'], "Young_Click_Constraint"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in ad_types) >= data['goal_old'], "Old_Click_Constraint"

# Unique Click Constraints for Age Groups
problem += pulp.lpSum(data['young_clicks'][a] * data['unique_clicks'][a] * x[a] for a in ad_types) >= data['goal_unique_young'], "Unique_Young_Click_Constraint"
problem += pulp.lpSum(data['old_clicks'][a] * data['unique_clicks'][a] * x[a] for a in ad_types) >= data['goal_unique_old'], "Unique_Old_Click_Constraint"

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')