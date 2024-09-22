import pulp
import json

# Data from the provided JSON
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

# Parameters unpacked from data
n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']
I = len(requiredquality)

# Create the LP problem
problem = pulp.LpProblem("MiningCompanyProblem", pulp.LpMaximize)

# Decision Variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(I)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(I)), lowBound=0)

# Objective Function
problem += pulp.lpSum(
    (price * pulp.lpSum(amount[(k, i)] for k in range(n_mines)) - 
     pulp.lpSum(royalty[k] * isoperated[(k, i)] for k in range(n_mines))) / (1 + discount)**(i + 1)
    for i in range(I)
)

# Constraints

# Capacity Constraint
for k in range(n_mines):
    for i in range(I):
        problem += amount[(k, i)] <= limit[k] * isoperated[(k, i)], f"CapacityConstraint_k{(k)}_i{(i)}"

# Quality Constraints
for i in range(I):
    problem += pulp.lpSum(amount[(k, i)] * quality[k] for k in range(n_mines)) == requiredquality[i] * pulp.lpSum(amount[(k, i)] for k in range(n_mines)), f"QualityConstraint_i{(i)}"

# Active Mines Constraint
for i in range(I):
    problem += pulp.lpSum(isoperated[(k, i)] for k in range(n_mines)) <= n_maxwork, f"ActiveMinesConstraint_i{(i)}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')