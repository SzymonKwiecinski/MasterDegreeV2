import pulp

# Input data
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

# Extracting data
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100
taxRate = data['TaxRate'] / 100
K = data['K']

# Define the LP problem
problem = pulp.LpProblem("Stock_Portfolio_Optimization", pulp.LpMaximize)

# Decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i], cat='Continuous') for i in range(N)]

# Objective: Maximize the expected future value of the portfolio
objective_terms = [(bought[i] - sell[i]) * futurePrice[i] for i in range(N)]
problem += pulp.lpSum(objective_terms)

# Constraint: Net proceeds constraint
net_proceeds_terms = [(sell[i] * currentPrice[i]) * (1 - transactionRate) - 
                      ((sell[i] * currentPrice[i]) - (sell[i] * buyPrice[i])) * taxRate 
                      for i in range(N)]
problem += pulp.lpSum(net_proceeds_terms) >= K

# Solve the problem
problem.solve()

# Extract the results
solution = {'sell': [pulp.value(sell[i]) for i in range(N)]}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')