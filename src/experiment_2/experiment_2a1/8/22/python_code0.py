import pulp
import json

# Input data in JSON format
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Extracting the data
requirements = data["requirement"]
strengths = data["strength"]
less_one_waste = data["lessonewaste"]
more_one_waste = data["moreonewaste"]
recruit_limits = data["recruit"]
cost_redundancy = data["costredundancy"]
num_overman = data["num_overman"]
cost_overman = data["costoverman"]
num_shortwork = data["num_shortwork"]
cost_short = data["costshort"]

K = len(requirements)  # number of labor categories
I = len(requirements[0])  # number of years

# Initialize the LP problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision variables
recruit_vars = pulp.LpVariable.dicts("Recruit", (range(K), range(I)), lowBound=0, cat='Integer')
overmanning_vars = pulp.LpVariable.dicts("Overmanning", (range(K), range(I)), lowBound=0, cat='Integer')
short_vars = pulp.LpVariable.dicts("Short", (range(K), range(I)), lowBound=0, cat='Integer')

# Objective function: Minimize total redundancy costs
problem += pulp.lpSum(cost_redundancy[k] * (strengths[k] + pulp.lpSum(recruit_vars[k][i] for i in range(I))
                                              + pulp.lpSum(overmanning_vars[k][i] for i in range(I))
                                              - pulp.lpSum(short_vars[k][i] for i in range(I))
                                              - (strengths[k] * (1 - more_one_waste[k])) - requirements[k][i])
                      for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        # Recruitment limits
        problem += recruit_vars[k][i] <= recruit_limits[k]
        # Overmanning limits
        problem += overmanning_vars[k][i] <= num_overman
        # Short-time working limits
        problem += short_vars[k][i] <= num_shortwork

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "recruit": [[pulp.value(recruit_vars[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning_vars[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_vars[k][i]) for i in range(I)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')