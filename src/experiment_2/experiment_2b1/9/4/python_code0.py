import json
import pulp

# Input data
data = json.loads('{"T": 7, "Period": 4, "Demand": [0, 5, 9, 15, 4, 7, 3]}')
T = data['T']
period = data['Period']
demand = data['Demand']

# Define the problem
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

# Define decision variables
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')

# Define the objective function
problem += pulp.lpSum(start[j] for j in range(T)), "Total_Nurses"

# Constraints
for j in range(T):
    for k in range(period):
        if j + k < T:
            problem += pulp.lpSum(start[j+k] for j in range(max(0, j - period + 1), min(T, j + 1))) >= demand[j], f"Demand_Constraint_Day_{j+1}")

# Solve the problem
problem.solve()

# Prepare the output
result_start = [int(start[j].value()) for j in range(T)]
total_nurses = int(pulp.value(problem.objective))

# Output result
output = {
    "start": result_start,
    "total": total_nurses
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')