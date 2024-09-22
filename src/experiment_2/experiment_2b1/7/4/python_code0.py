import json
import pulp

# Input data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
period = data['Period']
demand = data['Demand']

# Create the linear programming problem
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

# Decision variables: start_j for each day j
start = pulp.LpVariable.dicts("start", range(1, 8), lowBound=0, cat='Integer')

# Objective function: minimize the total number of nurses hired
problem += pulp.lpSum(start[j] for j in range(1, 8)), "Total_Nurses"

# Constraints: ensuring that the demand is met for each day
for j in range(1, 8):
    problem += pulp.lpSum(start[(j - i) % 7 + 1] for i in range(period) if (j - i) % 7 + 1 >= 1) >= demand[j - 1], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Extracting the results
nurses_start = [int(start[j].varValue) for j in range(1, 8)]
total_nurses = int(pulp.value(problem.objective))

# Prepare output
output = {
    "start": nurses_start,
    "total": total_nurses
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')