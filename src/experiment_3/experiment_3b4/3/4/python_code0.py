import pulp

# Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
Period = data['Period']
demand = data['Demand']

# Problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Integer') for j in range(T)]

# Objective
problem += pulp.lpSum(x[j] for j in range(T)), "Total_Nurses"

# Constraints
for j in range(T):
    problem += pulp.lpSum(x[(j + i) % T] for i in range(Period)) >= demand[j], f"Demand_Day_{j+1}"

# Solve
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')