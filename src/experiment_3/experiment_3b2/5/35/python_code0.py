import pulp
import json

data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')

# Extracting parameters from the data
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']
N = len(prices)

# Create the linear programming problem
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", range(1, N + 1), lowBound=0)
sellquantity = pulp.LpVariable.dicts("sellquantity", range(1, N + 1), lowBound=0)
stock = pulp.LpVariable.dicts("stock", range(1, N + 1), lowBound=0, upBound=capacity)

# Objective Function
problem += pulp.lpSum(prices[n - 1] * sellquantity[n] - costs[n - 1] * buyquantity[n] - holding_cost * stock[n] for n in range(1, N + 1))

# Constraints
problem += (stock[1] == buyquantity[1] - sellquantity[1], "Initial_Stock_Condition")

for n in range(2, N + 1):
    problem += (stock[n] == stock[n - 1] + buyquantity[n] - sellquantity[n], f"Stock_Balance_{n}")

problem += (stock[N] == 0, "Final_Stock_Condition")

for n in range(1, N + 1):
    problem += (stock[n] >= 0, f"Non_Negative_Stock_{n}")
    problem += (stock[n] <= capacity, f"Capacity_Constraint_{n}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')