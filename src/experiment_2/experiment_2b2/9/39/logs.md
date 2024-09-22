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

#### Data from input
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

#### Unpack data
num_employees_required = data["num"]
n_working_days = data["n_working_days"]
n_resting_days = data["n_resting_days"]
N = len(num_employees_required)

#### Define the LP problem
problem = pulp.LpProblem("Minimum_Employees_Hiring", pulp.LpMinimize)

#### Decision variables
#### Let's assume a large enough upper bound for the number of employees
max_possible_employees = sum(num_employees_required)
is_work = [
    [
        pulp.LpVariable(f"is_work_{i}_{n}", cat='Binary')
        for n in range(N)
    ]
    for i in range(max_possible_employees)
]

#### Objective function
#### Minimize total number of employees hired
total_number = pulp.LpVariable("total_number", lowBound=0, cat="Continuous")
problem += total_number

#### Constraints
#### Each day n must have at least num_employees_required[n] employees working
for n in range(N):
    problem += pulp.lpSum(is_work[i][n] for i in range(max_possible_employees)) >= num_employees_required[n]

#### Working and resting pattern constraint
for i in range(max_possible_employees):
    for n in range(N):
        if n + n_working_days + n_resting_days <= N:
            #### If working day starts on day n, ensure it forms a cycle with working and resting days
            for j in range(n_working_days):
                problem += is_work[i][n + j] <= 1
            for j in range(n_working_days, n_working_days + n_resting_days):
                problem += is_work[i][n + j] == 0

#### Additional constraint to link total_number with actual employee usage
for i in range(max_possible_employees):
    for n in range(N):
        problem += total_number >= is_work[i][n]

#### Solve the problem
problem.solve()

#### Extract the results
hired_employees = [
    [int(pulp.value(is_work[i][n])) for n in range(N)]
    for i in range(max_possible_employees)
]

#### Filter out employees who are not working at all
final_hired_employees = [emp for emp in hired_employees if sum(emp) > 0]

output = {
    "total_number": len(final_hired_employees),
    "is_work": final_hired_employees
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

