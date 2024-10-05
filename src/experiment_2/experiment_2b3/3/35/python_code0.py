import pulp

# Parse the input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
capacity = data["capacity"]
holding_cost = data["holding_cost"]
prices = data["price"]
costs = data["cost"]

N = len(prices)

# Create the LP Maximization problem
problem = pulp.LpProblem("Warehouse_Profit_Maximization", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", range(N), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("SellQuantity", range(N), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("Stock", range(N), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
objective_terms = [sellquantity[n] * prices[n] - buyquantity[n] * costs[n] - stock[n] * holding_cost for n in range(N)]
problem += pulp.lpSum(objective_terms)

# Constraints
# Initial stock is 0
problem += stock[0] == buyquantity[0] - sellquantity[0]

# Stock constraints for subsequent periods
for n in range(1, N):
    problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]

# Capacity constraints for each period
for n in range(N):
    problem += stock[n] <= capacity

# Final stock must be 0
problem += stock[N-1] == 0

# Solve the problem
problem.solve()

# Collect the results
result = {
    "buyquantity": [pulp.value(buyquantity[n]) for n in range(N)],
    "sellquantity": [pulp.value(sellquantity[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')