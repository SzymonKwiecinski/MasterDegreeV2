import pulp

# Data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
Capacity = data['capacity']
HoldingCost = data['holding_cost']
Price = data['price']
Cost = data['cost']
N = len(Price)

# Create LP problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = [pulp.LpVariable(f'B_{t}', lowBound=0, cat='Continuous') for t in range(N)]
S = [pulp.LpVariable(f'S_{t}', lowBound=0, cat='Continuous') for t in range(N)]
I = [pulp.LpVariable(f'I_{t}', lowBound=0, cat='Continuous') for t in range(N)]

# Objective Function
profit = pulp.lpSum([Price[t] * S[t] - Cost[t] * B[t] - HoldingCost * I[t] for t in range(N)])
problem += profit

# Constraints
# Initial inventory
initial_inventory_constraint = I[0] == 0
problem += initial_inventory_constraint

# Inventory balance constraints
for t in range(N):
    if t == 0:
        problem += I[t] == B[t] - S[t]  # Inventory balance for first period
    else:
        problem += I[t] == I[t-1] + B[t] - S[t]  # Inventory balance for other periods

# Capacity constraints
for t in range(N):
    problem += I[t] <= Capacity

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')