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

\section*{Mathematical Model for Employee Scheduling in a Cafeteria}

\subsection*{Definitions}
Let:
\begin{itemize}
    \item $N$ be the total number of days.
    \item $num_n$ be the number of employees required on day $n$ where $n = 1, \ldots, N$.
    \item $n_{working}$ be the number of consecutive working days for each employee.
    \item $n_{resting}$ be the number of days off for each employee.
    \item $total\_number$ be the total number of employees to hire.
    \item $is\_work_{n, i}$ be a binary variable that indicates whether employee $i$ is working on day $n$.
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item $is\_work_{n, i} \in \{0, 1\}$ for all $n \in \{1, \ldots, N\}$ and $i \in \{1, \ldots, total\_number\}$
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of employees:
\[
\text{Minimize } total\_number
\]

\subsection*{Constraints}
1. Ensure that the required number of employees is met for each day:
\[
\sum_{i=1}^{total\_number} is\_work_{n, i} \geq num_n \quad \forall n \in \{1, \ldots, N\}
\]

2. Each employee works for $n_{working}$ days followed by $n_{resting}$ days. This can be enforced by using a block of variables:
\[
is\_work_{n, i} = 
\begin{cases} 
1 & \text{if } n \mod (n_{working} + n_{resting}) < n_{working} \\
0 & \text{otherwise}
\end{cases}
\]

3. Ensure that the binary variable does not exceed the working limit:
\[
\sum_{n=1}^{N} is\_work_{n, i} \leq n_{working} \quad \forall i \in \{1, \ldots, total\_number\}
\]

4. Ensure an employee rests for $n_{resting}$ days after $n_{working}$ days:
\[
is\_work_{n, i} + is\_work_{n + d, i} \leq 1 \quad \forall i, d \text{ where } d \in \{1, \ldots, n_{resting}\}, n + d \leq N
\]

\subsection*{Output}
The solution includes:
\begin{itemize}
    \item The value of $total\_number$ representing the total number of employees to employ.
    \item A matrix $is\_work$ where $is\_work_{n, i}$ indicates whether employee $i$ works on day $n$.
\end{itemize}

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

\section*{Mathematical Model for Employee Scheduling in a Cafeteria}

\subsection*{Definitions}
Let:
\begin{itemize}
    \item $N$ be the total number of days.
    \item $num_n$ be the number of employees required on day $n$ where $n = 1, \ldots, N$.
    \item $n_{working}$ be the number of consecutive working days for each employee.
    \item $n_{resting}$ be the number of days off for each employee.
    \item $total\_number$ be the total number of employees to hire.
    \item $is\_work_{n, i}$ be a binary variable that indicates whether employee $i$ is working on day $n$.
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item $is\_work_{n, i} \in \{0, 1\}$ for all $n \in \{1, \ldots, N\}$ and $i \in \{1, \ldots, total\_number\}$
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of employees:
\[
\text{Minimize } total\_number
\]

\subsection*{Constraints}
1. Ensure that the required number of employees is met for each day:
\[
\sum_{i=1}^{total\_number} is\_work_{n, i} \geq num_n \quad \forall n \in \{1, \ldots, N\}
\]

2. Each employee works for $n_{working}$ days followed by $n_{resting}$ days. This can be enforced by using a block of variables:
\[
is\_work_{n, i} = 
\begin{cases} 
1 & \text{if } n \mod (n_{working} + n_{resting}) < n_{working} \\
0 & \text{otherwise}
\end{cases}
\]

3. Ensure that the binary variable does not exceed the working limit:
\[
\sum_{n=1}^{N} is\_work_{n, i} \leq n_{working} \quad \forall i \in \{1, \ldots, total\_number\}
\]

4. Ensure an employee rests for $n_{resting}$ days after $n_{working}$ days:
\[
is\_work_{n, i} + is\_work_{n + d, i} \leq 1 \quad \forall i, d \text{ where } d \in \{1, \ldots, n_{resting}\}, n + d \leq N
\]

\subsection*{Output}
The solution includes:
\begin{itemize}
    \item The value of $total\_number$ representing the total number of employees to employ.
    \item A matrix $is\_work$ where $is\_work_{n, i}$ indicates whether employee $i$ works on day $n$.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads("{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}")
num_n = data['num']
n_working = data['n_working_days']
n_resting = data['n_resting_days']
N = len(num_n)

#### Define the problem
problem = pulp.LpProblem("Employee_Scheduling", pulp.LpMinimize)

#### Define the total number of employees variable
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')

#### Define the binary decision variables
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(total_number.name)), cat='Binary')

#### Objective function: Minimize the number of employees
problem += total_number, "Minimize_Total_Employees"

#### Constraints to ensure required employees for each day
for n in range(N):
    problem += (pulp.lpSum(is_work[n][i] for i in range(total_number)) >= num_n[n]), f"Employee_Requirement_Day_{n+1}"

#### Constraints for working and resting days for each employee
for i in range(total_number):
    #### Each employee should not exceed the working limit
    problem += (pulp.lpSum(is_work[n][i] for n in range(N)) <= n_working, f"Max_Work_Days_Employee_{i+1}")

    #### Enforce resting days
    for n in range(N - n_working - n_resting):
        for d in range(1, n_resting + 1):
            problem += (is_work[n][i] + is_work[n + d][i] <= 1, f"Rest_Employee_{i+1}_Day_{n+1}_After_Rest_{d}")

#### Solve the problem
problem.solve()

#### Output the results
total_employees = pulp.value(total_number)
print(f' (Objective Value): <OBJ>{total_employees}</OBJ>')

#### Optionally, you can also print the work schedule matrix
schedule_matrix = [[pulp.value(is_work[n][i]) for i in range(total_employees)] for n in range(N)]
print("Schedule Matrix:")
for row in schedule_matrix:
    print(row)
```

