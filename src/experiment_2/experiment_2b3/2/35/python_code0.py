import pulp

# Load data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

# Extract data
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buyquantity = [pulp.LpVariable(f"buyquantity_{n}", lowBound=0) for n in range(N)]
sellquantity = [pulp.LpVariable(f"sellquantity_{n}", lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f"stock_{n}", lowBound=0) for n in range(N)]

# Objective function: Maximize total profit
objective = pulp.lpSum((price[n] * sellquantity[n] - cost[n] * buyquantity[n] - holding_cost * stock[n]) for n in range(N))
problem += objective

# Constraints
for n in range(N):
    if n == 0:
        problem += stock[n] == buyquantity[n] - sellquantity[n]
    else:
        problem += stock[n] == stock[n - 1] + buyquantity[n] - sellquantity[n] - holding_cost * stock[n]
    problem += stock[n] <= capacity

# Final stock constraint: end with zero stock
problem += stock[N - 1] == 0

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