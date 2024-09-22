import pulp

# Extract data from JSON
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

capacity = data["capacity"]
holding_cost = data["holding_cost"]
prices = data["price"]
costs = data["cost"]
N = len(prices)

# Define the problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

# Define decision variables
buyquantity = [pulp.LpVariable(f"buyquantity_{n}", lowBound=0) for n in range(N)]
sellquantity = [pulp.LpVariable(f"sellquantity_{n}", lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f"stock_{n}", lowBound=0) for n in range(N)]

# Objective function: Maximize profit
profit = pulp.lpSum([(prices[n] * sellquantity[n] - costs[n] * buyquantity[n] - holding_cost * stock[n]) for n in range(N)])
problem += profit

# Constraints
# Initial stock is zero
problem += (stock[0] == buyquantity[0] - sellquantity[0])

# Stock balance constraints for subsequent periods
for n in range(1, N):
    problem += (stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n])

# Final stock must be zero
problem += (stock[N-1] == 0)

# Capacity constraints for each period
for n in range(N):
    problem += (stock[n] <= capacity)

# Solve the problem
problem.solve()

# Print results
output = {
    "buyquantity": [pulp.value(buyquantity[n]) for n in range(N)],
    "sellquantity": [pulp.value(sellquantity[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

print(output)
print(f"(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")