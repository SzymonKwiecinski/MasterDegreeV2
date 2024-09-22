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

\section*{Mathematical Model of the Nurse Scheduling Problem}

\subsection*{Parameters}
\begin{itemize}
    \item $period$: Number of days each nurse works in a row on the night shift.
    \item $d_j$: Demand for nurses on day $j$, where $j = 1, \ldots, 7$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $start_j$: Number of nurses that start their period on day $j$, where $j = 1, \ldots, 7$.
    \item $N$: Total number of nurses hired.
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of nurses hired:
\[
\text{Minimize } N = \sum_{j=1}^{7} start_j
\]

\subsection*{Constraints}
For each day $j$:
\[
\sum_{i=0}^{period-1} start_{(j-i) \mod 7} \geq d_j \quad \forall j \in \{1, 2, \ldots, 7\}
\]

Where $start_k = 0$ for $k \leq 0$ to account for the circular nature of the week.

\subsection*{Output}
The output will consist of:
\begin{itemize}
    \item A list $start = [start_1, start_2, \ldots, start_7]$ which denotes the number of nurses starting on each day.
    \item The total number of nurses hired $total = N$.
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

\section*{Mathematical Model of the Nurse Scheduling Problem}

\subsection*{Parameters}
\begin{itemize}
    \item $period$: Number of days each nurse works in a row on the night shift.
    \item $d_j$: Demand for nurses on day $j$, where $j = 1, \ldots, 7$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $start_j$: Number of nurses that start their period on day $j$, where $j = 1, \ldots, 7$.
    \item $N$: Total number of nurses hired.
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of nurses hired:
\[
\text{Minimize } N = \sum_{j=1}^{7} start_j
\]

\subsection*{Constraints}
For each day $j$:
\[
\sum_{i=0}^{period-1} start_{(j-i) \mod 7} \geq d_j \quad \forall j \in \{1, 2, \ldots, 7\}
\]

Where $start_k = 0$ for $k \leq 0$ to account for the circular nature of the week.

\subsection*{Output}
The output will consist of:
\begin{itemize}
    \item A list $start = [start_1, start_2, \ldots, start_7]$ which denotes the number of nurses starting on each day.
    \item The total number of nurses hired $total = N$.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided
data = {
    'T': 7,
    'Period': 4,
    'Demand': [0, 5, 9, 15, 4, 7, 3]
}

#### Extract data
T = data['T']
period = data['Period']
demand = data['Demand']

#### Initialize the problem
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

#### Decision Variables
start_vars = [pulp.LpVariable(f'start_{j}', lowBound=0, cat='Integer') for j in range(T)]
total_nurses = pulp.LpVariable('total_nurses', lowBound=0, cat='Integer')

#### Objective Function
problem += total_nurses, "Minimize total number of nurses"

#### Total nurses constraint
problem += total_nurses == pulp.lpSum(start_vars), "Total nurses constraint"

#### Constraints for each day
for j in range(T):
    problem += pulp.lpSum(start_vars[(j-i) % T] for i in range(period)) >= demand[j], f"Demand_constraint_day_{j+1}"

#### Solve the problem
problem.solve()

#### Output results
start_values = [pulp.value(var) for var in start_vars]
total_nurses_hired = pulp.value(total_nurses)

print("Number of nurses starting each day:", start_values)
print("Total number of nurses hired:", total_nurses_hired)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

