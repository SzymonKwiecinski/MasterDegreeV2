# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- An Italian transport company must send empty containers from its depots to ports. 
- The number of containers available in the depot \var{i} is denoted with \var{numdepot_i}. 
- Container requirement in port \var{j} is \var{numport_{j}}. 
- Transport of containers is by barges. 
- Each barge can only contain two containers and the cost of transport (per barge) is proportional to the distance traveled (price is \var{price} Euros/km).
- The distances between depot \var{i} and port \var{j} is \var{distance_{i, j}}.

INPUT FORMAT:

{
	"numdepot": [numdepot_{i} for i in 1,...,I],
	"numport": [numport_{j} for j in 1,...,J],
	"price": price,
	"distance": [[distance_{i, j} for i in 1,...I] for j in 1,...,J]
}


OBJECTIVE: Minimize the total transportation cost.

OUTPUT INFO:

\var{number} represents the number of containers sent from each depot to port

OUTPUT FORMAT:

{
	"number": [[number_{i, j} for i in 1,...,I] for j in 1,...,J]
}
</DESCRIPTION>
<DATA>
{'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)  #### Number of depots
J = len(numport)   #### Number of ports

#### Create the problem variable
problem = pulp.LpProblem("Transport_Problem", pulp.LpMinimize)

#### Decision variables
number = pulp.LpVariable.dicts("number", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Integer')

#### Objective function: minimize total transportation cost
problem += pulp.lpSum(number[i, j] * distance[i][j] * price / 2 for i in range(I) for j in range(J)), "Total_Cost"

#### Constraints
#### Supply constraints for depots
for i in range(I):
    problem += pulp.lpSum(number[i, j] for j in range(J)) <= numdepot[i], f"Depot_Supply_Constraint_{i}"

#### Demand constraints for ports
for j in range(J):
    problem += pulp.lpSum(number[i, j] for i in range(I)) >= numport[j], f"Port_Demand_Constraint_{j}"

#### Solve the problem
problem.solve()

#### Prepare the output
output = {
    "number": [[number[i, j].varValue for j in range(J)] for i in range(I)]
}

print(json.dumps(output))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

