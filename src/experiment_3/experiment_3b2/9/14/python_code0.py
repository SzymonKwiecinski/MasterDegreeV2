import pulp
import json

# Data input
data = json.loads('{"P": 2, "Cash": 3000, "Hour": [2, 6], "Cost": [3, 2], "Price": [6, 5], "InvestPercentage": [0.4, 0.3], "UpgradeHours": 2000, "UpgradeCost": 400, "AvailableHours": 2000}')

P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
invest_percentage = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Create the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)  # Continuous variables for product quantities
y = pulp.LpVariable("y", cat='Binary')  # Binary variable for upgrade decision

# Objective function
problem += pulp.lpSum((price[i] - cost[i] - invest_percentage[i] * price[i]) * x[i] for i in range(P)) - upgrade_cost * y, "Net_Income"

# Constraints
problem += pulp.lpSum(hour[i] * x[i] for i in range(P)) <= available_hours + upgrade_hours * y, "Machine_Hours_Constraint"

problem += pulp.lpSum(cost[i] * x[i] for i in range(P)) <= cash + pulp.lpSum(invest_percentage[i] * price[i] * x[i] for i in range(P)) - upgrade_cost * y, "Cash_Availability_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')