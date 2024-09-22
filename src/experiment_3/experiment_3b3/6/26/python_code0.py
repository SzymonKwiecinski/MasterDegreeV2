import pulp

# Define the data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

K = len(data['stock'])
T = 5
available_manpower = 1000000  # This should be defined somewhere in the problem statement

# Initialize the problem
problem = pulp.LpProblem("Economic_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective function: Maximize total manpower requirement
problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t]
                      for k in range(K) for t in range(T))

# Constraints

# 1. Production and Stock Constraints for each year
for k in range(K):
    for t in range(T):
        if t == 0:
            problem += (produce[k, t] + data['stock'][k] == data['demand'][k] + stockhold[k, t])
        else:
            problem += (produce[k, t] + stockhold[k, t-1] == data['demand'][k] + stockhold[k, t])

# 2. Capacity Constraints
for k in range(K):
    for t in range(1, T):
        problem += (data['capacity'][k] + sum(buildcapa[k, t_prime] for t_prime in range(max(0, t-2))) <= produce[k, t] + stockhold[k, t])

# 3. Input Requirements for Production
for k in range(K):
    for t in range(1, T):
        problem += (pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K)) >= produce[k, t])

# 4. Manpower Constraints
for t in range(T):
    problem += (pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] 
                           for k in range(K)) <= available_manpower)

# Solving the problem
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Display solutions (if needed)
# for k in range(K):
#     for t in range(T):
#         print(f'produce[{k+1},{t+1}]: {produce[k, t].varValue}')
#         print(f'buildcapa[{k+1},{t+1}]: {buildcapa[k, t].varValue}')
#         print(f'stockhold[{k+1},{t+1}]: {stockhold[k, t].varValue}')