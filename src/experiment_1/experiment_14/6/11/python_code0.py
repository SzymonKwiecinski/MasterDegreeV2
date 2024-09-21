import pulp

# Data from provided JSON
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
Capacity = data['capacity']
HoldingCost = data['holding_cost']
Price = data['price']
Cost = data['cost']
N = len(Price)

# Create the LP problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = [pulp.LpVariable(f'B_{t}', lowBound=0, cat='Continuous') for t in range(N)]
S = [pulp.LpVariable(f'S_{t}', lowBound=0, cat='Continuous') for t in range(N)]
I = [pulp.LpVariable(f'I_{t}', lowBound=0, cat='Continuous') for t in range(N)]

# Objective Function
problem += pulp.lpSum([Price[t] * S[t] - Cost[t] * B[t] - HoldingCost * I[t] for t in range(N)])

# Constraints
for t in range(N):
    problem += I[t] <= Capacity, f'Storage_Capacity_{t}'

problem += I[0] == 0, "Initial Inventory"

for t in range(N):
    if t == 0:
        problem += I[t] == B[t] - S[t], f'Inventory_Balance_{t}'
    else:
        problem += I[t] == I[t-1] + B[t] - S[t], f'Inventory_Balance_{t}'

# Solve the problem
problem.solve()

# Print the optimal objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')