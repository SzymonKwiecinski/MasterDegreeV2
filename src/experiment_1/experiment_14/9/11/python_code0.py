import pulp

# Data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Parameters
Capacity = data['capacity']
HoldingCost = data['holding_cost']
Price = data['price']
Cost = data['cost']
N = len(Price)  # Number of periods

# Problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = pulp.LpVariable.dicts("B", range(N), lowBound=0, cat='Continuous')
S = pulp.LpVariable.dicts("S", range(N), lowBound=0, cat='Continuous')
I = pulp.LpVariable.dicts("I", range(N), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([Price[t] * S[t] - Cost[t] * B[t] - HoldingCost * I[t] for t in range(N)])

# Constraints

# Initial inventory
problem += I[0] == 0, "Initial_Inventory"

# Inventory balance constraints
for t in range(N):
    if t == 0:
        problem += I[t] == B[t] - S[t], f"Inventory_Balance_{t}"
    else:
        problem += I[t] == I[t-1] + B[t] - S[t], f"Inventory_Balance_{t}"

# Storage capacity constraints
for t in range(N):
    problem += I[t] <= Capacity, f"Storage_Capacity_{t}"

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')