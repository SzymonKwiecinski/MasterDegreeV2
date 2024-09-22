import pulp

# Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Variables
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')

# Objective
problem += pulp.lpSum(start[j] for j in range(T)), "Total_Nurses"

# Constraints
for j in range(T):
    problem += pulp.lpSum(start[(j - i) % T] for i in range(period)) >= demand[j], f"Demand_Day_{j+1}"

# Solve
problem.solve()

# Output
start_list = [int(pulp.value(start[j])) for j in range(T)]
total = int(pulp.value(problem.objective))

output = {
    "start": start_list,
    "total": total
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')