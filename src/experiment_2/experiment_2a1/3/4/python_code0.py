import pulp
import json

# Input data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}

# Extracting values from the input data
T = data['T']
period = data['Period']
demand = data['Demand']

# Create the problem variable
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables: Number of nurses starting on each day
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')

# Objective function: Minimize the total number of nurses hired
problem += pulp.lpSum(start[j] for j in range(T)), "Total_Nurses"

# Constraints
for j in range(T):
    problem += pulp.lpSum(start[(j-i) % T] for i in range(period)) >= demand[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Collecting results
start_values = [int(start[j].varValue) for j in range(T)]
total_nurses = pulp.value(problem.objective)

# Output the results
output = {
    "start": start_values,
    "total": total_nurses
}

print(json.dumps(output))

print(f' (Objective Value): <OBJ>{total_nurses}</OBJ>')