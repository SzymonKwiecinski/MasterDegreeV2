import pulp
import json

# Data
data = {
    'N': 3,
    'Bought': [100, 150, 80],
    'BuyPrice': [50, 40, 30],
    'CurrentPrice': [60, 35, 32],
    'FuturePrice': [65, 44, 34],
    'TransactionRate': 1.0,
    'TaxRate': 15.0,
    'K': 5000
}

# Variables
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100
taxRate = data['TaxRate'] / 100
K = data['K']

# Problem definition
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0)

# Objective function
profit = pulp.lpSum((futurePrice[i] * bought[i] - buyPrice[i] * bought[i]) for i in range(N))
transaction_costs = pulp.lpSum(transactionRate * (currentPrice[i] * x[i]) for i in range(N))
taxes = pulp.lpSum(taxRate * (currentPrice[i] * x[i] - buyPrice[i] * x[i]) for i in range(N))

problem += profit - transaction_costs - taxes

# Constraints
# Total amount raised net of costs
total_net_sales = pulp.lpSum(
    (currentPrice[i] * x[i] * (1 - transactionRate) - taxRate * (currentPrice[i] * x[i] - buyPrice[i] * x[i]))
    for i in range(N)
)
problem += total_net_sales >= K

# Non-negativity constraints and limit on shares sold
for i in range(N):
    problem += x[i] <= bought[i]

# Solve the problem
problem.solve()

# Output the result
sell = [x[i].varValue for i in range(N)]
print(json.dumps({"sell": sell}))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')