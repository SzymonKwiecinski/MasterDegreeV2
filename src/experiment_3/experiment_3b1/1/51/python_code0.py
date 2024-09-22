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
    'unique_clicks': [40, 75, 90],
    'budget': 105000
}

# Decision variables
A = len(data['young_clicks'])
x = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, cat='Continuous')

# Define the problem
problem = pulp.LpProblem("Tees_Advertising_Campaign", pulp.LpMaximize)

# Objective Function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
# 1. Total clicks from visitors aged 18-25
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Goal_Young_Clicks"

# 2. Total clicks from visitors older than 25
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Goal_Old_Clicks"

# 3. Unique goal for young visitors
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Goal_Unique_Young"

# 4. Unique goal for old visitors
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Goal_Unique_Old"

# 5. Budget constraint
problem += pulp.lpSum(data['costs'][a] * x[a] / 1000 for a in range(A)) <= data['budget'], "Budget_Constraint"

# 6. Maximum allowable clicks for each ad type
for a in range(A):
    problem += x[a] <= data['max_clicks'][a], f"Max_Clicks_{a}"

# Solve the problem
problem.solve()

# Output results
clicks = [x[a].varValue for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_unique_clicks}</OBJ>')
print(f'Clicks purchased for each ad type: {clicks}')