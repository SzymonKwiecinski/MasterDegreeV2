import pulp

# Data from the provided JSON format
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

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", range(data['N']), lowBound=0)

# Objective function
problem += pulp.lpSum(
    (data['Bought'][i] - sell[i]) * data['FuturePrice'][i] for i in range(data['N'])
), "Total Portfolio Value"

# Constraints
problem += (
    pulp.lpSum(
        sell[i] * data['CurrentPrice'][i] - 
        (data['TaxRate'] / 100) * pulp.lpSum(
            pulp.lpMax(0, (sell[i] * data['CurrentPrice'][i] - sell[i] * data['BuyPrice'][i])) for i in range(data['N'])
        ) - 
        (data['TransactionRate'] / 100) * sell[i] * data['CurrentPrice'][i]
        for i in range(data['N'])) 
    ) >= data['K'], "NetAmountRaised"
)

for i in range(data['N']):
    problem += (sell[i] <= data['Bought'][i], f"MaxSell_{i}")

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')