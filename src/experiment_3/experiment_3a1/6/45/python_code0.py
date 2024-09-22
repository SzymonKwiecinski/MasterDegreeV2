import pulp

# Data from the provided JSON format
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

# Variables
A = len(data['costs'])  # Number of different ad types

# Create the linear programming problem
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(A), lowBound=0, upBound=None, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)), "Total_Cost"

# Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Goal_Young_Clicks"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Goal_Old_Clicks"
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Goal_Unique_Young_Clicks"
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Goal_Unique_Old_Clicks"

# Maximum allowable clicks constraints
for a in range(A):
    problem += x[a] <= data['max_clicks'][a] / 1000.0, f"Max_Clicks_{a}"

# Solve the problem
problem.solve()

# Output the results
for a in range(A):
    print(f'x_{a}: {x[a].varValue} (in thousands)')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')