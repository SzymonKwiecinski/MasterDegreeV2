import pulp
import json

# Input data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
period = data['Period']
demand = data['Demand']

# Create the problem variable
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables: number of nurses starting their shift on each day
start = [pulp.LpVariable(f'start_{j}', lowBound=0, cat='Integer') for j in range(data['T'])]

# Objective function: minimize the total number of nurses hired
problem += pulp.lpSum(start), "Total_Nurses"

# Constraints: satisfy demand for each day
for j in range(data['T']):
    problem += (pulp.lpSum(start[(j - k) % data['T']] for k in range(period)) >= demand[j]), f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "start": [int(start[j].varValue) for j in range(data['T'])],
    "total": int(pulp.value(problem.objective))
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')