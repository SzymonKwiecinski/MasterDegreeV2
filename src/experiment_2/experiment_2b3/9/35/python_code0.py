import pulp

# Parse the input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']
N = len(prices)

# Create the optimization problem
problem = pulp.LpProblem("Warehouse_Operation_Maximize_Profit", pulp.LpMaximize)

# Decision variables
buyquantity = [pulp.LpVariable(f"buyquantity_{n}", lowBound=0) for n in range(N)]
sellquantity = [pulp.LpVariable(f"sellquantity_{n}", lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f"stock_{n}", lowBound=0) for n in range(N)]

# Objective function: Maximize Total Profit
profit = pulp.lpSum([prices[n] * sellquantity[n] - costs[n] * buyquantity[n] - holding_cost * stock[n] for n in range(N)])
problem += profit

# Constraints
for n in range(N):
    # Capacity constraint
    problem += (stock[n] <= capacity, f"Capacity_Constraint_{n}")

    # Stock balance equations
    if n == 0:
        problem += (stock[n] == buyquantity[n] - sellquantity[n], f"Stock_Balance_{n}")
    else:
        problem += (stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n], f"Stock_Balance_{n}")

# Final stock must be zero at the end of the last period
problem += (stock[N-1] == 0, f"Final_Stock_Constraint")

# Solve the problem
problem.solve()

# Collect results
result = {
    "buyquantity": [pulp.value(buyquantity[n]) for n in range(N)],
    "sellquantity": [pulp.value(sellquantity[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')