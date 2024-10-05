import pulp

# Data from the JSON input
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

N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
transaction_rate = data['TransactionRate'] / 100
tax_rate = data['TaxRate'] / 100
K = data['K']

# Setting up the problem
problem = pulp.LpProblem("Maximize_Expected_Portfolio_Value", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0)

# Objective Function: Maximize expected value of portfolio next year
problem += pulp.lpSum((Bought[i] - sell[i]) * FuturePrice[i] for i in range(N))

# Constraints
problem += pulp.lpSum((sell[i] * CurrentPrice[i] - 
                        (sell[i] * BuyPrice[i]) * tax_rate - 
                        (sell[i] * CurrentPrice[i]) * transaction_rate) 
                      for i in range(N)) >= K, "Raise_Money_Constraint"

# Solve the problem
problem.solve()

# Prepare the output
solution = {
    "sell": [pulp.value(sell[i]) for i in range(N)],
}

print(solution)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')