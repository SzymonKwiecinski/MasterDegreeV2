import pulp

# Problem Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}

# Define the problem
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f"x_{j}", lowBound=0, cat='Integer') for j in range(data['T'])]

# Objective Function
problem += pulp.lpSum(x), "Total Number of Nurses"

# Constraints
for j in range(data['T']):
    problem += pulp.lpSum(x[(j-i) % data['T']] for i in range(data['Period'])) >= data['Demand'][j], f"Demand_Constraint_Day_{j+1}"

# Solve the problem
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')