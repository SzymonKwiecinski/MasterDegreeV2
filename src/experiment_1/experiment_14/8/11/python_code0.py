import pulp

# Constants and data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

N = len(data['price'])
Capacity = data['capacity']
HoldingCost = data['holding_cost']
Price = data['price']
Cost = data['cost']

# Define the problem
problem = pulp.LpProblem("OptimalTradingStrategy", pulp.LpMaximize)

# Decision Variables
B = [pulp.LpVariable(f"B_{t}", lowBound=0, cat='Continuous') for t in range(N)]
S = [pulp.LpVariable(f"S_{t}", lowBound=0, cat='Continuous') for t in range(N)]
I = [pulp.LpVariable(f"I_{t}", lowBound=0, cat='Continuous') for t in range(N)]

# Objective Function
profit = pulp.lpSum([Price[t] * S[t] - Cost[t] * B[t] - HoldingCost * I[t] for t in range(N)])
problem += profit

# Constraints
for t in range(N):
    problem += I[t] <= Capacity, f"StorageCapacity_{t}"

problem += I[0] == B[0] - S[0], "InitialInventory"

for t in range(1, N):
    problem += I[t] == I[t-1] + B[t] - S[t], f"InventoryBalance_{t}"

# Solve the problem
problem.solve()

# Print the results
for t in range(N):
    print(f"Period {t+1}: Buy {B[t].varValue}, Sell {S[t].varValue}, Inventory {I[t].varValue}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')