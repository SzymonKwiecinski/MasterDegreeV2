import pulp

# Parse the data
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

A = len(data['young_clicks'])

# Define the problem
problem = pulp.LpProblem("Custom_Tees_Advertising", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f"x_{a}", lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

# Objective function
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)), "Total_Cost"

# Constraints
# 1. Age 18-25 Clicks Goal
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young']

# 2. Age >25 Clicks Goal
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old']

# 3. Unique Age 18-25 Clicks Goal
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young']

# 4. Unique Age >25 Clicks Goal
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old']

# Solve the problem
problem.solve()

# Get results
clicks = [x_var.varValue for x_var in x]
total_cost = pulp.value(problem.objective)

# Print the result
print(f"(Objective Value): <OBJ>{total_cost}</OBJ>")