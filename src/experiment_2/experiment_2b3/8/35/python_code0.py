import pulp

# Parse the input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buyquantity = [pulp.LpVariable(f"Buy_Quantity_{n}", lowBound=0) for n in range(N)]
sellquantity = [pulp.LpVariable(f"Sell_Quantity_{n}", lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f"Stock_{n}", lowBound=0) for n in range(N)]

# Objective function
profit = pulp.lpSum([(price[n] * sellquantity[n] - cost[n] * buyquantity[n] - holding_cost * stock[n]) for n in range(N)])
problem += profit

# Constraints
problem += (stock[0] == buyquantity[0] - sellquantity[0])

for n in range(1, N):
    problem += (stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n])

for n in range(N):
    problem += (stock[n] <= capacity)

problem += (stock[N-1] == 0)

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "buyquantity": [pulp.value(buyquantity[n]) for n in range(N)],
    "sellquantity": [pulp.value(sellquantity[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')