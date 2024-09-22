import pulp
import json

# Given data
data_json = '''{
    "N": 3,
    "Bought": [100, 150, 80],
    "BuyPrice": [50, 40, 30],
    "CurrentPrice": [60, 35, 32],
    "FuturePrice": [65, 44, 34],
    "TransactionRate": 1.0,
    "TaxRate": 15.0,
    "K": 5000
}'''

data = json.loads(data_json)

# Extracting data from JSON
N = data['N']
Bought = data['Bought']
BuyPrice = data['BuyPrice']
CurrentPrice = data['CurrentPrice']
FuturePrice = data['FuturePrice']
TransactionRate = data['TransactionRate']
TaxRate = data['TaxRate']
K = data['K']

# Create the linear programming problem
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("Sell", range(N), lowBound=0)

# Objective Function
problem += pulp.lpSum((FuturePrice[i] - CurrentPrice[i]) * (Bought[i] - sell[i]) for i in range(N)), "Total_Expected_Value"

# Constraints
# Constraint for raising enough money
problem += (pulp.lpSum((CurrentPrice[i] * sell[i])
                      - (TransactionRate * (CurrentPrice[i] * sell[i] / 100))
                      - (TaxRate * ((CurrentPrice[i] - BuyPrice[i]) * sell[i] / 100)) for i in range(N)) >= K), "Capital_Requirement"

# Constraints to ensure sell does not exceed bought
for i in range(N):
    problem += (sell[i] <= Bought[i]), f"Max_Sell_Constraint_{i}"

# Solve the problem
problem.solve()

# Output the results
sell_values = [pulp.value(sell[i]) for i in range(N)]
output = {"sell": sell_values}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')