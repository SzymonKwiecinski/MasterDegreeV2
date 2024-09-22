import pulp
import json

# Input Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Create the LP problem
problem = pulp.LpProblem("NurseScheduling", pulp.LpMinimize)

# Decision variables
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')

# Objective Function: Minimize the total number of nurses hired
problem += pulp.lpSum(start[j] for j in range(T)), "TotalNurses"

# Constraints
for j in range(T):
    # Each day's demand must be satisfied
    problem += pulp.lpSum(start[(j - k) % T] for k in range(period)) >= demand[j], f"Demand_{j}"

# Solve the problem
problem.solve()

# Output results
total_nurses = pulp.value(problem.objective)
start_values = [start[j].varValue for j in range(T)]

output = {
    "start": start_values,
    "total": total_nurses
}

# Print the objective
print(f' (Objective Value): <OBJ>{total_nurses}</OBJ>')