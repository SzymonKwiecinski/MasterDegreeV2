import pulp

# Problem data
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

# Extract parameters
n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']
n_years = len(requiredquality)

# Indices
K = range(n_mines)
I = range(n_years)

# Problem definition
problem = pulp.LpProblem("Mine_Operation_Optimization", pulp.LpMaximize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in K for i in I), lowBound=0, cat='Continuous')
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in K for i in I), cat='Binary')

# Objective function
discounted_profit = sum(
    (1 / (1 + discount) ** (i + 1)) * (
        price * sum(amount[(k, i)] for k in K) -
        sum(royalty[k] * isoperated[(k, i)] for k in K)
    )
    for i in I
)
problem += discounted_profit

# Constraints
# Quality requirements
for i in I:
    total_extracted = sum(amount[(k, i)] for k in K)
    problem += sum(amount[(k, i)] * quality[k] for k in K) == requiredquality[i] * total_extracted

# Max number of mines operated per year
for i in I:
    problem += sum(isoperated[(k, i)] for k in K) <= n_maxwork

# Extraction limits
for k in K:
    for i in I:
        problem += amount[(k, i)] <= limit[k] * isoperated[(k, i)]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')