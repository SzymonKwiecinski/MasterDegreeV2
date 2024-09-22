# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- Consider a road divided into \var{N} segments that is illuminated by \var{M} lamps.
- Let \var{power_j} be the power of the \var{j}-th lamp. The illumination \var{ill_i} of the \var{i}-th segment is assumed to be \sum_{j=1}^{\var{M}} \var{coeff_{i,j}} \var{power_j}, where \var{coeff_{i,j}} are known coefficients.
- Let \var{desired_i} be the desired illumination of road \var{i}. 
- We are interested in choosing the lamp powers \var{power_j} so that the illuminations {ill_i} are close to the desired illuminations {desired_i}. 

INPUT FORMAT: 

{
    "coeff": [[coeff_{i,j} for j in 1, ..., M] for i in 1, ..., N],
    "desired": [desired_i for i in 1, ..., N]
}

OBJECTIVE: Find the lamp powers \var{power_j} that minimize the absolute error between the illuminations {ill_i} and the desired illuminations {desired_i}.

OUTPUT INFO:

- \var{power_j} is the optimal power of the \var{j}-th lamp.
- \var{error} is the absolute error between the illuminations {ill_i} and the desired illuminations {desired_i}.

OUTPUT FORMAT:

{
    "power": [power_j for j in 1, ..., M]
    "error": error
}
</DESCRIPTION>
<DATA>
{'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data from the JSON format
data = {'N': 3, 'M': 2, 'Coefficients': [[0.5, 0.3], [0.2, 0.4], [0.1, 0.6]], 'DesiredIlluminations': [14, 3, 12]}

N = data['N']
M = data['M']
coefficients = data['Coefficients']
desired_illuminations = data['DesiredIlluminations']

#### Define the problem
problem = pulp.LpProblem("Lamp_Power_Optimization", pulp.LpMinimize)

#### Define decision variables
powers = pulp.LpVariable.dicts("power", range(M), lowBound=0)

#### Define the errors
errors = pulp.LpVariable.dicts("error", range(N), lowBound=0)

#### Objective function: Minimize the sum of errors
problem += pulp.lpSum(errors[i] for i in range(N))

#### Constraints: Calculate illumination and set error
for i in range(N):
    illumination = pulp.lpSum(coefficients[i][j] * powers[j] for j in range(M))
    problem += illumination + errors[i] >= desired_illuminations[i]  #### Illumination must be at least desired
    problem += illumination - errors[i] <= desired_illuminations[i]  #### Illumination must be at most desired

#### Solve the problem
problem.solve()

#### Collect results
optimal_powers = [pulp.value(powers[j]) for j in range(M)]
total_error = pulp.value(problem.objective)

#### Output results
output = {
    "power": optimal_powers,
    "error": total_error
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_error}</OBJ>')
```

