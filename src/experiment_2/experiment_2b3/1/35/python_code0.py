import pulp

# Data Input
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Extracting data elements
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']
N = len(prices)

# Creating a linear programming problem
problem = pulp.LpProblem("Warehouse_Stock_Optimization", pulp.LpMaximize)

# Defining decision variables
buy = [pulp.LpVariable(f"buy_{n}", lowBound=0) for n in range(N)]
sell = [pulp.LpVariable(f"sell_{n}", lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f"stock_{n}", lowBound=0) for n in range(N)]

# Objective function: Maximize profit
profit = pulp.lpSum([(prices[n] * sell[n] - costs[n] * buy[n] - holding_cost * stock[n]) for n in range(N)])
problem += profit

# Constraints
for n in range(N):
    if n == 0:
        problem += (stock[n] == buy[n] - sell[n]), f"StockBalance_0"
    else:
        problem += (stock[n] == stock[n-1] + buy[n] - sell[n]), f"StockBalance_{n}"

    # Capacity constraint
    problem += (stock[n] <= capacity), f"Capacity_{n}"

# Final stock should be zero at the end of last period
problem += (stock[N-1] == 0), "FinalStockZero"

# Solve the problem
problem.solve()

# Output format
output = {
    "buyquantity": [pulp.value(buy[n]) for n in range(N)],
    "sellquantity": [pulp.value(sell[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

# Print results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')