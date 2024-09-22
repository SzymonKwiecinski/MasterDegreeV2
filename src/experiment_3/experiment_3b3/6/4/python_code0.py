import pulp

# Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
p = data['Period']
demand = data['Demand']

# Problem
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Integer') for j in range(T)]

# Objective function
problem += pulp.lpSum(x[j] for j in range(T)), "Total_Nurses"

# Constraints
for j in range(T):
    problem += pulp.lpSum(x[(j-i) % T] for i in range(p)) >= demand[j], f"Demand_Day_{j+1}"

# Solve
problem.solve()

# Results
start = [pulp.value(x[j]) for j in range(T)]
total_nurses = sum(start)

print("start:", start)
print("total:", total_nurses)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')