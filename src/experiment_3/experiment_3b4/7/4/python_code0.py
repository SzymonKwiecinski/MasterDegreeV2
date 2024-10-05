import pulp

# Extracting data from the JSON format
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Define the problem
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Integer') for j in range(T)]

# Objective function: Minimize the total number of nurses
problem += pulp.lpSum(x), "Total_Nurses"

# Constraints
for j in range(T):
    problem += pulp.lpSum(x[(j-i-1) % T] for i in range(period)) >= demand[j], f"Demand_Day_{j+1}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')