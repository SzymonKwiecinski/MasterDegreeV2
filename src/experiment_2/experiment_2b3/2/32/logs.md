# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- We suppose that some products can be produced, each of them passing through several stages.
- Necessary time to produce 1 unit of product \var{k} is \var{produce_time_{k, s}} hours for stage \var{s}.
- Availability in working hours is \var{time_{s}} for stage \var{s}. 
- The unitary profits for product \var{k} is \var{profit_{k}}.

INPUT FORMAT:

{
	"produce_time": [[produce_time_{k, s} for s in 1,...,S] for k in 1,...,K],
	"available_time": [time_{s} for s in 1,...,S],
	"profit": [profit_{k} for k in 1,...,K]
}


OBJECTIVE: Determine the quantities to be produced such that all the production constraints are satisfied and the profit is maximized.

OUTPUT INFO:

- \var{quantity} represents the production quantity for each product

OUTPUT FORMAT:

{
	"quantity": [quantity_{k} for k in 1,...,K]
}
</DESCRIPTION>
<DATA>
{'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To solve this problem using Linear Programming with the Pulp library in Python, we need to maximize the profit while satisfying the production constraints for each machine. Here's the corresponding Python code:

```python
import pulp

#### Data from JSON
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

#### Initialize the Linear Programming Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(data['NumProducts'])]

#### Objective Function
problem += pulp.lpSum([data['Profit'][k] * x[k] for k in range(data['NumProducts'])]), "Total_Profit"

#### Constraints
for s in range(data['NumMachines']):
    problem += (pulp.lpSum([data['ProduceTime'][k][s] * x[k] for k in range(data['NumProducts'])]) <= data['AvailableTime'][s]), f"Time_Constraint_Stage_{s}"

#### Solve the problem
problem.solve()

#### Output Result
result = {
    "quantity": [pulp.value(x[k]) for k in range(data['NumProducts'])]
}

#### Print the result
print(result)

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

This code sets up the optimization problem to maximize profit by producing the right quantity of each product while respecting the machine's time constraints. The decision variables, constraints, and objective function are set according to the given data, and the solution is obtained using Pulp's solver.

