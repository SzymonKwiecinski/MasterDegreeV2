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
To solve the problem of determining the minimum number of employees needed to meet the staffing requirements in the cafeteria while considering the specified working and resting pattern, we can formulate it as an Integer Linear Programming (ILP) problem. Here's the formulation of the problem in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsfonts}
\begin{document}

\section*{Mathematical Model}

\subsection*{Indices}
\begin{align*}
n & : \text{Index for days, where } n = 1, \ldots, N \\
i & : \text{Index for employees, where } i = 1, \ldots, I 
\end{align*}

\subsection*{Parameters}
\begin{align*}
\text{num}[n] & : \text{Number of employees required on day } n \\
n_{\text{working\_days}} & : \text{Number of consecutive working days} \\
n_{\text{resting\_days}} & : \text{Number of consecutive resting days}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
x_i & : \text{Binary variable, 1 if employee } i \text{ is hired, 0 otherwise} \\
\text{is\_work}_{n,i} & : \text{Binary variable, 1 if employee } i \text{ works on day } n, 0 \text{ otherwise}
\end{align*}

\subsection*{Objective Function}
Minimize the total number of employees hired:
\begin{align*}
\min \sum_{i=1}^{I} x_i
\end{align*}

\subsection*{Constraints}
\begin{align}
\sum_{i=1}^{I} \text{is\_work}_{n,i} & \geq \text{num}[n], \quad \forall n = 1, \ldots, N \\
\text{is\_work}_{n,i} & \leq x_i, \quad \forall n = 1, \ldots, N, \forall i = 1, \ldots, I \\
\sum_{k=0}^{n_{\text{working\_days}}-1} \text{is\_work}_{n+k,i} & = n_{\text{working\_days}} \cdot y_{n,i}, \quad \forall n = 1, \ldots, N, \forall i = 1, \ldots, I \\
\sum_{k=n_{\text{working\_days}}}^{n_{\text{working\_days}}+n_{\text{resting\_days}}-1} \text{is\_work}_{n+k,i} & = 0, \quad \forall n = 1, \ldots, N, \forall i = 1, \ldots, I
\end{align}

\subsection*{Explanation}
\begin{itemize}
    \item Constraint (1) ensures that for each day \( n \), the required number of employees are working.
    \item Constraint (2) ensures that an employee \( i \) can work only if they are hired.
    \item Constraints (3) and (4) manage the block of \( n_{\text{working\_days}} \) working days followed by \( n_{\text{resting\_days}} \) resting days for each employee.
\end{itemize}

\end{document}
```

This ILP model uses binary decision variables to determine the working and rest days for each employee, while minimizing the total number of employees needed to satisfy daily staffing requirements. Constraints ensure that each employee follows the necessary cycle of consecutive working and rest days.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsfonts}
\begin{document}

\section*{Mathematical Model}

\subsection*{Indices}
\begin{align*}
n & : \text{Index for days, where } n = 1, \ldots, N \\
i & : \text{Index for employees, where } i = 1, \ldots, I 
\end{align*}

\subsection*{Parameters}
\begin{align*}
\text{num}[n] & : \text{Number of employees required on day } n \\
n_{\text{working\_days}} & : \text{Number of consecutive working days} \\
n_{\text{resting\_days}} & : \text{Number of consecutive resting days}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
x_i & : \text{Binary variable, 1 if employee } i \text{ is hired, 0 otherwise} \\
\text{is\_work}_{n,i} & : \text{Binary variable, 1 if employee } i \text{ works on day } n, 0 \text{ otherwise}
\end{align*}

\subsection*{Objective Function}
Minimize the total number of employees hired:
\begin{align*}
\min \sum_{i=1}^{I} x_i
\end{align*}

\subsection*{Constraints}
\begin{align}
\sum_{i=1}^{I} \text{is\_work}_{n,i} & \geq \text{num}[n], \quad \forall n = 1, \ldots, N \\
\text{is\_work}_{n,i} & \leq x_i, \quad \forall n = 1, \ldots, N, \forall i = 1, \ldots, I \\
\sum_{k=0}^{n_{\text{working\_days}}-1} \text{is\_work}_{n+k,i} & = n_{\text{working\_days}} \cdot y_{n,i}, \quad \forall n = 1, \ldots, N, \forall i = 1, \ldots, I \\
\sum_{k=n_{\text{working\_days}}}^{n_{\text{working\_days}}+n_{\text{resting\_days}}-1} \text{is\_work}_{n+k,i} & = 0, \quad \forall n = 1, \ldots, N, \forall i = 1, \ldots, I
\end{align}

\subsection*{Explanation}
\begin{itemize}
    \item Constraint (1) ensures that for each day \( n \), the required number of employees are working.
    \item Constraint (2) ensures that an employee \( i \) can work only if they are hired.
    \item Constraints (3) and (4) manage the block of \( n_{\text{working\_days}} \) working days followed by \( n_{\text{resting\_days}} \) resting days for each employee.
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
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

N = len(num)  #### Number of days
I = 6  #### Number of employees (assuming as per length of num)

#### Create the problem
problem = pulp.LpProblem("EmployeeScheduling", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(I), cat='Binary')  #### Hiring decision
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(I)), cat='Binary')  #### Work schedule

#### Objective Function
problem += pulp.lpSum([x[i] for i in range(I)])

#### Constraints
#### (1) Ensure the required number of employees work each day
for n in range(N):
    problem += pulp.lpSum([is_work[n][i] for i in range(I)]) >= num[n]

#### (2) An employee can only work if they are hired
for n in range(N):
    for i in range(I):
        problem += is_work[n][i] <= x[i]

#### (3) Working days follow a set pattern
for n in range(N - n_working_days + 1):
    for i in range(I):
        problem += pulp.lpSum([is_work[n + k][i] for k in range(n_working_days)]) == n_working_days * x[i]

#### (4) Resting days after working days
for n in range(N - n_working_days - n_resting_days + 1):
    for i in range(I):
        problem += pulp.lpSum([is_work[n + k][i] for k in range(n_working_days, n_working_days + n_resting_days)]) == 0

#### Solve the problem
problem.solve()

#### Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

