import pulp

# Data from JSON
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Initialize the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables
start = [pulp.LpVariable(f'start_{j+1}', lowBound=0, cat='Integer') for j in range(T)]

# Objective function: Minimize total number of nurses hired
problem += pulp.lpSum(start)

# Constraints
for j in range(T):
    demand_constraint = start[j]
    for k in range(1, period):
        demand_constraint += start[(j - k) % T]
    problem += (demand_constraint >= demand[j], f"Demand_Constraint_Day_{j+1}")

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')