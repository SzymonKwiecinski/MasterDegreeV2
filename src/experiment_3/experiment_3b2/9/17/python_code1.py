import pulp

# Data from JSON format
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

# Parameters
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate']
taxRate = data['TaxRate']
K = data['K']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Expected_Future_Value", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0)

# Objective Function
problem += pulp.lpSum((bought[i] - sell[i]) * futurePrice[i] for i in range(N)), "Total_Expected_Future_Value"

# Constraints
# Net proceeds constraint
net_proceeds = pulp.lpSum(
    (1 - transactionRate / 100) * currentPrice[i] * sell[i] - 
    (taxRate / 100) * pulp.lpSum([pulp.lpMax(0, (currentPrice[i] - buyPrice[i]) * sell[i]) for i in range(N)])
)
problem += net_proceeds >= K, "Net_Proceeds_Constraint"

# Stock limits constraints
for i in range(N):
    problem += sell[i] <= bought[i], f"Stock_Limit_Constraint_{i}"
    problem += sell[i] >= 0, f"Non_Negativity_Constraint_{i}"

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')