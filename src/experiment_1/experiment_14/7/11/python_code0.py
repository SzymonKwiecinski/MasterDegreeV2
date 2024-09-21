import pulp

# Data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Constants
Capacity = data['capacity']
HoldingCost = data['holding_cost']
Prices = data['price']
Costs = data['cost']
N = len(Prices)

# Problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = [pulp.LpVariable(f'B_{t}', lowBound=0, cat='Continuous') for t in range(N)]
S = [pulp.LpVariable(f'S_{t}', lowBound=0, cat='Continuous') for t in range(N)]
I = [pulp.LpVariable(f'I_{t}', lowBound=0, cat='Continuous') for t in range(N)]

# Objective Function
problem += pulp.lpSum([Prices[t] * S[t] - Costs[t] * B[t] - HoldingCost * I[t] for t in range(N)])

# Constraints

# Initial inventory
problem += (I[0] == 0)

# Inventory balance and capacity constraints
for t in range(N):
    if t == 0:
        problem += (I[t] == B[t] - S[t])
    else:
        problem += (I[t] == I[t - 1] + B[t] - S[t])
    problem += (I[t] <= Capacity)

# Solve
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')