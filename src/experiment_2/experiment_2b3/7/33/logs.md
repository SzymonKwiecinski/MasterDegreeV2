# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MIP
PROBLEM INFO:

- The knapsack problem has a significant place in the study of integer programming models with binary variables. 
- In the knapsack problem, one needs to pack a set of items in a container.
- Each item \var{k} has value \var{value_{k}} and size \var{size_{k}}.
- And the container has maximum capacity \var{C}. 
- If the total size of the items exceeds the capacity, we can't pack them all. 
- In that case, the problem is to choose a subset of the items of maximum total value that will fit in the container. 

INPUT FORMAT:

{
	"C": C,
	"value": [value_{k} for k in 1,...,K],
	"size": [size_{k} for k in 1,...,K]
}


OBJECTIVE: Maximize the total value of the packed items

OUTPUT INFO:

- \var{isincluded} represents whether each item is included in the container

OUTPUT FORMAT:

{
	"isincluded": [isincluded_{k} for k in 1,...,K]
}
</DESCRIPTION>
<DATA>
{'C': 10, 'value': [10, 20], 'size': [8, 6]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Parse input data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

#### Initialize the problem
problem = pulp.LpProblem('Knapsack', pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{k}', cat='Binary') for k in range(K)]

#### Objective function: Maximize total value
problem += pulp.lpSum(values[k] * x[k] for k in range(K))

#### Constraint: Total size should not exceed capacity
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C

#### Solve the problem
problem.solve()

#### Prepare the output
isincluded = [int(x[k].varValue) for k in range(K)]
output = {
    "isincluded": isincluded
}

#### Output result
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

