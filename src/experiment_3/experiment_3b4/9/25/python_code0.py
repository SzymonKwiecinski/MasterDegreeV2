import pulp

# Data from the JSON
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

# Constants
K = len(data['capacity'])  # Number of industries
T = 3  # Given three years, we define T as 3 (year indices 0 to 2)

# Create the Linear Programming problem
problem = pulp.LpProblem("Economic_Model", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective function: Maximize production in the last two years
problem += pulp.lpSum(produce[k, T-2] + produce[k, T-1] for k in range(K)), "Total_Production_Last_Two_Years"

# Constraints

# Initial Conditions
for k in range(K):
    problem += stockhold[k, 0] == data['stock'][k], f"Initial_Stock_{k}"
    problem += stockhold[k, 0] <= data['stock'][k], f"Stock_Constraint_{k}_0"
    
# Production Capacity Constraints
for t in range(2, T):
    for k in range(K):
        problem += produce[k, t] <= data['capacity'][k] + pulp.lpSum(buildcapa[j, t-2] * data['inputtwo'][k][j] for j in range(K)), f"Capacity_Constraint_{k}_{t}"

# Resource Utilization Constraints
for t in range(T):
    for k in range(K):
        problem += (pulp.lpSum(produce[j, t] * data['inputone'][k][j] for j in range(K)) +
                    pulp.lpSum(buildcapa[j, t] * data['inputtwo'][k][j] for j in range(K))) <= (
                            stockhold[k, t-1] + produce[k, t] + stockhold[k, t]), f"Resource_Utilization_{k}_{t}"

# Manpower Constraints
for t in range(T):
    problem += (pulp.lpSum(produce[k, t] * data['manpowerone'][k] + buildcapa[k, t] * data['manpowertwo'][k] for k in range(K))
                <= data['manpower_limit']), f"Manpower_Constraint_{t}"

# Stock Balance
for t in range(1, T):
    for k in range(K):
        problem += stockhold[k, t] == (stockhold[k, t-1] + produce[k, t] -
                                       pulp.lpSum(produce[j, t] * data['inputone'][k][j] + buildcapa[j, t] * data['inputtwo'][k][j] for j in range(K))), f"Stock_Balance_{k}_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')