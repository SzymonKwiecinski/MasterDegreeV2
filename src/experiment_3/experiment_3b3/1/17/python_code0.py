import pulp

# Data from JSON
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
TransactionRate = data['TransactionRate']
TaxRate = data['TaxRate']
K = data['K']

# Define the problem
problem = pulp.LpProblem("Stock_Selling_Optimization", pulp.LpMaximize)

# Decision variables
sell = [pulp.LpVariable(f'sell_{i}', 0, Bought[i], cat='Continuous') for i in range(N)]

# Objective function
problem += pulp.lpSum([FuturePrice[i] * (Bought[i] - sell[i]) for i in range(N)])

# Constraint 1: Net amount raised from selling shares must meet the requirement K
problem += pulp.lpSum([
    (CurrentPrice[i] * sell[i] * (1 - TransactionRate / 100))
    - (sell[i] * (CurrentPrice[i] - BuyPrice[i]) * TaxRate / 100) 
    for i in range(N)
]) >= K

# Constraint 2: The number of shares sold cannot exceed the number of shares bought
# Already implemented by bounds on decision variables

# Solve the problem
problem.solve()

# Output the solution
sell_values = [pulp.value(sell[i]) for i in range(N)]
solution = {"sell": sell_values}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')