import pulp
import json

# Data provided in JSON format
data = json.loads('{"T": 7, "Period": 4, "Demand": [0, 5, 9, 15, 4, 7, 3]}')

# Parameters
T = data['T']  # Number of days
period = data['Period']  # Consecutive days a nurse works
demand = data['Demand']  # Demand for nurses for each day

# Initialize the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(1, T + 1), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum([x[j] for j in range(1, T + 1)]), "Total_Nurses_Hired"

# Constraints to meet the demand for each day
for j in range(1, T + 1):
    problem += (pulp.lpSum([x[(j - k - 1) % T + 1] for k in range(period)]) >= demand[j - 1]), f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare the result
start = [x[j].varValue for j in range(1, T + 1)]
total_nurses_hired = pulp.value(problem.objective)

# Print the results
print(f'Start: {start}')
print(f'Total Nurses Hired: {total_nurses_hired}')
print(f' (Objective Value): <OBJ>{total_nurses_hired}</OBJ>')