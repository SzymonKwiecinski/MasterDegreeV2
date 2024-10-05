import pulp

# Parse the data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Initialize LP problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

# Define decision variables
buy_quantity = [pulp.LpVariable(f"buy_{n}", lowBound=0, cat='Continuous') for n in range(N)]
sell_quantity = [pulp.LpVariable(f"sell_{n}", lowBound=0, cat='Continuous') for n in range(N)]
stock = [pulp.LpVariable(f"stock_{n}", lowBound=0, upBound=capacity, cat='Continuous') for n in range(N)]

# Set the objective function
profit = pulp.lpSum([(price[n] * sell_quantity[n] - cost[n] * buy_quantity[n] - holding_cost * stock[n]) for n in range(N)])
problem += profit

# Add constraints
# Initial stock constraint
problem += stock[0] == buy_quantity[0] - sell_quantity[0]

# Stock balance constraints
for n in range(1, N):
    problem += stock[n] == stock[n-1] + buy_quantity[n] - sell_quantity[n]

# Final stock should be empty
problem += stock[N-1] == 0

# Solve the problem
problem.solve()

# Prepare the solution
solution = {
    "buyquantity": [pulp.value(buy_quantity[n]) for n in range(N)],
    "sellquantity": [pulp.value(sell_quantity[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')