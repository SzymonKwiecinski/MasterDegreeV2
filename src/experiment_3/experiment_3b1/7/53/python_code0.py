import pulp

# Data from the JSON input
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Sets
K = range(data['NumTerminals'])  # Terminal cities
L = range(data['NumDestinations'])  # Destination cities
A = [(k, l) for k in K for l in L]  # All routes

# Create the problem
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", A, lowBound=0)  # amount[i,j] >= 0

# Objective function
problem += pulp.lpSum(data['Cost'][i][j] * amount[(i, j)] for i in K for j in L), "Total_Cost"

# Supply constraints
for k in K:
    problem += pulp.lpSum(amount[(k, j)] for j in L) <= data['Supply'][k], f"Supply_Constraint_{k}"

# Demand constraints
for l in L:
    problem += pulp.lpSum(amount[(i, l)] for i in K) >= data['Demand'][l], f"Demand_Constraint_{l}"

# Solve the problem
problem.solve()

# Print the distribution and total cost
distribution = [(i, j, pulp.value(amount[(i, j)])) for i, j in A]
total_cost = pulp.value(problem.objective)

print("Distribution:")
for record in distribution:
    if record[2] > 0:  # Only print positive shipments
        print(f"From city {record[0]} to city {record[1]}: {record[2]} units")

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')