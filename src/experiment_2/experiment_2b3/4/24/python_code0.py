from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value, LpBinary
import json

# Load data
data = json.loads('{"n_mines": 4, "n_maxwork": 3, "royalty": [5000000.0, 4000000.0, 4000000.0, 5000000.0], "limit": [2000000.0, 2500000.0, 1300000.0, 3000000.0], "quality": [1.0, 0.7, 1.5, 0.5], "requiredquality": [0.9, 0.8, 1.2, 0.6, 1.0], "price": 10, "discount": 0.1}')

# Extract parameters
n_mines = data["n_mines"]
n_maxwork = data["n_maxwork"]
royalty = data["royalty"]
limit = data["limit"]
quality = data["quality"]
requiredquality = data["requiredquality"]
price = data["price"]
discount = data["discount"]

# Number of years
n_years = len(requiredquality)

# Create the problem instance
problem = LpProblem("Maximize_Profit", LpMaximize)

# Decision variables
is_operated = LpVariable.dicts("IsOperated", [(k, i) for k in range(n_mines) for i in range(n_years)], cat=LpBinary)
amount = LpVariable.dicts("Amount", [(k, i) for k in range(n_mines) for i in range(n_years)], lowBound=0)

# Objective function: Maximize discounted profit
problem += lpSum(
    (price * lpSum(amount[k, i] for k in range(n_mines)) - lpSum(royalty[k] * is_operated[k, i] for k in range(n_mines))) / ((1 + discount) ** i)
    for i in range(n_years)
)

# Constraints

# Each year, only n_maxwork mines can be operated
for i in range(n_years):
    problem += lpSum(is_operated[k, i] for k in range(n_mines)) <= n_maxwork

# Ensure quality requirement is met each year
for i in range(n_years):
    problem += lpSum(amount[k, i] * quality[k] for k in range(n_mines)) == requiredquality[i] * lpSum(amount[k, i] for k in range(n_mines))

# Production constraints for each mine
for k in range(n_mines):
    for i in range(n_years):
        problem += amount[k, i] <= limit[k] * is_operated[k, i]

# Solve the problem
problem.solve()

# Prepare results
isoperated = [[int(is_operated[k, i].varValue) for i in range(n_years)] for k in range(n_mines)]
amounts = [[amount[k, i].varValue for i in range(n_years)] for k in range(n_mines)]

results = {
    "isoperated": isoperated,
    "amount": amounts
}

print(json.dumps(results, indent=4))
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')