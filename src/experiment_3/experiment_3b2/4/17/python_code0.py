import pulp
import json

# Data provided in JSON format
data_json = '''{'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}'''
data = json.loads(data_json.replace("'", "\""))

# Parameters
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate']
tax_rate = data['TaxRate']
K = data['K']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0)

# Objective function
problem += pulp.lpSum((bought[i] - x[i]) * future_price[i] for i in range(N))

# Constraints
problem += pulp.lpSum((x[i] * current_price[i] * (1 - transaction_rate / 100) - 
                     pulp.max(0, x[i] * current_price[i] - bought[i] * buy_price[i]) * (tax_rate / 100))
                     for i in range(N)) == K

# Bound constraints
for i in range(N):
    problem += x[i] <= bought[i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')