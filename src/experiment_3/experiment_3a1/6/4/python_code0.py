import pulp

# Data from the JSON format
T = 7  # Number of days
period = 4  # Consecutive days a nurse works
demand = [0, 5, 9, 15, 4, 7, 3]  # Demand for nurses on each day

# Create a linear programming problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision Variables
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')
total = pulp.LpVariable("total", lowBound=0, cat='Integer')

# Objective Function
problem += total

# Constraints
for j in range(T):
    problem += pulp.lpSum(start[(j - k) % T] for k in range(period)) >= demand[j]

# Total nurses hired
problem += total == pulp.lpSum(start[j] for j in range(T))

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')