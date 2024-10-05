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

\section*{Cafeteria Staffing Problem}

\subsection*{Parameters}
Let:
\begin{itemize}
    \item $N$: The total number of days.
    \item $num_n$: The number of employees required on day $n$ for $n = 1, \ldots, N$.
    \item $n_{\text{working}}$: The number of consecutive working days for each employee.
    \item $n_{\text{resting}}$: The number of consecutive resting days for each employee.
\end{itemize}

\subsection*{Decision Variables}
Define binary decision variables:
\begin{itemize}
    \item $x_i$: A binary variable that equals 1 if employee $i$ works on day $n$, and 0 otherwise.
\end{itemize}

Let $T$ be the total number of employees to hire.

\subsection*{Objective Function}
The objective is to minimize the total number of employees hired:
\[
\text{Minimize } T
\]

\subsection*{Constraints}
For each day $n = 1, \ldots, N$, the following constraints must hold:
\[
\sum_{i=1}^{T} x_{n,i} \geq num_n \quad \forall n = 1, \ldots, N
\]

\subsubsection*{Working and Resting Days Constraints}
Each employee $i$ can work for $n_{\text{working}}$ days followed by $n_{\text{resting}}$ days. Therefore, for any employee $i$, we have:
\[
x_{n,i} + x_{n+1,i} + \ldots + x_{n_{\text{working}},i} \leq n_{\text{working}} \quad \forall n \text{ such that } 1 \leq n \leq N - n_{\text{working}} + 1
\]
\[
x_{n+ n_{\text{working}},i} + x_{n+ n_{\text{working}} + 1,i} + \ldots + x_{n+ n_{\text{working}} + n_{\text{resting}} - 1,i} = 0 \quad \forall n \text{ such that } 1 \leq n \leq N - n_{\text{working}} - n_{\text{resting}} + 1
\]

\subsection*{Output Variables}
\begin{itemize}
    \item Let $total\_number = T$
    \item Let $is\_work_{n,i} = x_{n,i}$
\end{itemize}

\subsection*{Output Format}
The output will be:
\[
\begin{align*}
\{ \\
\quad total\_number: total\_number, \\
\quad is\_work: [is\_work_{n,i} \text{ for } n = 1, \ldots, N \text{ and } i = 1, \ldots, total\_number] \\
\}
\end{align*}
\]

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

\section*{Cafeteria Staffing Problem}

\subsection*{Parameters}
Let:
\begin{itemize}
    \item $N$: The total number of days.
    \item $num_n$: The number of employees required on day $n$ for $n = 1, \ldots, N$.
    \item $n_{\text{working}}$: The number of consecutive working days for each employee.
    \item $n_{\text{resting}}$: The number of consecutive resting days for each employee.
\end{itemize}

\subsection*{Decision Variables}
Define binary decision variables:
\begin{itemize}
    \item $x_i$: A binary variable that equals 1 if employee $i$ works on day $n$, and 0 otherwise.
\end{itemize}

Let $T$ be the total number of employees to hire.

\subsection*{Objective Function}
The objective is to minimize the total number of employees hired:
\[
\text{Minimize } T
\]

\subsection*{Constraints}
For each day $n = 1, \ldots, N$, the following constraints must hold:
\[
\sum_{i=1}^{T} x_{n,i} \geq num_n \quad \forall n = 1, \ldots, N
\]

\subsubsection*{Working and Resting Days Constraints}
Each employee $i$ can work for $n_{\text{working}}$ days followed by $n_{\text{resting}}$ days. Therefore, for any employee $i$, we have:
\[
x_{n,i} + x_{n+1,i} + \ldots + x_{n_{\text{working}},i} \leq n_{\text{working}} \quad \forall n \text{ such that } 1 \leq n \leq N - n_{\text{working}} + 1
\]
\[
x_{n+ n_{\text{working}},i} + x_{n+ n_{\text{working}} + 1,i} + \ldots + x_{n+ n_{\text{working}} + n_{\text{resting}} - 1,i} = 0 \quad \forall n \text{ such that } 1 \leq n \leq N - n_{\text{working}} - n_{\text{resting}} + 1
\]

\subsection*{Output Variables}
\begin{itemize}
    \item Let $total\_number = T$
    \item Let $is\_work_{n,i} = x_{n,i}$
\end{itemize}

\subsection*{Output Format}
The output will be:
\[
\begin{align*}
\{ \\
\quad total\_number: total\_number, \\
\quad is\_work: [is\_work_{n,i} \text{ for } n = 1, \ldots, N \text{ and } i = 1, \ldots, total\_number] \\
\}
\end{align*}
\]

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Problem data based on given JSON
data = {
    'num': [5, 10, 2, 3, 2, 10],
    'n_working_days': 5,
    'n_resting_days': 2
}

#### Extracting data values
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

#### Create a Linear Programming Problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

#### Decision variable for the total number of employees
T = pulp.LpVariable('T', lowBound=0, cat='Integer')

#### Decision variables for employees working on a particular day
x = pulp.LpVariable.dicts("x", ((n, i) for n in range(N) for i in range(100)), cat='Binary')

#### Objective: Minimize the total number of employees
problem += T

#### Constraints: Ensure enough employees are working per day
for n in range(N):
    problem += pulp.lpSum(x[n, i] for i in range(100)) >= num[n]

#### Constraints: Working and resting schedule
for i in range(100):
    for n in range(N - n_working_days + 1):
        problem += pulp.lpSum(x[n + k, i] for k in range(n_working_days)) <= n_working_days

    for n in range(N - n_working_days - n_resting_days + 1):
        problem += pulp.lpSum(x[n + n_working_days + k, i] for k in range(n_resting_days)) == 0

#### Linking T with the actual number of employees required
for i in range(100):
    problem += pulp.lpSum(x[n, i] for n in range(N)) <= T * N  #### To limit by T

#### Solve the problem
problem.solve()

#### Gathering output
total_number = int(pulp.value(T))
is_work = [[int(pulp.value(x[n, i])) for i in range(total_number)] for n in range(N)]

#### Printing the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print("{")
print(f"  total_number: {total_number},")
print(f"  is_work: {is_work}")
print("}")
```

