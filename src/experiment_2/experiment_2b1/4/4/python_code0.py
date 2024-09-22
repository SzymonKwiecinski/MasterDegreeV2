import pulp
import json

# Input data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Problem definition
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')

# Objective function: minimize the total number of nurses hired
problem += pulp.lpSum(start[j] for j in range(T))

# Constraints: ensure the demand for nurses is met for each day
for j in range(T):
    problem += (pulp.lpSum(start[(j-i) % T] for i in range(period)) >= demand[j]), f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare the output
total_nurses = pulp.value(problem.objective)
start_days = [pulp.value(start[j]) for j in range(T)]

# Output
output = {
    "start": start_days,
    "total": total_nurses
}

# Print the result
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')