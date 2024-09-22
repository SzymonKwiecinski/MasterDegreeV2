import pulp

# Data from the provided JSON
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)  # Total number of periods

# Create the Linear Programming problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

# Define decision variables
buyquantity = [pulp.LpVariable(f'buyquantity_{n+1}', lowBound=0) for n in range(N)]
sellquantity = [pulp.LpVariable(f'sellquantity_{n+1}', lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f'stock_{n+1}', lowBound=0, upBound=capacity) for n in range(N)]

# Objective function
problem += pulp.lpSum(price[n] * sellquantity[n] - cost[n] * buyquantity[n] - holding_cost * stock[n] for n in range(N))

# Constraints
for n in range(N):
    if n == 0:
        problem += stock[n] == buyquantity[n] - sellquantity[n]  # First period
    else:
        problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]  # Stock balance for subsequent periods

    problem += stock[n] <= capacity  # Capacity constraint
    problem += stock[n] >= 0  # Non-negativity of stock

# Selling equals buying constraint
problem += pulp.lpSum(sellquantity[n] for n in range(N)) == pulp.lpSum(buyquantity[n] for n in range(N))

# Final stock constraint
problem += stock[N-1] == 0  # Stock at the end of the last period should be zero

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')