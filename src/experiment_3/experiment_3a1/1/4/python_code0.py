import pulp
import json

# Parse the provided JSON data
data = json.loads('{"T": 7, "Period": 4, "Demand": [0, 5, 9, 15, 4, 7, 3]}')

# Set parameters based on the data
T = data['T']
Period = data['Period']
Demand = data['Demand']

# Create the Linear Programming problem
problem = pulp.LpProblem("NurseScheduling", pulp.LpMinimize)

# Decision Variables
start = pulp.LpVariable.dicts("start", range(1, T + 1), lowBound=0, cat='Integer')
N = pulp.LpVariable("N", lowBound=0, cat='Integer')

# Objective Function
problem += N, "Minimize_Total_Nurses"

# Constraints
# Total nurses hired
problem += pulp.lpSum(start[j] for j in range(1, T + 1)) == N, "Total_Nurses_Hired"

# Demand satisfaction for each day
for i in range(1, T + 1):
    problem += pulp.lpSum(start[j] for j in range(i, min(i + Period, T + 1))) >= Demand[i - 1], f"Demand_Satisfaction_{i}"

# Solve the problem
problem.solve()

# Output the results
start_values = [pulp.value(start[j]) for j in range(1, T + 1)]
total_nurses = pulp.value(N)

print(f'start = {start_values}')
print(f'total = {total_nurses}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')