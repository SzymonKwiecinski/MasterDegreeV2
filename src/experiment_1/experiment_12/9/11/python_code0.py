import pulp

# Data provided from the JSON format
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Unpacking the data
Capacity = data['capacity']
HoldingCost = data['holding_cost']
Price = data['price']
Cost = data['cost']
N = len(Price)

# Creating the Linear Programming problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = pulp.LpVariable.dicts("Bought", range(N), lowBound=0, cat='Continuous')
S = pulp.LpVariable.dicts("Sold", range(N), lowBound=0, cat='Continuous')
I = pulp.LpVariable.dicts("Inventory", range(N), lowBound=0, cat='Continuous')

# Objective Function: Maximize Profit
problem += pulp.lpSum(Price[t] * S[t] - Cost[t] * B[t] - HoldingCost * I[t] for t in range(N))

# Constraints
# Initial Inventory
problem += I[0] == 0

# For each period t
for t in range(N):
    # Inventory balance constraint
    if t == 0:
        problem += I[t] == B[t] - S[t]
    else:
        problem += I[t] == I[t - 1] + B[t] - S[t]
    # Inventory capacity constraint
    problem += I[t] <= Capacity

# Solving the problem
problem.solve()

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')