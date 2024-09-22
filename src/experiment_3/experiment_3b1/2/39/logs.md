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

\section*{Mathematical Model for Cafeteria Staffing Problem}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( N \) be the total number of days.
    \item Let \( num_n \) be the number of employees required on day \( n \) for \( n = 1, 2, \ldots, N \).
    \item Let \( n_{\text{working}} \) be the number of consecutive working days for each employee.
    \item Let \( n_{\text{resting}} \) be the number of consecutive resting days for each employee.
    \item Let \( T = n_{\text{working}} + n_{\text{resting}} \) be the total cycle length for each employee.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( total\_number \) be the total number of employees to hire.
    \item Let \( is\_work_{n, i} \) be a binary variable that indicates whether employee \( i \) is working on day \( n \):
    \[
    is\_work_{n, i} =
    \begin{cases}
      1 & \text{if employee } i \text{ works on day } n \\
      0 & \text{otherwise}
    \end{cases}
    \end{equation*}
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of employees hired:
\[
\text{Minimize } total\_number
\]

\subsection*{Constraints}
For each day \( n = 1, 2, \ldots, N \):
\[
\sum_{i=1}^{total\_number} is\_work_{n, i} \geq num_n
\]

For each employee \( i \):
\begin{equation}
is\_work_{n, i} \text{ must satisfy the working/resting schedule}
\end{equation}
This implies that if an employee works on day \( n \), they must work for \( n_{\text{working}} \) days and then rest for \( n_{\text{resting}} \) days, creating the following constraints:
\[
is\_work_{n, i} + is\_work_{n+1, i} + \ldots + is\_work_{n+n_{\text{working}}-1, i} = n_{\text{working}} \quad \text{for } n \text{ such that } n + n_{\text{working}} - 1 \leq N
\]
\[
is\_work_{n+n_{\text{working}}, i} + is\_work_{n+n_{\text{working}}+1, i} + \ldots + is\_work_{n+n_{\text{working}}+n_{\text{resting}}-1, i} = 0 \quad \text{for } n \text{ such that } n+n_{\text{working}} + n_{\text{resting}} - 1 \leq N
\]

\subsection*{Output}
The output will consist of:
\begin{itemize}
    \item \( total\_number \): Total number of employees hired.
    \item \( is\_work \): A matrix where \( is\_work[n][i] \) indicates whether employee \( i \) is working on day \( n \).
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

\section*{Mathematical Model for Cafeteria Staffing Problem}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( N \) be the total number of days.
    \item Let \( num_n \) be the number of employees required on day \( n \) for \( n = 1, 2, \ldots, N \).
    \item Let \( n_{\text{working}} \) be the number of consecutive working days for each employee.
    \item Let \( n_{\text{resting}} \) be the number of consecutive resting days for each employee.
    \item Let \( T = n_{\text{working}} + n_{\text{resting}} \) be the total cycle length for each employee.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( total\_number \) be the total number of employees to hire.
    \item Let \( is\_work_{n, i} \) be a binary variable that indicates whether employee \( i \) is working on day \( n \):
    \[
    is\_work_{n, i} =
    \begin{cases}
      1 & \text{if employee } i \text{ works on day } n \\
      0 & \text{otherwise}
    \end{cases}
    \end{equation*}
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of employees hired:
\[
\text{Minimize } total\_number
\]

\subsection*{Constraints}
For each day \( n = 1, 2, \ldots, N \):
\[
\sum_{i=1}^{total\_number} is\_work_{n, i} \geq num_n
\]

For each employee \( i \):
\begin{equation}
is\_work_{n, i} \text{ must satisfy the working/resting schedule}
\end{equation}
This implies that if an employee works on day \( n \), they must work for \( n_{\text{working}} \) days and then rest for \( n_{\text{resting}} \) days, creating the following constraints:
\[
is\_work_{n, i} + is\_work_{n+1, i} + \ldots + is\_work_{n+n_{\text{working}}-1, i} = n_{\text{working}} \quad \text{for } n \text{ such that } n + n_{\text{working}} - 1 \leq N
\]
\[
is\_work_{n+n_{\text{working}}, i} + is\_work_{n+n_{\text{working}}+1, i} + \ldots + is\_work_{n+n_{\text{working}}+n_{\text{resting}}-1, i} = 0 \quad \text{for } n \text{ such that } n+n_{\text{working}} + n_{\text{resting}} - 1 \leq N
\]

\subsection*{Output}
The output will consist of:
\begin{itemize}
    \item \( total\_number \): Total number of employees hired.
    \item \( is\_work \): A matrix where \( is\_work[n][i] \) indicates whether employee \( i \) is working on day \( n \).
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

N = len(data['num'])  #### Total number of days
num_n = data['num']  #### Employees required on each day
n_working_days = data['n_working_days']  #### Consecutive working days
n_resting_days = data['n_resting_days']  #### Consecutive resting days
T = n_working_days + n_resting_days  #### Total cycle length

#### Problem Definition
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

#### Decision Variables
total_number = pulp.LpVariable('total_number', lowBound=1, cat='Integer')  #### Total employees
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')  #### Assume a maximum of 100 employees for initial setup

#### Objective Function
problem += total_number, "Minimize_Total_Employees"

#### Constraints for minimum employees required
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(100)) >= num_n[n], f"Req_Employees_Day_{n+1}"

#### Constraints for working/resting schedule
for i in range(100):  #### For each employee
    for n in range(N - n_working_days + 1):
        problem += pulp.lpSum(is_work[n+k][i] for k in range(n_working_days)) == n_working_days, f"Working_Days_Employee_{i}_Start_{n+1}"
    
    for n in range(N - n_working_days - n_resting_days + 1):
        problem += pulp.lpSum(is_work[n + n_working_days + k][i] for k in range(n_resting_days)) == 0, f"Resting_Days_Employee_{i}_Start_{n+1}"

#### Calculate the total number of employees used
for i in range(100):
    problem += pulp.lpSum(is_work[n][i] for n in range(N)) <= total_number

#### Solve the problem
problem.solve()

#### Output
print(f'Total Employees Hired: {pulp.value(problem.objective)}')
for n in range(N):
    for i in range(100):
        if pulp.value(is_work[n][i]) == 1:
            print(f'Employee {i} works on day {n+1}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

