import pulp
import json

# Given data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Create the LP problem
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

# Decision variables: number of nurses starting on each day
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')

# Objective function: Minimize the total number of nurses hired
problem += pulp.lpSum([start[j] for j in range(T)])

# Constraints: Ensure demand is met for each day
for j in range(T):
    problem += pulp.lpSum([start[(j - k) % T] for k in range(period)]) >= demand[j]

# Solve the problem
problem.solve()

# Collect results
result_start = [start[j].varValue for j in range(T)]
total_nurses = pulp.value(problem.objective)

# Output results
output = {
    "start": result_start,
    "total": total_nurses
}

# Print objective value
print(f' (Objective Value): <OBJ>{total_nurses}</OBJ>')