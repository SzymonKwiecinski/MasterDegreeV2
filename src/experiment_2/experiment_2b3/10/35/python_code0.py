import pulp

# Data input
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Extracting data
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Define problem
problem = pulp.LpProblem("Warehouse_Profit_Maximization", pulp.LpMaximize)

# Decision variables
buyquantity = [pulp.LpVariable(f'buyquantity_{n}', lowBound=0, cat='Continuous') for n in range(N)]
sellquantity = [pulp.LpVariable(f'sellquantity_{n}', lowBound=0, cat='Continuous') for n in range(N)]
stock = [pulp.LpVariable(f'stock_{n}', lowBound=0, upBound=capacity, cat='Continuous') for n in range(N)]

# Objective function
profit = pulp.lpSum([price[n] * sellquantity[n] - cost[n] * buyquantity[n] - holding_cost * stock[n] for n in range(N)])
problem += profit

# Constraints
# Warehouse starts empty
problem += stock[0] == buyquantity[0] - sellquantity[0]

# Stock and flow balance for each period
for n in range(1, N):
    problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]

# Warehouse ends empty
problem += stock[N-1] == 0

# Solve problem
problem.solve()

# Extract results
results = {
    "buyquantity": [pulp.value(buyquantity[n]) for n in range(N)],
    "sellquantity": [pulp.value(sellquantity[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
results