import pulp
import json

# Data provided in JSON format
data = json.loads("{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}")

# Model parameters
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
invest_percentage = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)  # Production quantities for products
u = pulp.LpVariable("u", cat='Binary')  # Upgrade decision variable

# Objective Function
net_income = pulp.lpSum((price[i] - cost[i]) * x[i] - invest_percentage[i] * price[i] * x[i] for i in range(P)) - u * upgrade_cost
problem += net_income, "Total_Net_Income"

# Constraints
# Machine Capacity Constraint
problem += pulp.lpSum(hour[i] * x[i] for i in range(P)) <= available_hours + u * upgrade_hours, "Machine_Capacity"

# Cash Availability Constraint
problem += pulp.lpSum(cost[i] * x[i] for i in range(P)) <= cash + pulp.lpSum(invest_percentage[i] * price[i] * x[i] for i in range(P)), "Cash_Availability"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')