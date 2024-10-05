import pulp

# Data
data = {
    'P': 2,
    'Cash': 3000,
    'Hour': [2, 6],
    'Cost': [3, 2],
    'Price': [6, 5],
    'InvestPercentage': [0.4, 0.3],
    'UpgradeHours': 2000,
    'UpgradeCost': 400,
    'AvailableHours': 2000
}

# Unpack data
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
invest_percentage = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(P)]
u = pulp.LpVariable("u", cat='Binary')

# Objective Function
problem += pulp.lpSum(
    price[i] * x[i] - cost[i] * x[i] - invest_percentage[i] * price[i] * x[i] for i in range(P)
)

# Cash Constraint
problem += pulp.lpSum(
    cost[i] * x[i] + invest_percentage[i] * price[i] * x[i] for i in range(P)
) + u * upgrade_cost <= cash

# Machine Hours Constraint
problem += pulp.lpSum(
    hour[i] * x[i] for i in range(P)
) <= available_hours + u * upgrade_hours

# Solve
problem.solve()

# Result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')