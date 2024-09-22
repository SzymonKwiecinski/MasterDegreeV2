# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
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


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Employee Scheduling}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( N \) be the total number of days.
    \item Let \( \text{num}_{n} \) be the desired number of employees on day \( n \) for \( n = 1, \ldots, N \).
    \item Let \( n_{\text{working}} \) be the number of consecutive working days for each employee.
    \item Let \( n_{\text{resting}} \) be the number of consecutive resting days for each employee.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( \text{total\_number} \) be the total number of employees to hire.
    \item Let \( \text{is\_work}_{n, i} \) be a binary variable, where \( \text{is\_work}_{n, i} = 1 \) if employee \( i \) is working on day \( n \) and \( 0 \) otherwise.
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of employees:
\[
\text{minimize} \quad \text{total\_number}
\]

\subsection*{Constraints}
1. Ensure that the number of employees working on each day meets the requirement:
\[
\sum_{i=1}^{\text{total\_number}} \text{is\_work}_{n, i} \geq \text{num}_{n}, \quad \forall n \in \{1, \ldots, N\}
\]

2. Define the working and resting cycle for each employee:
\[
\text{is\_work}_{n, i} = 1 \quad \text{for } n = k(n_{\text{working}} + n_{\text{resting}}) + j, \quad \text{with } j = 0, \ldots, n_{\text{working}} - 1
\]
\[
\text{is\_work}_{n, i} = 0 \quad \text{for } n = k(n_{\text{working}} + n_{\text{resting}}) + j, \quad \text{with } j = n_{\text{working}}, \ldots, n_{\text{working}} + n_{\text{resting}} - 1
\]
where \( k \) is a non-negative integer determined by the employee's work cycle.

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Employee Scheduling}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( N \) be the total number of days.
    \item Let \( \text{num}_{n} \) be the desired number of employees on day \( n \) for \( n = 1, \ldots, N \).
    \item Let \( n_{\text{working}} \) be the number of consecutive working days for each employee.
    \item Let \( n_{\text{resting}} \) be the number of consecutive resting days for each employee.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( \text{total\_number} \) be the total number of employees to hire.
    \item Let \( \text{is\_work}_{n, i} \) be a binary variable, where \( \text{is\_work}_{n, i} = 1 \) if employee \( i \) is working on day \( n \) and \( 0 \) otherwise.
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of employees:
\[
\text{minimize} \quad \text{total\_number}
\]

\subsection*{Constraints}
1. Ensure that the number of employees working on each day meets the requirement:
\[
\sum_{i=1}^{\text{total\_number}} \text{is\_work}_{n, i} \geq \text{num}_{n}, \quad \forall n \in \{1, \ldots, N\}
\]

2. Define the working and resting cycle for each employee:
\[
\text{is\_work}_{n, i} = 1 \quad \text{for } n = k(n_{\text{working}} + n_{\text{resting}}) + j, \quad \text{with } j = 0, \ldots, n_{\text{working}} - 1
\]
\[
\text{is\_work}_{n, i} = 0 \quad \text{for } n = k(n_{\text{working}} + n_{\text{resting}}) + j, \quad \text{with } j = n_{\text{working}}, \ldots, n_{\text{working}} + n_{\text{resting}} - 1
\]
where \( k \) is a non-negative integer determined by the employee's work cycle.

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"num": [5, 10, 2, 3, 2, 10], "n_working_days": 5, "n_resting_days": 2}')
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

#### Problem definition
problem = pulp.LpProblem("EmployeeScheduling", pulp.LpMinimize)

#### Decision Variables
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')  #### 100 is a safe upper limit for employees

#### Objective Function
problem += total_number

#### Constraints for number of employees needed each day
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(100)) >= num[n], f"EmployeeRequirement_day_{n}"

#### Constraints for working and resting cycles for each employee
for i in range(100):  #### Iterate over possible employees
    for k in range((N // (n_working_days + n_resting_days)) + 1):  #### Calculate k for cycles
        for j in range(n_working_days):
            day = k * (n_working_days + n_resting_days) + j
            if day < N:
                problem += is_work[day][i] == 1, f"Work_day_{day}_employee_{i}"
        for j in range(n_working_days, n_working_days + n_resting_days):
            day = k * (n_working_days + n_resting_days) + j
            if day < N:
                problem += is_work[day][i] == 0, f"Rest_day_{day}_employee_{i}"

#### Constraint to define the total number of employees based on is_work variables
problem += total_number == pulp.lpSum(is_work[n][i] for n in range(N) for i in range(100)), "TotalEmployees"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

