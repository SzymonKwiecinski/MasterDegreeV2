import pulp

# Parse the provided JSON data
data = {'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}

# Unpack the data
n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']

n_years = len(requiredquality)

# Initialize the optimization problem
problem = pulp.LpProblem("Mining_Optimization", pulp.LpMaximize)

# Decision variables
isoperated = pulp.LpVariable.dicts("IsOperated", [(k, i) for k in range(n_mines) for i in range(n_years)], cat='Binary')
amount = pulp.LpVariable.dicts("Amount", [(k, i) for k in range(n_mines) for i in range(n_years)], lowBound=0)

# Objective function
discounted_revenue = [
    sum(amount[k, i] * price / ((1 + discount) ** i) for k in range(n_mines))
    for i in range(n_years)
]

discounted_royalty = [
    sum(isoperated[k, i] * royalty[k] / ((1 + discount) ** i) for k in range(n_mines))
    for i in range(n_years)
]

problem += sum(discounted_revenue[i] - discounted_royalty[i] for i in range(n_years)), "Total Discounted Profit"

# Constraints

# Quality constraint for blended ore in each year
for i in range(n_years):
    problem += sum(amount[k, i] * quality[k] for k in range(n_mines)) == \
               requiredquality[i] * sum(amount[k, i] for k in range(n_mines)), f"Quality_Constraint_Year_{i}"

# Limit constraint for each mine in each year
for k in range(n_mines):
    for i in range(n_years):
        problem += amount[k, i] <= limit[k] * isoperated[k, i], f"Limit_Constraint_Mine_{k}_Year_{i}"

# Maximum number of mines working constraint in each year
for i in range(n_years):
    problem += sum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork, f"Max_Working_Mines_Year_{i}"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "isoperated": [[int(isoperated[k, i].varValue) for i in range(n_years)] for k in range(n_mines)],
    "amount": [[amount[k, i].varValue for i in range(n_years)] for k in range(n_mines)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')