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
Price = data['price']
Cost = data['cost']
N = len(Price)

# Problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = pulp.LpVariable.dicts("B", range(N), lowBound=0, cat='Continuous')
S = pulp.LpVariable.dicts("S", range(N), lowBound=0, cat='Continuous')
I = pulp.LpVariable.dicts("I", range(N), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([Price[t] * S[t] - Cost[t] * B[t] - HoldingCost * I[t] for t in range(N)])

# Constraints
for t in range(N):
    problem += I[t] <= Capacity, f"StorageCapacityConstraint_{t}"

    if t == 0:
        problem += I[t] == B[t] - S[t], f"InitialInventoryBalance_{t}"
    else:
        problem += I[t] == I[t-1] + B[t] - S[t], f"InventoryBalance_{t}"

# Solve the problem
problem.solve()

# Print the results
print(f"Optimal Profit (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")

for t in range(N):
    print(f"Period {t + 1}: Buy {B[t].varValue}, Sell {S[t].varValue}, Inventory {I[t].varValue}")