import pulp
import json

# Input data from JSON
data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 
        'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 
        'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 
        'unique_clicks': [40, 75, 90], 'budget': 105000}

# Define the problem
problem = pulp.LpProblem("Advertising_Campaign", pulp.LpMaximize)

# Number of ad types
A = len(data['young_clicks'])

# Decision variables: clicks_a
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=None, cat='Continuous')

# Objective function: Maximize total unique clicks
total_unique_clicks = pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A))
problem += total_unique_clicks

# Constraints
# Budget constraint
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A)) <= data['budget'], "BudgetConstraint"

# Max clicks constraints
for a in range(A):
    problem += clicks[a] <= data['max_clicks'][a], f"MaxClicksConstraint_{a}"

# Goal for young clicks
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young'], "YoungClickGoal"

# Goal for old clicks
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old'], "OldClickGoal"

# Solve the problem
problem.solve()

# Get the result
clicks_result = [clicks[a].varValue for a in range(A)]
total_unique_clicks_result = pulp.value(problem.objective)

# Output result
result = {
    "clicks": clicks_result,
    "total_unique_clicks": total_unique_clicks_result
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')