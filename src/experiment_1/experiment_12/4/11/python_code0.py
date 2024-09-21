import pulp

# Data
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
problem += I[0] == 0

# Constraints for each period
for t in range(N):
    # Storage capacity constraint
    problem += I[t] <= Capacity
    # Inventory balance constraint
    if t > 0:
        problem += I[t] == I[t-1] + B[t] - S[t]

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')