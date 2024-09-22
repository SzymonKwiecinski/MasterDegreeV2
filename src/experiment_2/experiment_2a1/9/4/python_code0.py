import pulp
import json

# Given data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Create the model
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')

# Constraints
for j in range(T):
    for k in range(period):
        if j + k < T:
            problem += (pulp.lpSum(start[(j - k) % T] for k in range(period)) >= demand[j]), f"Demand_Constraint_{j}"

# Objective function
problem += pulp.lpSum(start[j] for j in range(T))

# Solve the problem
problem.solve()

# Collect results
start_values = [int(start[j].varValue) for j in range(T)]
total_nurses = int(pulp.value(problem.objective))

# Output result
result = {
    "start": start_values,
    "total": total_nurses
}

print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')