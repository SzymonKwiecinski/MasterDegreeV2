# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
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


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Nurse Scheduling}

\textbf{Parameters:}
\begin{itemize}
    \item $p$: Period (number of days a nurse works in a row)
    \item $d_j$: Demand for nurses on day $j$, for $j = 1, \ldots, 7$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_j$: Number of nurses that start their shift on day $j$, for $j = 1, \ldots, 7$
    \item $N$: Total number of nurses hired
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } N = \sum_{j=1}^{7} x_j
\]

\textbf{Constraints:}
\begin{itemize}
    \item For each day $j$, the demand must be satisfied:
    \[
    \sum_{i=0}^{p-1} x_{(j-i \mod 7)} \geq d_j, \quad \forall j = 1, \ldots, 7
    \]
    where we take into account that a nurse who starts on day $j-i$ works for $p$ consecutive days.
    
    \item Non-negativity constraint:
    \[
    x_j \geq 0 \quad \forall j = 1, \ldots, 7
    \]
\end{itemize}

\textbf{Output:}
\begin{itemize}
    \item $start = [x_1, x_2, x_3, x_4, x_5, x_6, x_7]$
    \item $total = N$
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

\section*{Mathematical Model for Nurse Scheduling}

\textbf{Parameters:}
\begin{itemize}
    \item $p$: Period (number of days a nurse works in a row)
    \item $d_j$: Demand for nurses on day $j$, for $j = 1, \ldots, 7$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_j$: Number of nurses that start their shift on day $j$, for $j = 1, \ldots, 7$
    \item $N$: Total number of nurses hired
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } N = \sum_{j=1}^{7} x_j
\]

\textbf{Constraints:}
\begin{itemize}
    \item For each day $j$, the demand must be satisfied:
    \[
    \sum_{i=0}^{p-1} x_{(j-i \mod 7)} \geq d_j, \quad \forall j = 1, \ldots, 7
    \]
    where we take into account that a nurse who starts on day $j-i$ works for $p$ consecutive days.
    
    \item Non-negativity constraint:
    \[
    x_j \geq 0 \quad \forall j = 1, \ldots, 7
    \]
\end{itemize}

\textbf{Output:}
\begin{itemize}
    \item $start = [x_1, x_2, x_3, x_4, x_5, x_6, x_7]$
    \item $total = N$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
p = data['Period']
demand = data['Demand']

#### Create the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(1, T + 1), lowBound=0, cat='Integer')
N = pulp.LpVariable("N", lowBound=0, cat='Integer')

#### Objective Function
problem += N

#### Constraints
for j in range(1, T + 1):
    problem += pulp.lpSum(x[(j - i) % T + 1] for i in range(p)) >= demand[j - 1], f"Demand_Constraint_{j}"

#### Total Nurses
problem += N == pulp.lpSum(x[j] for j in range(1, T + 1)), "Total_Nurses"

#### Solve the problem
problem.solve()

#### Output
start = [x[j].varValue for j in range(1, T + 1)]
total = pulp.value(N)

print(f' (Objective Value): <OBJ>{total}</OBJ>')
print(f'Start: {start}')
```

