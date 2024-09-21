import pulp

# Data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Parameters
N = len(data['price'])
Capacity = data['capacity']
HoldingCost = data['holding_cost']
Price = data['price']
Cost = data['cost']

# Create the problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = pulp.LpVariable.dicts("B", range(N), lowBound=0)  # Buy quantities
S = pulp.LpVariable.dicts("S", range(N), lowBound=0)  # Sell quantities
I = pulp.LpVariable.dicts("I", range(N), lowBound=0, upBound=Capacity)  # Inventory levels

# Objective Function
profit = pulp.lpSum([Price[t] * S[t] - Cost[t] * B[t] - HoldingCost * I[t] for t in range(N)])
problem += profit

# Constraints
# Initial Inventory
problem += I[0] == 0

# Inventory Balance and other constraints
for t in range(N):
    if t > 0:
        problem += I[t] == I[t-1] + B[t] - S[t]
    problem += I[t] >= 0  # Non-negative inventory
    problem += S[t] >= 0  # Non-negative sales
    problem += B[t] >= 0  # Non-negative purchases
    problem += I[t] <= Capacity  # Storage capacity

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')