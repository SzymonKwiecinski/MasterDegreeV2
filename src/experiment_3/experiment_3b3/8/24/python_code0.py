import pulp

# Data
data = {
    'n_mines': 4,
    'n_maxwork': 3,
    'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0],
    'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0],
    'quality': [1.0, 0.7, 1.5, 0.5],
    'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0],
    'price': 10,
    'discount': 0.1
}

# Number of years
n_years = len(data['requiredquality'])

# Problem Definition
problem = pulp.LpProblem("Mining_Company_Operations", pulp.LpMaximize)

# Decision Variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(data['n_mines']) for i in range(n_years)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(data['n_mines']) for i in range(n_years)), lowBound=0)

# Revenue and Cost Calculation
revenue = sum(data['price'] * amount[k, i] for k in range(data['n_mines']) for i in range(n_years))
cost = sum(data['royalty'][k] * isoperated[k, i] for k in range(data['n_mines']) for i in range(n_years))

# Objective Function
problem += revenue - cost, "Total_Profit"

# Constraints
# Production Quality Constraint
for i in range(n_years):
    problem += (
        pulp.lpSum(data['quality'][k] * amount[k, i] for k in range(data['n_mines'])) == 
        data['requiredquality'][i] * pulp.lpSum(amount[j, i] for j in range(data['n_mines']))
    )

# Ore Extraction Limit
for k in range(data['n_mines']):
    for i in range(n_years):
        problem += amount[k, i] <= data['limit'][k] * isoperated[k, i]

# Operating Mines Constraint
for i in range(n_years):
    problem += pulp.lpSum(isoperated[k, i] for k in range(data['n_mines'])) <= data['n_maxwork']

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')