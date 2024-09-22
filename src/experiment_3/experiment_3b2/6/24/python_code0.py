import pulp
import json

# Data provided in JSON format
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

# Parameters
n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']
n_years = len(requiredquality)

# Create the problem
problem = pulp.LpProblem("Mining_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
isoperated = pulp.LpVariable.dicts("isoperated", 
                                    ((k, i) for k in range(n_mines) for i in range(n_years)), 
                                    cat='Binary')
amount = pulp.LpVariable.dicts("amount", 
                                ((k, i) for k in range(n_mines) for i in range(n_years)), 
                                lowBound=0)

# Objective Function
problem += pulp.lpSum(
    (price * pulp.lpSum(amount[k, i] for k in range(n_mines)) - 
     pulp.lpSum(royalty[k] * isoperated[k, i] for k in range(n_mines))) /
    ((1 + discount) ** (i + 1))
    for i in range(n_years)), 
    "Total_Profit"
)

# Constraints

# Ore Quality Constraint
for i in range(n_years):
    problem += (pulp.lpSum(amount[k, i] * quality[k] for k in range(n_mines)) ==
                 requiredquality[i] * pulp.lpSum(amount[k, i] for k in range(n_mines))), f"Quality_Constraint_{i}"

# Operation Limit Constraint
for i in range(n_years):
    problem += (pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork), f"Operation_Limit_Constraint_{i}"

# Capacity Constraint
for k in range(n_mines):
    for i in range(n_years):
        problem += (amount[k, i] <= limit[k] * isoperated[k, i]), f"Capacity_Constraint_{k}_{i}"
        problem += (amount[k, i] >= 0), f"Non_Negativity_Constraint_{k}_{i}"

# Sequential Operation Constraint
for k in range(n_mines):
    for i in range(1, n_years):
        problem += (isoperated[k, i] <= isoperated[k, i - 1] + 1), f"Sequential_Operation_Constraint_{k}_{i}"

# Solve the problem
problem.solve()

# Print result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')