import pulp

# Parse the input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']
N = len(prices)

# Define the problem
problem = pulp.LpProblem("Warehouse_Stock_Optimization", pulp.LpMaximize)

# Decision variables
buyquantity = [pulp.LpVariable(f"buyquantity_{n}", lowBound=0) for n in range(N)]
sellquantity = [pulp.LpVariable(f"sellquantity_{n}", lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f"stock_{n}", lowBound=0, upBound=capacity) for n in range(N)]

# Objective function: Maximize profit
profit = pulp.lpSum([
    (prices[n] * sellquantity[n]) - (costs[n] * buyquantity[n]) - (holding_cost * stock[n])
    for n in range(N)
])
problem += profit

# Constraints
# Stock balance constraints
problem += stock[0] == buyquantity[0] - sellquantity[0], "Initial_Stock"
for n in range(1, N):
    problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n], f"Stock_Balance_{n}"

# Warehouse begins and ends empty
problem += stock[-1] == 0, "Final_Stock_Zero"

# Solve the problem
problem.solve()

# Extract results
output = {
    "buyquantity": [pulp.value(buyquantity[n]) for n in range(N)],
    "sellquantity": [pulp.value(sellquantity[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')