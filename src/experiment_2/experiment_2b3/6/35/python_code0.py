import pulp

# Parse the input data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}

capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buy = [pulp.LpVariable(f"buy_{n}", lowBound=0) for n in range(N)]
sell = [pulp.LpVariable(f"sell_{n}", lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f"stock_{n}", lowBound=0) for n in range(N)]

# Objective function
profit = pulp.lpSum([(price[n] * sell[n] - cost[n] * buy[n] - holding_cost * stock[n]) for n in range(N)])
problem += profit

# Constraints

# Initial stock constraint (stock at time 0 is 0)
problem += (stock[0] == buy[0] - sell[0]), "Initial_Stock"

# Stock capacity constraint and flow balance for each period
for n in range(1, N):
    problem += (stock[n] == stock[n-1] + buy[n] - sell[n]), f"Stock_Balance_{n}"

# Capacity constraint
for n in range(N):
    problem += (stock[n] <= capacity), f"Capacity_Constraint_{n}"

# Ending stock must be zero
problem += (stock[N-1] == 0), "Ending_Stock"

# Solve the problem
problem.solve()

# Output the results
result = {
    "buyquantity": [pulp.value(buy[n]) for n in range(N)],
    "sellquantity": [pulp.value(sell[n]) for n in range(N)],
    "stock": [pulp.value(stock[n]) for n in range(N)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')