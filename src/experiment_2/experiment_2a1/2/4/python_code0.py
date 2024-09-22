import pulp
import json

# Input data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}

# Problem parameters
T = data['T']
period = data['Period']
demand = data['Demand']

# Create the problem
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

# Decision variables: start[j] is the number of nurses starting their shift on day j
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')

# Objective function: Minimize the total number of nurses hired
problem += pulp.lpSum(start[j] for j in range(T)), "Total_Nurses_Hired"

# Constraints: Ensure the demand is met for each day
for j in range(T):
    problem += (pulp.lpSum(start[(j - k) % T] for k in range(period)) >= demand[j]), f"Demand_Constraint_Day_{j}"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "start": [int(start[j].varValue) for j in range(T)],
    "total": int(pulp.value(problem.objective))
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')