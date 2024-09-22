import pulp

# Input data
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

# Unpack data
n_mines = data["n_mines"]
n_maxwork = data["n_maxwork"]
royalty = data["royalty"]
limit = data["limit"]
quality = data["quality"]
requiredquality = data["requiredquality"]
price = data["price"]
discount = data["discount"]

n_years = len(requiredquality)

# Create the problem
problem = pulp.LpProblem("Mining_Optimization", pulp.LpMaximize)

# Variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(n_years)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(n_years)), lowBound=0)

# Objective function
discounted_revenue = pulp.lpSum(
    ((price * pulp.lpSum(amount[(k, i)] for k in range(n_mines)) -
      pulp.lpSum(royalty[k] * isoperated[(k, i)] for k in range(n_mines))) / ((1 + discount) ** i))
    for i in range(n_years)
)

problem += discounted_revenue

# Constraints
for i in range(n_years):
    # Quality constraint
    problem += pulp.lpSum(quality[k] * amount[(k, i)] for k in range(n_mines)) == requiredquality[i] * pulp.lpSum(amount[(k, i)] for k in range(n_mines))
    
    # Maximum number of operational mines
    problem += pulp.lpSum(isoperated[(k, i)] for k in range(n_mines)) <= n_maxwork

    # Operational and limit constraints
    for k in range(n_mines):
        problem += amount[(k, i)] <= limit[k] * isoperated[(k, i)]

# Solve
problem.solve()

# Output
output = {
    "isoperated": [[pulp.value(isoperated[(k, i)]) for i in range(n_years)] for k in range(n_mines)],
    "amount": [[pulp.value(amount[(k, i)]) for i in range(n_years)] for k in range(n_mines)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')