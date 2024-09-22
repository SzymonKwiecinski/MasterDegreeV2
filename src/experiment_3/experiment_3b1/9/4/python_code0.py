import pulp
import json

# Input data
data = json.loads('{"T": 7, "Period": 4, "Demand": [0, 5, 9, 15, 4, 7, 3]}')
T = data['T']
Period = data['Period']
Demand = data['Demand']

# Create the model
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Define decision variables
start = pulp.LpVariable.dicts("start", range(1, T + 1), lowBound=0, cat='Integer')

# Objective function: Minimize total number of nurses hired
problem += pulp.lpSum(start[j] for j in range(1, T + 1)), "Total_Nurses"

# Constraints to meet demand for each day
for j in range(1, T + 1):
    problem += (pulp.lpSum(start[j-i] for i in range(Period) if j-i >= 1) >= Demand[j-1]), f"Demand_Constraint_{j}"

# Constraints for periods that cannot start new shifts
for j in range(T - Period + 2, T + 1):
    problem += (start[j] == 0), f"Zero_Starts_After_{j}"

# Solve the problem
problem.solve()

# Output results
start_values = [start[j].varValue for j in range(1, T + 1)]
total_nurses = pulp.value(problem.objective)

print(f'Start Values: {start_values}')
print(f'Total Number of Nurses Hired: {total_nurses}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')