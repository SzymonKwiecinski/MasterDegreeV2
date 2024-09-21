import pulp

# Data from the JSON
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Number of periods
N = len(data['price'])

# Parameters
Capacity = data['capacity']
HoldingCost = data['holding_cost']
Price = data['price']
Cost = data['cost']

# Initialize the problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = pulp.LpVariable.dicts("B", range(N), lowBound=0, cat='Continuous')
S = pulp.LpVariable.dicts("S", range(N), lowBound=0, cat='Continuous')
I = pulp.LpVariable.dicts("I", range(N), lowBound=0, cat='Continuous')

# Objective Function
objective = pulp.lpSum([Price[t] * S[t] - Cost[t] * B[t] - HoldingCost * I[t] for t in range(N)])
problem += objective

# Constraints
# Initial inventory
problem += I[0] == 0

# Inventory balance, non-negativity, and capacity constraints
for t in range(N):
    if t > 0:
        problem += I[t] == I[t-1] + B[t] - S[t]
    problem += I[t] <= Capacity
    problem += S[t] >= 0
    problem += B[t] >= 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')