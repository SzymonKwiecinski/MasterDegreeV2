import pulp
import json

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
    'unique_clicks': [40, 75, 90],
    'budget': 105000
}

# Define the problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision Variables
A = len(data['young_clicks'])
x = pulp.LpVariable.dicts("x", range(A), lowBound=0, upBound=None, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
# Budget Constraint
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)) <= data['budget'], "Budget_Constraint"

# Clicks Constraints for Different Age Groups
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Young_Clicks_Constraint"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Old_Clicks_Constraint"

# Unique Clicks Constraints for Age Groups
problem += pulp.lpSum(data['young_clicks'][a] * data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Unique_Young_Clicks_Constraint"
problem += pulp.lpSum(data['old_clicks'][a] * data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Unique_Old_Clicks_Constraint"

# Solve the problem
problem.solve()

# Print the results
for a in range(A):
    print(f'x_{a+1} (Clicks for ad type {a+1}): {x[a].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')