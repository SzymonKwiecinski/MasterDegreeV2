import pulp

# Data from JSON
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

# Parameters
K = len(data['capacity'])
T = 5  # Consider a 5-year plan

# Create a linear programming problem
problem = pulp.LpProblem("Economic_Production_Plan", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(produce[k, T-1] + produce[k, T-2] for k in range(K))

# Constraints
for k in range(K):
    for t in range(T):
        if t == 0:
            stock_prev = data['stock'][k]
        else:
            stock_prev = stockhold[k, t-1]
        
        # Production constraints
        problem += produce[k, t] <= data['capacity'][k] + stock_prev

        # Input constraints for production
        problem += pulp.lpSum(data['inputone'][k][j] * (produce[j, t-1] if t > 0 else 0) for j in range(K)) + stock_prev >= produce[k, t]
        
        # Stock constraints
        if t > 0:
            problem += stockhold[k, t] == stockhold[k, t-1] + produce[k, t-1] - produce[k, t]

# Manpower constraints
for t in range(T):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')