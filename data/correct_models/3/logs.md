# START: OR_ModelCreator 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. You receive task description between <TASK_DESCRIPTION> and </TASK_DESCRIPTION>. You receive target objective between <OBJECTIVE> and </OBJECTIVE>. You receive description of constraints between <CONSTRAINTS> and </CONSTRAINTS>. You receive all 'parameters' which you have to use in model with symbol and shape between <PARAMETERS> and </PARAMETERS>. 
## START MESSAGE 0 
### ROLE: Role.USER
<TASK_DESCRIPTION>: The problem involves determining the optimal quantities of various spare parts to be produced in a month, considering the time required on different machines and the machines' monthly capacities.</TASK_DESCRIPTION>.
<OBJECTIVE>: Maximize the total profit from the production of spare parts </OBJECTIVE>
<CONSTRAINTS>
<CONSTRAINT>Every spare part quantity produced is non-negative</CONSTRAINT>
<CONSTRAINT>Total time used on each machine for all spare parts cannot exceed the machine's monthly capacity</CONSTRAINT>
</CONSTRAINTS>
<PARAMETERS>
<PARAMETER>
<DEFINITION>Number of spare parts to be produced</DEFINITION>
<SYMBOL>NumParts</SYMBOL>
<SHAPE>constant</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Number of machines available</DEFINITION>
<SYMBOL>NumMachines</SYMBOL>
<SHAPE>constant</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>The time taken to make one unit of spare part k on machine s</DEFINITION>
<SYMBOL>Time</SYMBOL>
<SHAPE>['NumParts', 'NumMachines']</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Profit from producing one unit of spare part k</DEFINITION>
<SYMBOL>Profit</SYMBOL>
<SHAPE>['NumParts']</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Capacity of machine s for the month</DEFINITION>
<SYMBOL>Capacity</SYMBOL>
<SHAPE>['NumMachines']</SHAPE>
 </PARAMETER>
</PARAMETERS>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{itemize}
    \item $NumParts$: Number of spare parts to be produced
    \item $NumMachines$: Number of machines available
    \item $Time_{ks}$: Time taken to make one unit of spare part $k$ on machine $s$, for $k = 1, 2, \ldots, NumParts$ and $s = 1, 2, \ldots, NumMachines$
    \item $Profit_k$: Profit from producing one unit of spare part $k$, for $k = 1, 2, \ldots, NumParts$
    \item $Capacity_s$: Capacity of machine $s$ for the month, for $s = 1, 2, \ldots, NumMachines$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_k$: Quantity of spare part $k$ to be produced, for $k = 1, 2, \ldots, NumParts$
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit from the production of spare parts:
\[
\text{Maximize } Z = \sum_{k=1}^{NumParts} Profit_k \cdot x_k
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Non-negativity constraints for the quantity of each spare part:
    \[
    x_k \geq 0 \quad \text{for } k = 1, 2, \ldots, NumParts
    \]
    \item Machine capacity constraints:
    \[
    \sum_{k=1}^{NumParts} Time_{ks} \cdot x_k \leq Capacity_s \quad \text{for } s = 1, 2, \ldots, NumMachines
    \]
\end{enumerate}

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

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{itemize}
    \item $NumParts$: Number of spare parts to be produced
    \item $NumMachines$: Number of machines available
    \item $Time_{ks}$: Time taken to make one unit of spare part $k$ on machine $s$, for $k = 1, 2, \ldots, NumParts$ and $s = 1, 2, \ldots, NumMachines$
    \item $Profit_k$: Profit from producing one unit of spare part $k$, for $k = 1, 2, \ldots, NumParts$
    \item $Capacity_s$: Capacity of machine $s$ for the month, for $s = 1, 2, \ldots, NumMachines$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_k$: Quantity of spare part $k$ to be produced, for $k = 1, 2, \ldots, NumParts$
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit from the production of spare parts:
\[
\text{Maximize } Z = \sum_{k=1}^{NumParts} Profit_k \cdot x_k
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Non-negativity constraints for the quantity of each spare part:
    \[
    x_k \geq 0 \quad \text{for } k = 1, 2, \ldots, NumParts
    \]
    \item Machine capacity constraints:
    \[
    \sum_{k=1}^{NumParts} Time_{ks} \cdot x_k \leq Capacity_s \quad \text{for } s = 1, 2, \ldots, NumMachines
    \]
\end{enumerate}

\end{document}
```
<DATA>
{'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}
</DATA>

## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

#### Parameters
NumParts = data['NumParts']
NumMachines = data['NumMachines']
Time = data['Time']
Profit = data['Profit']
Capacity = data['Capacity']

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(NumParts), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(Profit[k] * x[k] for k in range(NumParts)), "Total_Profit"

#### Constraints
for s in range(NumMachines):
    problem += pulp.lpSum(Time[k][s] * x[k] for k in range(NumParts)) <= Capacity[s], f"Capacity_Constraint_{s+1}"

#### Solve the problem
problem.solve()

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for k in range(NumParts):
    print(f'Quantity of spare part {k+1}: {x[k].varValue}')
```

