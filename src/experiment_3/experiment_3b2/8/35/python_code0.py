import pulp
import json

# Load data
data = json.loads("{'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}")

# Parameters
N = len(data['price'])
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']

# Create the optimization problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", range(N), lowBound=0)
sellquantity = pulp.LpVariable.dicts("sellquantity", range(N), lowBound=0)
stock = pulp.LpVariable.dicts("stock", range(N + 1), lowBound=0)

# Objective Function
problem += pulp.lpSum(prices[n] * sellquantity[n] - costs[n] * buyquantity[n] - holding_cost * stock[n] for n in range(N))

# Constraints
problem += stock[0] == 0  # Initial stock condition

for n in range(1, N + 1):
    problem += stock[n] == stock[n - 1] + buyquantity[n - 1] - sellquantity[n - 1]  # Stock balance
    problem += stock[n] <= capacity  # Capacity constraint

problem += stock[N] == 0  # End condition

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')