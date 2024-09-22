# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MILP

PROBLEM INFO:

- A paper company produces large rolls of paper with a width of \var{large_roll_width} inches.
- These large rolls are cut into smaller rolls of various widths options to meet customer demand.
- There are \var{M} different types of smaller rolls.
- The demand for rolls of width \var{inch_j} ​is \var{demand_j}​ units.
- The company has \var{N} different cutting patterns available for producing the smaller rolls.
- For pattern \var{i}, the number of rolls of width \var{j} that are produced is \var{pattern_{i,j}}.

INPUT FORMAT: 

{
    "large_roll_width": large_roll_width,
    "roll_width_options": [inch_j for j in 1, ..., M],
    "demands": [demand_j for j in 1, ..., M],
    "patterns": [[pattern_{i,j} for j in 1, ..., M] for i in 1, ..., N]
}

OBJECTIVE: Determine the minimum number of large \var{large_roll_width}-inch rolls needed to fulfill all the orders.

OUTPUT INFO:

- The different cutting patterns applied to the large rolls are detailed in \var{patterns}.
- The total number of large rolls of paper used in this optimization is \var{total_large_rolls_used}.

OUTPUT FORMAT:

{
    "patterns": [
        {
         "pattern": [pattern_j for i in 1, ..., M]
         "amount": amount_i
        }
        for i in 1, ..., N
    ],
    "total_large_rolls_used": total_large_rolls
}
</DESCRIPTION>
<DATA>
{'large_roll_width': 70, 'demands': [40, 65, 80, 75], 'roll_width_options': [17, 14, 11, 8.5], 'patterns': [[4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0], [2, 2, 0, 0], [3, 0, 0, 2], [2, 1, 2, 0], [2, 1, 1, 1], [2, 1, 0, 2], [2, 0, 3, 0], [2, 0, 2, 1], [2, 0, 1, 2], [1, 3, 1, 0], [1, 3, 0, 1], [1, 2, 2, 0], [1, 2, 1, 1], [1, 2, 0, 2], [1, 1, 3, 0], [0, 5, 0, 0], [0, 4, 1, 0], [0, 4, 0, 1], [0, 3, 2, 0], [2, 0, 0, 4], [1, 1, 2, 2], [1, 1, 1, 3], [1, 1, 0, 4], [1, 0, 4, 1], [1, 0, 3, 2], [1, 0, 2, 3], [1, 0, 1, 4], [0, 3, 1, 2], [0, 3, 0, 3], [0, 2, 3, 1], [0, 2, 2, 2], [0, 2, 1, 3], [0, 2, 0, 4], [0, 1, 5, 0], [0, 1, 4, 1], [0, 1, 3, 2], [0, 0, 6, 0], [0, 0, 5, 1], [1, 0, 0, 6], [0, 1, 2, 4], [0, 1, 1, 5], [0, 1, 0, 6], [0, 0, 4, 3], [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6], [0, 0, 0, 8]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

data = {'large_roll_width': 70, 'demands': [40, 65, 80, 75], 'roll_width_options': [17, 14, 11, 8.5], 'patterns': [[4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0], [2, 2, 0, 0], [3, 0, 0, 2], [2, 1, 2, 0], [2, 1, 1, 1], [2, 1, 0, 2], [2, 0, 3, 0], [2, 0, 2, 1], [2, 0, 1, 2], [1, 3, 1, 0], [1, 3, 0, 1], [1, 2, 2, 0], [1, 2, 1, 1], [1, 2, 0, 2], [1, 1, 3, 0], [0, 5, 0, 0], [0, 4, 1, 0], [0, 4, 0, 1], [0, 3, 2, 0], [2, 0, 0, 4], [1, 1, 2, 2], [1, 1, 1, 3], [1, 1, 0, 4], [1, 0, 4, 1], [1, 0, 3, 2], [1, 0, 2, 3], [1, 0, 1, 4], [0, 3, 1, 2], [0, 3, 0, 3], [0, 2, 3, 1], [0, 2, 2, 2], [0, 2, 1, 3], [0, 2, 0, 4], [0, 1, 5, 0], [0, 1, 4, 1], [0, 1, 3, 2], [0, 0, 6, 0], [0, 0, 5, 1], [1, 0, 0, 6], [0, 1, 2, 4], [0, 1, 1, 5], [0, 1, 0, 6], [0, 0, 4, 3], [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6], [0, 0, 0, 8]]}

large_roll_width = data['large_roll_width']
demands = data['demands']
patterns = data['patterns']

#### Create a linear programming problem
problem = pulp.LpProblem("Roll_Cutting_Problem", pulp.LpMinimize)

#### Decision variables for the number of each cutting pattern to use
x = pulp.LpVariable.dicts("pattern", range(len(patterns)), lowBound=0, cat='Integer')

#### Objective function: minimize the number of large rolls used
problem += pulp.lpSum(x[i] for i in range(len(patterns))), "Total_Large_Rolls_Used"

#### Constraints to meet the demands
for j in range(len(demands)):
    problem += pulp.lpSum(patterns[i][j] * x[i] for i in range(len(patterns))) >= demands[j], f"Demand_Constraint_{j}"

#### Solve the problem
problem.solve()

#### Collecting results for the output
patterns_used = [{"pattern": patterns[i], "amount": int(x[i].varValue)} for i in range(len(patterns)) if x[i].varValue > 0]
total_large_rolls_used = int(pulp.value(problem.objective))

#### Output data
output = {
    "patterns": patterns_used,
    "total_large_rolls_used": total_large_rolls_used
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

