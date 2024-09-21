import pulp

# Data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Parameters
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = [pulp.LpVariable(f'B_{t}', lowBound=0, cat='Continuous') for t in range(N)]
S = [pulp.LpVariable(f'S_{t}', lowBound=0, cat='Continuous') for t in range(N)]
I = [pulp.LpVariable(f'I_{t}', lowBound=0, cat='Continuous') for t in range(N)]

# Objective Function
problem += pulp.lpSum([(price[t] * S[t] - cost[t] * B[t] - holding_cost * I[t]) for t in range(N)])

# Constraints
I_0 = 0  # Initial inventory
for t in range(N):
    if t == 0:
        problem += (I[t] == I_0 + B[t] - S[t], f'Inventory_Balance_{t}')
    else:
        problem += (I[t] == I[t-1] + B[t] - S[t], f'Inventory_Balance_{t}')
    problem += (I[t] <= capacity, f'Storage_Capacity_{t}')

# Solving the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')