import pulp

# Define the input data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}

# Extract data from the input
T = data['T']
period = data['Period']
demand = data['Demand']

# Create problem variable
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables
start = pulp.LpVariable.dicts("start", range(T), cat='Integer', lowBound=0)

# Objective function: Minimize the total number of nurses
problem += pulp.lpSum(start[j] for j in range(T)), "Total_Nurses"

# Constraints: Ensure the demand is met for each day
for j in range(T):
    problem += (pulp.lpSum(start[(j - k) % T] for k in range(period)) >= demand[j],
                f"Demand_Constraint_day_{j}")

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "start": [int(start[j].varValue) for j in range(T)],
    "total": int(pulp.value(problem.objective))
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')