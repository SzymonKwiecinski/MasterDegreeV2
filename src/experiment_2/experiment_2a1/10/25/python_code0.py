import pulp
import json

# Input data
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
K = len(data['inputone'])  # number of industries
T = 3  # number of years

# Create the LP problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective function: Maximize total production in the last two years
problem += pulp.lpSum(produce[k, 1] + produce[k, 2] for k in range(K)), "Total_Production"

# Constraints for manpower and inputs
for t in range(T):
    for k in range(K):
        # Manpower constraint
        manpower_used = pulp.lpSum(manpowerone[k] * produce[k, t] + manpowertwo[k] * buildcapa[k, t] for k in range(K))
        problem += manpower_used <= data['manpower_limit'], f"Manpower_Limit_{t}"

        # Input constraints
        # For produce in year t
        if t < T - 1:
            input_needed = pulp.lpSum(inputone[k][j] * produce[j, t] for j in range(K))
            problem += produce[k, t] <= input_needed + stockhold[k, t], f"Input_Constraint_{k}_{t}"
        
        # Stock hold constraints
        if t > 0:
            problem += stockhold[k, t] == stockhold[k, t - 1] + produce[k, t - 1] - pulp.lpSum(inputone[k][j] * produce[j, t - 1] for j in range(K)), f"Stock_Hold_{k}_{t}"

# Capacity and stock initialization for year 0
for k in range(K):
    problem += stockhold[k, 0] == data['stock'][k], f"Initial_Stock_{k}"
    problem += stockhold[k, 0] <= data['capacity'][k], f"Initial_Capacity_{k}"

# Solve the problem
problem.solve()

# Gather output
produce_result = [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)]
buildcapa_result = [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)]
stockhold_result = [[pulp.value(stockhold[k, t]) for t in range(T)] for k in range(K)]

# Prepare final output
output = {
    "produce": produce_result,
    "buildcapa": buildcapa_result,
    "stockhold": stockhold_result
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')