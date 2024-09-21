import pulp

# Data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
N = len(data['price'])
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']

# Problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = [pulp.LpVariable(f'B_{t}', lowBound=0, cat='Continuous') for t in range(N)]
S = [pulp.LpVariable(f'S_{t}', lowBound=0, cat='Continuous') for t in range(N)]
I = [pulp.LpVariable(f'I_{t}', lowBound=0, cat='Continuous') for t in range(N)]

# Objective Function
profit = pulp.lpSum(prices[t] * S[t] - costs[t] * B[t] - holding_cost * I[t] for t in range(N))
problem += profit

# Constraints
for t in range(N):
    problem += I[t] <= capacity, f"Storage_Capacity_{t}"
    if t == 0:
        problem += I[t] == B[t] - S[t], f"Inventory_Balance_Initial_{t}"
    else:
        problem += I[t] == I[t-1] + B[t] - S[t], f"Inventory_Balance_{t}"

# Solve
problem.solve()

# Output Objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')