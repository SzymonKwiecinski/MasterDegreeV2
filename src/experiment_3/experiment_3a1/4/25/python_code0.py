import pulp
import json

data = json.loads("{'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 'manpowerone': [0.6, 0.3, 0.2], 'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 'manpowertwo': [0.4, 0.2, 0.1], 'stock': [150, 80, 100], 'capacity': [300, 350, 280], 'manpower_limit': 470000000.0}")

K = len(data['stock'])
T = 10  # Assuming 10 years for the purpose of this example
manpower_limit = data['manpower_limit']

# Define the problem
problem = pulp.LpProblem("Economic_Production", pulp.LpMaximize)

# Define decision variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([produce[k][T-1] + produce[k][T-2] for k in range(K)])

# Initial Conditions
for k in range(K):
    problem += stockhold[k][0] == data['stock'][k]
    problem += stockhold[k][1] == data['stock'][k]  # Initial stock at year 0 equals initial stock

# Constraints
for t in range(1, T):
    for k in range(K):
        # Production Requirements
        problem += produce[k][t] <= data['capacity'][k] + stockhold[k][t-1]

        # Input Requirements for Production
        problem += pulp.lpSum(data['inputone'][k][j] * produce[j][t-1] for j in range(K)) + stockhold[k][t-1] >= produce[k][t]

    # Manpower Constraints for Production
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] for k in range(K)) <= manpower_limit

    for k in range(K):
        # Capacity Building Constraints
        problem += buildcapa[k][t] <= data['capacity'][k] + stockhold[k][t-1]

        # Input Requirements for Capacity Building
        problem += pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t-1] for j in range(K)) + stockhold[k][t-1] >= buildcapa[k][t]

    # Manpower Constraints for Capacity Building
    problem += pulp.lpSum(data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)) <= manpower_limit

    for k in range(K):
        # Stock Dynamics
        problem += stockhold[k][t] == stockhold[k][t-1] + produce[k][t-1] - produce[k][t]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')