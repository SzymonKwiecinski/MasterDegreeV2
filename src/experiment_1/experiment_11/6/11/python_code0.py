import pulp

# Data from the provided JSON
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

N = len(data['price'])  # Number of periods

# Create the problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = pulp.LpVariable.dicts("B", range(N), lowBound=0)  # Quantity bought in period t
S = pulp.LpVariable.dicts("S", range(N), lowBound=0)  # Quantity sold in period t
I = pulp.LpVariable.dicts("I", range(N), lowBound=0, upBound=data['capacity'])  # Inventory level at end of period t

# Objective Function
problem += pulp.lpSum(data['price'][t] * S[t] - data['cost'][t] * B[t] - data['holding_cost'] * I[t] for t in range(N))

# Constraints
# Initial inventory
problem += I[0] == 0

# Inventory balance and constraints for each period
for t in range(N):
    if t > 0:
        problem += I[t] == I[t-1] + B[t] - S[t]
    problem += I[t] >= 0  # Non-negative inventory
    problem += S[t] >= 0  # Non-negative sales
    problem += B[t] >= 0  # Non-negative purchases
    problem += I[t] <= data['capacity']  # Storage capacity

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')