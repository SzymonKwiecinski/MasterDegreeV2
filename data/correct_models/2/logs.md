# START: OR_ModelCreator 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. You receive task description between <TASK_DESCRIPTION> and </TASK_DESCRIPTION>. You receive target objective between <OBJECTIVE> and </OBJECTIVE>. You receive description of constraints between <CONSTRAINTS> and </CONSTRAINTS>. You receive all 'parameters' which you have to use in model with symbol and shape between <PARAMETERS> and </PARAMETERS>. 
## START MESSAGE 0 
### ROLE: Role.USER
<TASK_DESCRIPTION>: A hospital is trying to determine the minimal number of nurses to hire over a planning period to meet the daily demand for nursing staff.</TASK_DESCRIPTION>.
<OBJECTIVE>: Minimize the number of nurses that the hospital needs to hire for the planning period </OBJECTIVE>
<CONSTRAINTS>
<CONSTRAINT>Number of nurses is non-negative</CONSTRAINT>
<CONSTRAINT>The number of nurses hired must meet or exceed the demand for each day of the period</CONSTRAINT>
</CONSTRAINTS>
<PARAMETERS>
<PARAMETER>
<DEFINITION>Number of days</DEFINITION>
<SYMBOL>T</SYMBOL>
<SHAPE>constant</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>The planning period for nurse staffing</DEFINITION>
<SYMBOL>Period</SYMBOL>
<SHAPE>constant</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Array of demands for nurses for days</DEFINITION>
<SYMBOL>Demand</SYMBOL>
<SHAPE>['T']</SHAPE>
 </PARAMETER>
</PARAMETERS>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Nurse Staffing}

\subsection*{Objective}
Minimize the number of nurses that the hospital needs to hire for the planning period.

\subsection*{Parameters}
\begin{itemize}
    \item $T$: Number of days in the planning period.
    \item $Period$: The planning period for nurse staffing.
    \item $Demand_t$: The demand for nurses on day $t$, for $t = 1, 2, \ldots, T$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $N$: The number of nurses to hire.
\end{itemize}

\subsection*{Mathematical Formulation}
\begin{align*}
    \text{Minimize} \quad & N \\
    \text{subject to} \quad & N \geq Demand_t \quad \forall t = 1, 2, \ldots, T \\
    & N \geq 0
\end{align*}

\end{document}
```

# START: PythonProgrammerCreator 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Print at the end the objective between <OBJ></OBJ> Do not include 'pip install' in script. Assume every python package is installed like in this example `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Nurse Staffing}

\subsection*{Objective}
Minimize the number of nurses that the hospital needs to hire for the planning period.

\subsection*{Parameters}
\begin{itemize}
    \item $T$: Number of days in the planning period.
    \item $Period$: The planning period for nurse staffing.
    \item $Demand_t$: The demand for nurses on day $t$, for $t = 1, 2, \ldots, T$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $N$: The number of nurses to hire.
\end{itemize}

\subsection*{Mathematical Formulation}
\begin{align*}
    \text{Minimize} \quad & N \\
    \text{subject to} \quad & N \geq Demand_t \quad \forall t = 1, 2, \ldots, T \\
    & N \geq 0
\end{align*}

\end{document}
```
<DATA>
{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
</DATA>

## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
Demand = data['Demand']

#### Create the problem
problem = pulp.LpProblem("Nurse_Staffing_Problem", pulp.LpMinimize)

#### Decision variable
N = pulp.LpVariable("N", lowBound=0, cat='Integer')

#### Objective function
problem += N, "Minimize_the_number_of_nurses"

#### Constraints
for t in range(T):
    problem += N >= Demand[t], f"Demand_Constraint_{t+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

