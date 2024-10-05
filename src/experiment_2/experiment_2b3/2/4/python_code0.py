import pulp

# Load data from json
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}

T = data['T']
period = data['Period']
demand = data['Demand']

# Define the MILP problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Define the decision variables for the number of nurses starting each day
start = [pulp.LpVariable(f'start_{j}', lowBound=0, cat='Integer') for j in range(T)]

# Objective function: Minimize the total number of nurses
problem += pulp.lpSum(start), "Total_Nurses"

# Constraints: Meeting the demand for each day based on the nurses starting
for j in range(T):
    constraint_expr = sum(start[(j - k) % T] for k in range(period))
    problem += constraint_expr >= demand[j], f"Demand_on_day_{j+1}"

# Solve the problem
problem.solve()

# Gather results
result = {
    "start": [int(start[j].varValue) for j in range(T)],
    "total": int(pulp.value(problem.objective))
}

print("Solution: ", result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')