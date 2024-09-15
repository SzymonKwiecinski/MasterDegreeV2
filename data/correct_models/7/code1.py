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
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)

# Objective function
problem += pulp.lpSum((data['Bought'][i] - x[i]) * data['FuturePrice'][i] for i in range(data['N'])), "Total_Expected_Value"

# Constraints
# Non-negativity constraint is handled by the lowBound in the variable definition
for i in range(data['N']):
    problem += x[i] <= data['Bought'][i], f"Cannot_Sell_More_Than_Bought_{i}"

# Amount raised constraint
problem += (
    pulp.lpSum(
        x[i] * data['CurrentPrice'][i] - 
        x[i] * (data['CurrentPrice'][i] - data['BuyPrice'][i]) * (data['TaxRate'] / 100) - 
        x[i] * data['CurrentPrice'][i] * (data['TransactionRate'] / 100) 
        for i in range(data['N'])
    ) >= data['K'], "Amount_Raised_Constraint"
)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')