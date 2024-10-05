import pulp

# Data
data = {
    'T': 7, 
    'Period': 4, 
    'Demand': [0, 5, 9, 15, 4, 7, 3]
}

T = data['T']
period = data['Period']
demand = data['Demand']

# Problem
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Integer') for j in range(T)]

# Objective Function
problem += pulp.lpSum(x[j] for j in range(T)), "Total_Nurses_Hired"

# Constraints
for j in range(T):
    problem += pulp.lpSum(x[(j - i) % T] for i in range(period)) >= demand[j], f"Demand_Constraint_day_{j+1}"

# Solve
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')