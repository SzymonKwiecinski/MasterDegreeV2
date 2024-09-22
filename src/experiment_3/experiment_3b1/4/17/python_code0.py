import pulp

# Given Data
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

# Number of stocks
N = data['N']

# Create a linear programming problem
problem = pulp.LpProblem("Stock_Selling_Optimization", pulp.LpMaximize)

# Define decision variables
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0)

# Objective Function: Maximize expected value of the portfolio next year
problem += pulp.lpSum(data['FuturePrice'][i] * (data['Bought'][i] - sell[i]) for i in range(N)), "Expected_Value"

# Constraint: Total amount raised after costs should be at least K
problem += (
    pulp.lpSum(
        (data['CurrentPrice'][i] * sell[i] * (1 - data['TransactionRate'] / 100) -
         ((data['CurrentPrice'][i] - data['BuyPrice'][i]) * sell[i] * (data['TaxRate'] / 100)))
        for i in range(N)
    ) >= data['K'], "Minimum_Amount_Raised"
)

# Constraints: The number of shares sold cannot exceed the number of shares bought
for i in range(N):
    problem += sell[i] <= data['Bought'][i], f"Max_Sell_{i}"
    problem += sell[i] >= 0, f"Min_Sell_{i}"

# Solve the problem
problem.solve()

# Output the results
results = {f'sell_{i}': pulp.value(sell[i]) for i in range(N)}
print(f'Optimal shares to sell: {results}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')