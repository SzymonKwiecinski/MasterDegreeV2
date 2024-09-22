# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MILP

PROBLEM INFO: 
- A hospital wants to make a weekly night shift (12pm-8am) schedule for its nurses. 
- The demand for nurses for the night shift on day \var{j} = 1,...,7 is an integer \var{d_j}. 
- Every nurse works \var{period} days in a row on the night shift, followed by (7 - \var{period}) days off.


INPUT FORMAT: 

{
    "period": period,
    "demand": [d_j for j in 1, ...,7]
}

OBJECTIVE: The goal is to find the minimal number of nurses the hospital needs to hire. 

OUTPUT INFO: 

- for each day \var{j} = 1,...,7, \var{start_j} which shows the number of nurses that start their period on day \var{j}.
- the total number of nurses hired.

OUTPUT FORMAT:

{
    "start": [start_j for j in 1, ...,7],
    "total": total
}


</DESCRIPTION>
<DATA>
{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}

#### Parameters
T = data['T']
period = data['Period']
demand = data['Demand']

#### Define the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

#### Decision Variables
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')

#### Objective Function: Minimize the total number of nurses hired
total_nurses = pulp.lpSum([start[j] for j in range(T)])
problem += total_nurses

#### Constraints
for j in range(T):
    #### Demand must be satisfied for each day
    problem += (pulp.lpSum(start[(j - k) % T] for k in range(period)) >= demand[j]), f"Demand_Constraint_Day_{j}"

#### Solve the problem
problem.solve()

#### Get results
result = {
    "start": [int(start[j].value()) for j in range(T)],
    "total": int(pulp.value(problem.objective))
}

#### Output
print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

