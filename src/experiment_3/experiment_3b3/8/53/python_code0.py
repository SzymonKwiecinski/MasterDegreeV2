import pulp

# Data
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Set of terminal cities
terminals = range(data['NumTerminals'])
# Set of destination cities
destinations = range(data['NumDestinations'])

# Initialize the problem
problem = pulp.LpProblem("Soybean_Transportation", pulp.LpMinimize)

# Decision variables: amount of soybeans shipped from terminal k to destination l
amount_vars = pulp.LpVariable.dicts("amount",
                                    ((k, l) for k in terminals for l in destinations),
                                    lowBound=0,
                                    cat='Continuous')

# Objective function: Minimize the total transportation cost
problem += pulp.lpSum(data['Cost'][k][l] * amount_vars[k, l] for k in terminals for l in destinations), "Total_Cost"

# Supply constraints: Total amount shipped from each terminal should not exceed its supply
for k in terminals:
    problem += pulp.lpSum(amount_vars[k, l] for l in destinations) <= data['Supply'][k], f"Supply_Constraint_{k}"

# Demand constraints: Total amount received by each destination should meet its demand
for l in destinations:
    problem += pulp.lpSum(amount_vars[k, l] for k in terminals) >= data['Demand'][l], f"Demand_Constraint_{l}"

# Solve the problem
problem.solve()

# Output the results
distribution = []
for k in terminals:
    for l in destinations:
        amount = amount_vars[k, l].varValue
        distribution.append({"from": k, "to": l, "amount": amount})

results = {
    "distribution": distribution,
    "total_cost": pulp.value(problem.objective)
}

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')