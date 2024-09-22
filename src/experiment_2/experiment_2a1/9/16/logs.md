# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- A manager of an oil refinery has \var{allocated_i} million barrels of crude oil type \var{i} allocated for production during the coming month. 
- These resources can be used to make \var{P} different products. product \var{p} sells for $ \var{price_p} per barrel.
- There are \var{L} production processes. Process \var{l} uses \var{input_l_i} barrels of each crude \var{i}, and produces \var{output_l_p} barrels of each product \var{p}. 
- Process \var{l} has a cost of \var{cost_l} per barrel of product produced.
- All \var{input_l_i} quantities and \var{output_l_p} quanitites are in barrels. 
- There are no separate cost items for the cost of the crudes, as they have already been allocated.

INPUT FORMAT: 

{
    "allocated": [allocated_i for i in 1, ..., O],
    "price": [price_p for p in 1, ..., P],
    "input": [[input_l_i for i in 1, ..., O] for l in 1, ..., L],
    "output": [[output_l_p for p in 1, ..., P] for l in 1, ..., L],
    "cost": [cost_l for l in 1, ..., L]
}

OBJECTIVE: We want to know how many times should we execute each process to maximize the revenue for the next month (you can assume that the number of times that each process is executed is a floating point number)

OUTPUT INFO:

- \var{revenue} is the total revenue for the month.
- \var{execute_l} is the number of times that process \var{l} should be executed.

OUTPUT FORMAT:

{
    "revenue": revenue,
    "execute": [execute_l for l in 1, ..., L]
}

</DESCRIPTION>
<DATA>
{'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 
        'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 
        'Cost': [51, 11, 40]}

#### Extract data from the input JSON
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']

#### Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Variables for how many times each process is executed
execute = pulp.LpVariable.dicts("execute", range(L), lowBound=0, cat='Continuous')

#### Objective function: Maximize revenue - total cost
revenue = pulp.lpSum([execute[l] * pulp.lpSum([output_data[l][p] * price[p] for p in range(P)]) for l in range(L)])
total_cost = pulp.lpSum([execute[l] * cost[l] for l in range(L)])
problem += revenue - total_cost, "Total_Profit"

#### Constraints for the available crude oil
for i in range(O):
    problem += pulp.lpSum([execute[l] * input_data[l][i] for l in range(L)]) <= allocated[i], f"Oil_Constraint_{i}"

#### Solve the problem
problem.solve()

#### Output the results
revenue_value = pulp.value(problem.objective) + total_cost  #### since profit = revenue - cost
execute_values = [execute[l].varValue for l in range(L)]

#### Format the output
output = {
    "revenue": revenue_value,
    "execute": execute_values
}

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

