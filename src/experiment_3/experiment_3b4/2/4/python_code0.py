import pulp

# Data
data = {
    'T': 7,
    'Period': 4,
    'Demand': [0, 5, 9, 15, 4, 7, 3]
}

# Parameters
T = data['T']
period = data['Period']
demand = data['Demand']

# Problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision Variables
start = [pulp.LpVariable(f'start_{j+1}', lowBound=0, cat='Integer') for j in range(T)]

# Objective Function
problem += pulp.lpSum(start[j] for j in range(T))

# Constraints
for j in range(T):
    problem += pulp.lpSum(start[(j - k) % T] for k in range(period)) >= demand[j]

# Solve the problem
problem.solve()

# Output results
start_values = [pulp.value(start[j]) for j in range(T)]
total_value = pulp.value(problem.objective)

# Print outputs
print(f'Nurses starting each day: {start_values}')
print(f' (Objective Value): <OBJ>{total_value}</OBJ>')