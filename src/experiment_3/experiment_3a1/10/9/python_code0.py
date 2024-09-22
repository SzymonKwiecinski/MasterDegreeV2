import pulp
import json

# Data provided in JSON format
data_json = '''{
    "N": 3,
    "M": 2,
    "Coefficients": [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]],
    "DesiredIlluminations": [14, 3, 12]
}'''

data = json.loads(data_json)

# Parameters
N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

# Initialize the problem
problem = pulp.LpProblem("LampPowerOptimization", pulp.LpMinimize)

# Decision Variables
power = pulp.LpVariable.dicts("power", range(M), lowBound=0)  # power of lamps
u = pulp.LpVariable.dicts("u", range(N), lowBound=0)  # auxiliary variables for absolute error

# Objective Function: Minimize total absolute error
problem += pulp.lpSum(u[i] for i in range(N))

# Constraints
for i in range(N):
    # Illumination constraint
    problem += (pulp.lpSum(coefficients[i][j] * power[j] for j in range(M)) == 
                 pulp.lpSum(u[i] + desired_illuminations[i] for i in range(N)))

    # Auxiliary variable constraints for absolute values
    problem += u[i] >= (pulp.lpSum(coefficients[i][j] * power[j] for j in range(M)) - desired_illuminations[i])
    problem += u[i] >= -(pulp.lpSum(coefficients[i][j] * power[j] for j in range(M)) - desired_illuminations[i])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')