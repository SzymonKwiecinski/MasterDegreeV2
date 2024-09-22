import pulp

# Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
p = data['Period']
demand = data['Demand']

# Create the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(1, T + 1), lowBound=0, cat='Integer')
N = pulp.LpVariable("N", lowBound=0, cat='Integer')

# Objective Function
problem += N

# Constraints
for j in range(1, T + 1):
    problem += pulp.lpSum(x[(j - i) % T + 1] for i in range(p)) >= demand[j - 1], f"Demand_Constraint_{j}"

# Total Nurses
problem += N == pulp.lpSum(x[j] for j in range(1, T + 1)), "Total_Nurses"

# Solve the problem
problem.solve()

# Output
start = [x[j].varValue for j in range(1, T + 1)]
total = pulp.value(N)

print(f' (Objective Value): <OBJ>{total}</OBJ>')
print(f'Start: {start}')