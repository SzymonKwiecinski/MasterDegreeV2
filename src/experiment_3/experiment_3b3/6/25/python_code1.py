import pulp

# Define the data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0,
}

K = len(data['inputone'])  # Number of industries
T = 3  # Number of years

# Create the LP problem
problem = pulp.LpProblem("Economy_Linear_Programming", pulp.LpMaximize)

# Define variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("stock", ((k, t) for k in range(K) for t in range(T+1)), lowBound=0, cat='Continuous')  # Fix index range for stock

# Objective function: Maximize total production in the last two years
problem += pulp.lpSum(produce[k, T] + produce[k, T-1] for k in range(K)), "Maximize_Production_Last_Two_Years"

# Constraints

# Initial stock setup
for k in range(K):
    stock[k, 0] = data['stock'][k]  # Initial stock

# Production constraints for each industry in each year
for k in range(K):
    for t in range(1, T+1):
        problem += produce[k, t] <= stock[k, t-1] + pulp.lpSum(data['inputone'][j][k] * produce[j, t-1] for j in range(K)), f"Production_Constraint_{k}_{t}"

# Capacity constraints for each industry
for k in range(K):
    for t in range(1, T+1):
        problem += stock[k, t] == stock[k, t-1] + produce[k, t] - buildcapa[k, t], f"Capacity_Constraint_{k}_{t}"

# Manpower constraints for each year
for t in range(1, T+1):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit'], f"Manpower_Constraint_{t}"

# Capacity building constraints after one year
for k in range(K):
    for t in range(1, T):
        problem += data['capacity'][k] >= buildcapa[k, t+1], f"Capacity_Building_Year_{k}_{t}"

# Solve the problem
problem.solve(pulp.PULP_CBC_CMD(msg=0))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')