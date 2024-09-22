import pulp

# Data
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
N = len(data['price'])

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", range(N), lowBound=0, cat='Continuous')
sellquantity = pulp.LpVariable.dicts("SellQuantity", range(N), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("Stock", range(N+1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['price'][n] * sellquantity[n] - 
                      data['cost'][n] * buyquantity[n] - 
                      data['holding_cost'] * stock[n] for n in range(N))

# Constraints
problem += stock[0] == 0  # Initial stock
problem += stock[N] == 0  # Ending stock

for n in range(1, N+1):
    problem += stock[n] == stock[n-1] + buyquantity[n-1] - sellquantity[n-1]  # Stock balance

for n in range(N):
    problem += stock[n] <= data['capacity']  # Capacity constraint

# Solve
problem.solve()

# Output result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')