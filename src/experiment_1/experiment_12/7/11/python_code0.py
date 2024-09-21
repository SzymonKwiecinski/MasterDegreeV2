import pulp

# Parameters
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
Capacity = data['capacity']
HoldingCost = data['holding_cost']
Price = data['price']
Cost = data['cost']
N = len(Price)

# Problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = [pulp.LpVariable(f'B_{t}', lowBound=0) for t in range(N)]
S = [pulp.LpVariable(f'S_{t}', lowBound=0) for t in range(N)]
I = [pulp.LpVariable(f'I_{t}', lowBound=0) for t in range(N)]

# Objective Function
problem += pulp.lpSum([Price[t] * S[t] - Cost[t] * B[t] - HoldingCost * I[t] for t in range(N)])

# Constraints
for t in range(N):
    # Storage capacity
    problem += I[t] <= Capacity
    
    # Inventory balance
    if t == 0:
        problem += I[t] == B[t] - S[t]
    else:
        problem += I[t] == I[t - 1] + B[t] - S[t]

# Solve
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')