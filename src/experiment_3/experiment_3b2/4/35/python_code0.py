import pulp

# Define the data from the provided JSON format
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Number of periods
N = len(data['price'])

# Create a linear programming problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("buyquantity", range(N), lowBound=0)
sellquantity = pulp.LpVariable.dicts("sellquantity", range(N), lowBound=0)
stock = pulp.LpVariable.dicts("stock", range(N), lowBound=0)

# Objective function
problem += pulp.lpSum(data['price'][n] * sellquantity[n] for n in range(N)) - \
           pulp.lpSum(data['cost'][n] * buyquantity[n] for n in range(N)) - \
           pulp.lpSum(data['holding_cost'] * stock[n] for n in range(N)), "Total_Profit"

# Constraints
# Stock balance and capacity constraints
for n in range(N):
    if n == 0:
        problem += stock[n] == buyquantity[n] - sellquantity[n], f"Stock_Balance_{n}"
    else:
        problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n], f"Stock_Balance_{n}"

    problem += stock[n] <= data['capacity'], f"Stock_Capacity_{n}"

# Ending stock constraint
problem += stock[N-1] == 0, "Ending_Stock"

# Solve the problem
problem.solve()

# Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')