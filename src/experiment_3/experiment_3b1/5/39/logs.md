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

\section*{Linear Programming Model for Cafeteria Staffing}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( N \) be the total number of days considered.
    \item Let \( num_n \) be the number of employees required on day \( n \) where \( n = 1, 2, \ldots, N \).
    \item Let \( n_{\text{working}} \) be the number of consecutive working days for each employee.
    \item Let \( n_{\text{resting}} \) be the number of consecutive resting days for each employee.
    \item Let \( T = n_{\text{working}} + n_{\text{resting}} \) be the total cycle length for each employee.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( x \) be the total number of employees hired.
    \item Let \( is\_work_{n,i} \) be a binary variable that indicates whether employee \( i \) is working on day \( n \) (1 if working, 0 if resting).
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of employees to hire:
\[
\text{Minimize } x
\]

\subsection*{Constraints}
1. Staffing requirements:
\[
\sum_{i=1}^{x} is\_work_{n,i} \geq num_n, \quad \forall n = 1, 2, \ldots, N
\]

2. Employee working pattern:
Each employee works \( n_{\text{working}} \) days and then rests for \( n_{\text{resting}} \) days. Thus, for each employee \( i \):
\[
is\_work_{n,i} = 1 \quad \text{for } n = k(T) + 1, \ldots, k(T + n_{\text{working}}) \text{ for } k \in \mathbb{Z}
\]
\[
is\_work_{n,i} = 0 \quad \text{for } n = k(T + n_{\text{working}} + 1), \ldots, k(T + n_{\text{working}} + n_{\text{resting}}) \text{ for } k \in \mathbb{Z}
\]

3. Binary constraints:
\[
is\_work_{n,i} \in \{0, 1\}, \quad \forall n = 1, 2, \ldots, N, \, i = 1, 2, \ldots, x
\]

\subsection*{Output}
The output should provide:
\begin{itemize}
    \item \( total\_number \): the total number of employees to employ.
    \item \( is\_work \): a matrix of size \( N \times total\_number \) indicating the working status of each employee on each day.
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

\section*{Linear Programming Model for Cafeteria Staffing}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( N \) be the total number of days considered.
    \item Let \( num_n \) be the number of employees required on day \( n \) where \( n = 1, 2, \ldots, N \).
    \item Let \( n_{\text{working}} \) be the number of consecutive working days for each employee.
    \item Let \( n_{\text{resting}} \) be the number of consecutive resting days for each employee.
    \item Let \( T = n_{\text{working}} + n_{\text{resting}} \) be the total cycle length for each employee.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( x \) be the total number of employees hired.
    \item Let \( is\_work_{n,i} \) be a binary variable that indicates whether employee \( i \) is working on day \( n \) (1 if working, 0 if resting).
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of employees to hire:
\[
\text{Minimize } x
\]

\subsection*{Constraints}
1. Staffing requirements:
\[
\sum_{i=1}^{x} is\_work_{n,i} \geq num_n, \quad \forall n = 1, 2, \ldots, N
\]

2. Employee working pattern:
Each employee works \( n_{\text{working}} \) days and then rests for \( n_{\text{resting}} \) days. Thus, for each employee \( i \):
\[
is\_work_{n,i} = 1 \quad \text{for } n = k(T) + 1, \ldots, k(T + n_{\text{working}}) \text{ for } k \in \mathbb{Z}
\]
\[
is\_work_{n,i} = 0 \quad \text{for } n = k(T + n_{\text{working}} + 1), \ldots, k(T + n_{\text{working}} + n_{\text{resting}}) \text{ for } k \in \mathbb{Z}
\]

3. Binary constraints:
\[
is\_work_{n,i} \in \{0, 1\}, \quad \forall n = 1, 2, \ldots, N, \, i = 1, 2, \ldots, x
\]

\subsection*{Output}
The output should provide:
\begin{itemize}
    \item \( total\_number \): the total number of employees to employ.
    \item \( is\_work \): a matrix of size \( N \times total\_number \) indicating the working status of each employee on each day.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Given data
data = {
    'num': [5, 10, 2, 3, 2, 10],
    'n_working_days': 5,
    'n_resting_days': 2
}

N = len(data['num'])  #### Total number of days
num_n = data['num']  #### Number of employees required each day
n_working = data['n_working_days']  #### Number of consecutive working days
n_resting = data['n_resting_days']  #### Number of consecutive resting days
T = n_working + n_resting  #### Total cycle length

#### Create the LP problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable("total_employees", lowBound=0, cat='Integer')  #### Total number of employees hired
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')  #### Assume a max of 100 employees

#### Objective Function
problem += x, "Minimize total number of employees"

#### Constraints - Staffing requirements
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(100)) >= num_n[n], f"Staffing_requirement_day_{n+1}"

#### Employee working pattern constraints
for i in range(100):
    for k in range((N // T) + 1):  #### Calculate how many full cycles fit in N
        for w in range(n_working):
            if k * T + w < N:
                problem += is_work[k * T + w][i] == 1, f"Employee_{i+1}_working_day_{k*T+w+1}"
        for r in range(n_resting):
            if k * T + n_working + r < N:
                problem += is_work[k * T + n_working + r][i] == 0, f"Employee_{i+1}_resting_day_{k*T+n_working+r+1}"

#### Solve the problem
problem.solve()

#### Output
total_number = int(pulp.value(x))
is_work_matrix = [[int(is_work[n][i].varValue) for i in range(total_number)] for n in range(N)]

print(f'Total number of employees to hire: {total_number}')
print('Working status matrix (days x employees):')
for row in is_work_matrix:
    print(row)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

