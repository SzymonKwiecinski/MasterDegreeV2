import pulp
import json

# Data from JSON
data_json = '{"T": 7, "Period": 4, "Demand": [0, 5, 9, 15, 4, 7, 3]}'
data = json.loads(data_json)

# Parameters
T = data['T']  # Total days (7)
Period = data['Period']  # Working period (4)
Demand = data['Demand']  # Demand for each day

# Define the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Integer') for j in range(1, T + 1)]

# Objective Function
problem += pulp.lpSum(x[j - 1] for j in range(1, T + 1)), "Total_Nurses_Hired"

# Constraints to meet demand
for j in range(T):
    problem += (pulp.lpSum(x[(j - k) % T] for k in range(Period)) >= Demand[j]), f"Demand_Constraint_{j + 1}"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')