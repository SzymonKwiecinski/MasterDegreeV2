import pulp

# Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
Period = data['Period']
Demand = data['Demand']

# Initialize the problem
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(1, T + 1), lowBound=0, cat='Integer')  # Number of nurses starting on each day
N = pulp.LpVariable("N", lowBound=0, cat='Integer')  # Total number of nurses hired

# Objective Function
problem += N, "Total_Nurses_Hired"

# Constraints
# Total number of nurses is the sum of nurses starting on each day
problem += N == pulp.lpSum(x[j] for j in range(1, T + 1)), "Total_Nurses"

# Demand constraints for each day
for j in range(1, T + 1):
    problem += pulp.lpSum(x[(j - k - 1) % T + 1] for k in range(Period)) >= Demand[j - 1], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')