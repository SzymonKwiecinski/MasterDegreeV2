# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP or MILP
PROBLEM INFO:

- To operate a cafeteria, the manager must ensure on-call duty based on the statistics on the required staff. 
- In the future days, the number of desired employees on day \var{n} is denoted with \var{num_{n}}.
- Each employee works \var{n_working_days} days in a row and then has \var{n_resting_days} days off.

INPUT FORMAT:

{
	"num": [num_{n} for n in 1,...,N],
	"n_working_days": n_working_days,
	"n_resting_days": n_resting_days
}


OBJECTIVE: Calculate the minimum number of employees to hire

OUTPUT INFO:

- \var{total_number} represents the total number of employees to employ
- \var{is_work} represents whether employee is working a rest on each day. Its length is determined by \var{total_number}

OUTPUT FORMAT:

{
	"total_number": total_number,
	"is_work": [[is_work_{n, i} for n in 1,...,N] for i in 1,...,total_number]
}
</DESCRIPTION>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

#### Parameters extraction
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

#### Create the LP problem
problem = pulp.LpProblem("Cafeteria_Employee_Scheduling", pulp.LpMinimize)

#### Decision Variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')

#### Constraints
for n in range(N):
    #### Sum of employees working on day n should be >= num[n]
    problem += pulp.lpSum(is_work[n][i] for i in range(total_number)) >= num[n]

#### Each employee works n_working_days then rests n_resting_days
for i in range(100):  #### Assume a maximum of 100 employees for indexing
    for n in range(N):
        if n >= n_working_days:
            problem += is_work[n][i] + pulp.lpSum(is_work[j][i] for j in range(n - n_working_days, n)) <= 1
        else:
            problem += is_work[n][i] <= 1

#### Objective Function
problem += total_number, "Total Number of Employees"

#### Solve the problem
problem.solve()

#### Prepare the output
total_number_value = pulp.value(total_number)
is_work_matrix = [[pulp.value(is_work[n][i]) for n in range(N)] for i in range(100) if pulp.value(is_work[0][i]) is not None]

#### Output
output = {
    "total_number": total_number_value,
    "is_work": is_work_matrix
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

