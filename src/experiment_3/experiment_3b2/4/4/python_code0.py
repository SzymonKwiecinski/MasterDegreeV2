import pulp

# Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
Period = data['Period']
Demand = data['Demand']

# Create the problem
problem = pulp.LpProblem("Minimize_X", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(1, T + 1), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(x[j] for j in range(1, T + 1)), "Total_Production"

# Constraints
for j in range(1, T + 1):
    problem += (pulp.lpSum(x[(j - k - 1) % T + 1] for k in range(Period)) >= Demand[j - 1]), f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')