import pulp

# Data from the provided JSON format
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

N = len(data['price'])  # Number of periods

# Create a linear programming problem
problem = pulp.LpProblem("WarehouseManagement", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", range(N), lowBound=0)  # Quantity bought
sellquantity = pulp.LpVariable.dicts("sellquantity", range(N), lowBound=0)  # Quantity sold
stock = pulp.LpVariable.dicts("stock", range(N + 1), lowBound=0)  # Stock levels

# Initial stock condition
problem += (stock[0] == 0)

# Objective Function
problem += pulp.lpSum(data['price'][n] * sellquantity[n] - data['cost'][n] * buyquantity[n] - data['holding_cost'] * stock[n] for n in range(N))

# Constraints
for n in range(N):
    # Stock balance constraint
    problem += (stock[n + 1] == stock[n] + buyquantity[n] - sellquantity[n])
    
    # Capacity constraint
    problem += (stock[n + 1] <= data['capacity'])

# Final stock condition
problem += (stock[N] == 0)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')