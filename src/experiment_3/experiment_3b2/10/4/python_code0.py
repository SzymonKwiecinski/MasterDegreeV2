import pulp

# Data from the JSON input
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Initialize the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("NursesStartingDay", range(1, T + 1), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum([x[j] for j in range(1, T + 1)]), "Total_Nurses"

# Constraints
for j in range(1, T + 1):
    problem += pulp.lpSum([x[(j - i - 1) % T + 1] for i in range(period)]) >= demand[j - 1], f"Demand_Constraint_Day_{j}"

# Solve the problem
problem.solve()

# Print the optimal objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')