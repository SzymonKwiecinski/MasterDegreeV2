import pulp

# Data from JSON
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Create the Problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision Variables
start = pulp.LpVariable.dicts("start", range(1, T + 1), lowBound=0, cat='Integer')
total = pulp.LpVariable("total", lowBound=0, cat='Integer')

# Objective Function
problem += total, "Minimize_total_nurses_hired"

# Constraints
for j in range(1, T + 1):
    problem += (
        pulp.lpSum(start[i] for i in range(max(1, j - period + 1), j + 1)) >= demand[j - 1],
        f"Demand_Constraint_day_{j}"
    )

# Set the total variable
problem += total == pulp.lpSum(start[j] for j in range(1, T + 1)), "Total_nurses_hired"

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')