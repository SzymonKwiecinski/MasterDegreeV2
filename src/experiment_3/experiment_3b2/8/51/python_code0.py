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

# Number of ad types
A = len(data['young_clicks'])

# Create the problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(A), lowBound=0, upBound=None, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Goal_Young_Visitors"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Goal_Old_Visitors"
problem += pulp.lpSum(data['young_clicks'][a] * data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Goal_Unique_Young_Visitors"
problem += pulp.lpSum(data['old_clicks'][a] * data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Goal_Unique_Old_Visitors"
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)) <= data['budget'], "Budget_Constraint"

# Maximum allowable clicks
for a in range(A):
    problem += x[a] <= data['max_clicks'][a], f"Max_Clicks_{a}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')