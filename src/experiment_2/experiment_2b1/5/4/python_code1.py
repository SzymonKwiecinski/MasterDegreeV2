import pulp
import json

# Input data
data = json.loads('{"T": 7, "Period": 4, "Demand": [0, 5, 9, 15, 4, 7, 3]}')

# Extract data
T = data['T']  # Total days
period = data['Period']  # Nurse working period
demand = data['Demand']  # Demand for nurses each day

# Create the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables: start_j represents the number of nurses starting their period on day j
start = [pulp.LpVariable(f'start_{j}', lowBound=0, cat='Integer') for j in range(T)]

# Objective function: minimize the total number of nurses hired
problem += pulp.lpSum(start), "Minimize_Nurses"

# Constraints: ensuring that the demand is met for each day
for j in range(T):
    # Calculate the number of nurses available on day j
    problem += (pulp.lpSum(start[(j - k) % T] for k in range(period)) >= demand[j]), f'Demand_Constraint_{j}'

# Solve the problem
problem.solve()

# Prepare the output
start_values = [int(start[j].value()) for j in range(T)]
total_nurses = sum(start_values)

output = {
    "start": start_values,
    "total": total_nurses
}

# Print the output and the objective value
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')