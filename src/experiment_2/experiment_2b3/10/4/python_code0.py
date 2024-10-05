import pulp

# Data input from the JSON format
data = {
    'T': 7, 
    'Period': 4, 
    'Demand': [0, 5, 9, 15, 4, 7, 3]
}

# Extracting data from the input
T = data['T']
period = data['Period']
demand = data['Demand']

# Initialize the problem
problem = pulp.LpProblem("Nurse_Shift_Scheduling", pulp.LpMinimize)

# Decision variables: start_j for each day j
start = [pulp.LpVariable(f'start_{j}', lowBound=0, cat='Integer') for j in range(T)]

# Objective function: minimize total number of nurses
problem += pulp.lpSum(start), "Total_Nurses"

# Constraints: demand for each day j
for j in range(T):
    problem += pulp.lpSum(start[(j - i) % T] for i in range(period)) >= demand[j], f"Demand_day_{j+1}"

# Solve the problem
problem.solve()

# Prepare output
result = {
    "start": [int(start[j].varValue) for j in range(T)],
    "total": int(pulp.value(problem.objective))
}

# Print the result
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')