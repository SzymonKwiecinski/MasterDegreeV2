import pulp

# Given data
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

# Extract the data
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100.0
taxRate = data['TaxRate'] / 100.0
K = data['K']

# Define the LP problem
problem = pulp.LpProblem("Maximize_Expected_Portfolio_Value", pulp.LpMaximize)

# Define decision variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0)

# Objective function: maximize expected value of portfolio next year
expected_value = sum((bought[i] - sell[i]) * futurePrice[i] for i in range(N))
problem += expected_value

# Constraint: net cash from sales should be at least K
net_cash = sum((sell[i] * currentPrice[i] * (1 - transactionRate) - 
                taxRate * (sell[i] * currentPrice[i] - sell[i] * buyPrice[i])) 
               for i in range(N))
problem += net_cash >= K

# Constraint: can't sell more than bought
for i in range(N):
    problem += sell[i] <= bought[i]

# Solve the problem
problem.solve()

# Organize results
solution = {
    "sell": [sell[i].varValue for i in range(N)]
}

# Print solution
print(solution)

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')