import pulp
import json

# Input Data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

K = len(data['inputone'])  # Number of industries
T = 5  # Number of years

# Create the LP problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0, cat='Continuous')

# Objective Function: Maximize total manpower requirement over five years
problem += pulp.lpSum(data['manpowerone'][k] * (pulp.lpSum(produce[k][t] for t in range(T)) +
                                                 pulp.lpSum(buildcapa[k][t] for t in range(T)))
                      for k in range(K)), "Total_Manpower_Requirement"

# Constraints
for k in range(K):
    for t in range(T):
        # Capacity constraint for production
        if t == 0:
            problem += produce[k][t] + stockhold[k][t] <= data['stock'][k] + data['capacity'][k], f"Capacity_Year_{t}_Industry_{k}"
        else:
            problem += produce[k][t] + stockhold[k][t] <= data['capacity'][k] + stockhold[k][t-1], f"Capacity_Year_{t}_Industry_{k}_Previous"

        if t >= 1:
            # Input requirements for production and building capacity
            problem += pulp.lpSum(data['inputone'][k][j] * produce[j][t-1] for j in range(K)) >= produce[k][t] + data['demand'][k], f"Input_Production_Industry_{k}_Year_{t}"
            problem += pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t-1] for j in range(K)) >= buildcapa[k][t], f"Input_BuildCapacity_Industry_{k}_Year_{t}"

        # Stock constraint for year t
        if t > 0:  # Start from year 1 as we can't reference -1
            problem += stockhold[k][t] == stockhold[k][t-1] + produce[k][t] - data['demand'][k], f"Stock_Holding_Year_{t}_Industry_{k}"

# Initial stocks
for k in range(K):
    problem += stockhold[k][0] == data['stock'][k], f"Initial_Stock_Industry_{k}"

# Solve the Problem
problem.solve()

# Prepare the output
produce_result = [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)]
buildcapa_result = [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)]
stockhold_result = [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]

output = {
    "produce": produce_result,
    "buildcapa": buildcapa_result,
    "stockhold": stockhold_result
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')