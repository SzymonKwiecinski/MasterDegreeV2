import pulp
import json

# Provided data in JSON format
data_json = '''{
    "large_roll_width": 70, 
    "demands": [40, 65, 80, 75], 
    "roll_width_options": [17, 14, 11, 8.5], 
    "patterns": [
        [4, 0, 0, 0], 
        [3, 1, 0, 0], 
        [3, 0, 1, 0], 
        [2, 2, 0, 0], 
        [3, 0, 0, 2], 
        [2, 1, 2, 0], 
        [2, 1, 1, 1], 
        [2, 1, 0, 2], 
        [2, 0, 3, 0], 
        [2, 0, 2, 1], 
        [2, 0, 1, 2], 
        [1, 3, 1, 0], 
        [1, 3, 0, 1], 
        [1, 2, 2, 0], 
        [1, 2, 1, 1], 
        [1, 2, 0, 2], 
        [1, 1, 3, 0], 
        [0, 5, 0, 0], 
        [0, 4, 1, 0], 
        [0, 4, 0, 1], 
        [0, 3, 2, 0], 
        [2, 0, 0, 4], 
        [1, 1, 2, 2], 
        [1, 1, 1, 3], 
        [1, 1, 0, 4], 
        [1, 0, 4, 1], 
        [1, 0, 3, 2], 
        [1, 0, 2, 3], 
        [1, 0, 1, 4], 
        [0, 3, 1, 2], 
        [0, 3, 0, 3], 
        [0, 2, 3, 1], 
        [0, 2, 2, 2], 
        [0, 2, 1, 3], 
        [0, 2, 0, 4], 
        [0, 1, 5, 0], 
        [0, 1, 4, 1], 
        [0, 1, 3, 2], 
        [0, 0, 6, 0], 
        [0, 0, 5, 1], 
        [1, 0, 0, 6], 
        [0, 1, 2, 4], 
        [0, 1, 1, 5], 
        [0, 1, 0, 6], 
        [0, 0, 4, 3], 
        [0, 0, 3, 4], 
        [0, 0, 2, 5], 
        [0, 0, 1, 6], 
        [0, 0, 0, 8]
    ]
}'''

# Load the data
data = json.loads(data_json)

# Extracting data from the loaded JSON
large_roll_width = data['large_roll_width']
demands = data['demands']
patterns = data['patterns']

# Define the problem
problem = pulp.LpProblem("PaperCuttingProblem", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("pattern", range(len(patterns)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(x[i] for i in range(len(patterns))), "TotalLargeRolls"

# Constraints for demand fulfillment
for j in range(len(demands)):
    problem += pulp.lpSum(patterns[i][j] * x[i] for i in range(len(patterns))) >= demands[j], f"DemandForSmallRoll_{j+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')