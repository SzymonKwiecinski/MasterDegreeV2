import pulp

# Data provided
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

# Initialize the problem
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMaximize)

# Define the decision variables
A = len(data['unique_clicks'])
x = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=None)

# Objective function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Young_Visitor_Clicks"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Old_Visitor_Clicks"
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Unique_Clicks_Young"
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Unique_Clicks_Old"
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)) <= data['budget'], "Budget_Constraint"

for a in range(A):
    problem += x[a] <= data['max_clicks'][a], f"Max_Clicks_Ad_{a+1}"

# Solve the problem
problem.solve()

# Output the results
for a in range(A):
    print(f'Clicks purchased for ad type {a+1}: {x[a].varValue} thousands')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')