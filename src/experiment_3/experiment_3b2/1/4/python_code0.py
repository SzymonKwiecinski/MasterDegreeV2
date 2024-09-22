import pulp

# Data from the JSON input
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
Period = data['Period']
Demand = data['Demand']

# Create the LP problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision Variables
start = pulp.LpVariable.dicts("start", range(1, T + 1), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(start[j] for j in range(1, T + 1)), "Total_Nurses_Hired"

# Constraints
for j in range(1, T + 1):
    problem += (
        pulp.lpSum(start[(j - i - 1) % T + 1] for i in range(Period)) >= Demand[j - 1],
        f"Demand_Constraint_{j}"
    )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')