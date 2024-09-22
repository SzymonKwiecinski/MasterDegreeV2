import pulp

# Data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}
N = len(data['price'])
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
buyquantity = [pulp.LpVariable(f'buyquantity_{n}', lowBound=0) for n in range(N)]
sellquantity = [pulp.LpVariable(f'sellquantity_{n}', lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f'stock_{n}', lowBound=0) for n in range(N)]

# Objective function
profit = pulp.lpSum([price[n] * sellquantity[n] - cost[n] * buyquantity[n] for n in range(N)]) \
         - holding_cost * pulp.lpSum([stock[n] for n in range(N)])
problem += profit, "Maximize Profit"

# Constraints
problem += (stock[0] == 0), "Initial Stock is Zero"
for n in range(N):
    if n > 0:
        problem += (stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n]), f"Stock Balance {n}"
    problem += (sellquantity[n] <= stock[n-1] + buyquantity[n]), f"Sell Quantity Less Than or Equals Available {n}"
    problem += (stock[n] <= capacity), f"Stock Capacity {n}"
problem += (stock[N-1] == 0), "Final Stock is Zero"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')