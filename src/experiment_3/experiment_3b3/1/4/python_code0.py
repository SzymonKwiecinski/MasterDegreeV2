import pulp

# Data provided
data = {
    'T': 7,
    'Period': 4,
    'Demand': [0, 5, 9, 15, 4, 7, 3]
}

# Extract data
T = data['T']
period = data['Period']
demand = data['Demand']

# Initialize the problem
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

# Decision Variables
start_vars = [pulp.LpVariable(f'start_{j}', lowBound=0, cat='Integer') for j in range(T)]
total_nurses = pulp.LpVariable('total_nurses', lowBound=0, cat='Integer')

# Objective Function
problem += total_nurses, "Minimize total number of nurses"

# Total nurses constraint
problem += total_nurses == pulp.lpSum(start_vars), "Total nurses constraint"

# Constraints for each day
for j in range(T):
    problem += pulp.lpSum(start_vars[(j-i) % T] for i in range(period)) >= demand[j], f"Demand_constraint_day_{j+1}"

# Solve the problem
problem.solve()

# Output results
start_values = [pulp.value(var) for var in start_vars]
total_nurses_hired = pulp.value(total_nurses)

print("Number of nurses starting each day:", start_values)
print("Total number of nurses hired:", total_nurses_hired)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')