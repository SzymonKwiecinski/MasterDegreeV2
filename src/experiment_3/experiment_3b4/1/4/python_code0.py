import pulp

# Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
Period = data['Period']
Demand = data['Demand']

# Initialize the problem
problem = pulp.LpProblem("Nurse_Night_Shift_Scheduling", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f"x_{j}", lowBound=0, cat='Integer') for j in range(1, T + 1)]

# Objective Function
problem += pulp.lpSum(x[j] for j in range(T)), "Total_Nurses"

# Constraints
for j in range(T):
    problem += (pulp.lpSum(x[(j-i-1) % T] for i in range(Period)) >= Demand[j]), f"Demand_day_{j+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')