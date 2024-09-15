# START: OR_ModelCreator 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. You receive task description between <TASK_DESCRIPTION> and </TASK_DESCRIPTION>. You receive target objective between <OBJECTIVE> and </OBJECTIVE>. You receive description of constraints between <CONSTRAINTS> and </CONSTRAINTS>. You receive all 'parameters' which you have to use in model with symbol and shape between <PARAMETERS> and </PARAMETERS>. 
## START MESSAGE 0 
### ROLE: Role.USER
<TASK_DESCRIPTION>: The production involves multiple products and machines, with each product requiring specific production time on each machine and yielding a certain profit.</TASK_DESCRIPTION>.
<OBJECTIVE>: Maximize the total profit from producing different products subject to production time constraints on each machine </OBJECTIVE>
<CONSTRAINTS>
<CONSTRAINT>Each product k must be produced in non-negative quantities</CONSTRAINT>
<CONSTRAINT>For each machine m, the total production time for all products cannot exceed AvailableTime</CONSTRAINT>
</CONSTRAINTS>
<PARAMETERS>
<PARAMETER>
<DEFINITION>Number of different products</DEFINITION>
<SYMBOL>NumProducts</SYMBOL>
<SHAPE>constant</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Number of different machines</DEFINITION>
<SYMBOL>NumMachines</SYMBOL>
<SHAPE>constant</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Time to produce one unit of product k on machine m</DEFINITION>
<SYMBOL>ProduceTime</SYMBOL>
<SHAPE>['NumProducts', 'NumMachines']</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Total available time on machine m</DEFINITION>
<SYMBOL>AvailableTime</SYMBOL>
<SHAPE>['NumMachines']</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Profit from producing one unit of product k</DEFINITION>
<SYMBOL>Profit</SYMBOL>
<SHAPE>['NumProducts']</SHAPE>
 </PARAMETER>
</PARAMETERS>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Production Optimization}

\subsection*{Parameters}
\begin{itemize}
    \item $NumProducts$: Number of different products
    \item $NumMachines$: Number of different machines
    \item $ProduceTime_{k,m}$: Time to produce one unit of product $k$ on machine $m$, for $k = 1, \ldots, NumProducts$ and $m = 1, \ldots, NumMachines$
    \item $AvailableTime_m$: Total available time on machine $m$, for $m = 1, \ldots, NumMachines$
    \item $Profit_k$: Profit from producing one unit of product $k$, for $k = 1, \ldots, NumProducts$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_k$: Quantity of product $k$ to be produced, for $k = 1, \ldots, NumProducts$
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{NumProducts} Profit_k \cdot x_k
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Non-negativity constraints for each product:
    \[
    x_k \geq 0 \quad \text{for } k = 1, \ldots, NumProducts
    \]
    \item Production time constraints for each machine:
    \[
    \sum_{k=1}^{NumProducts} ProduceTime_{k,m} \cdot x_k \leq AvailableTime_m \quad \text{for } m = 1, \ldots, NumMachines
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

\section*{Mathematical Model for Production Optimization}

\subsection*{Parameters}
\begin{itemize}
    \item $NumProducts$: Number of different products
    \item $NumMachines$: Number of different machines
    \item $ProduceTime_{k,m}$: Time to produce one unit of product $k$ on machine $m$, for $k = 1, \ldots, NumProducts$ and $m = 1, \ldots, NumMachines$
    \item $AvailableTime_m$: Total available time on machine $m$, for $m = 1, \ldots, NumMachines$
    \item $Profit_k$: Profit from producing one unit of product $k$, for $k = 1, \ldots, NumProducts$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_k$: Quantity of product $k$ to be produced, for $k = 1, \ldots, NumProducts$
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{NumProducts} Profit_k \cdot x_k
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Non-negativity constraints for each product:
    \[
    x_k \geq 0 \quad \text{for } k = 1, \ldots, NumProducts
    \]
    \item Production time constraints for each machine:
    \[
    \sum_{k=1}^{NumProducts} ProduceTime_{k,m} \cdot x_k \leq AvailableTime_m \quad \text{for } m = 1, \ldots, NumMachines
    \]
\end{enumerate}

\end{document}
```
<DATA>
{'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}
</DATA>

## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

#### Creating the LP problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(data['NumProducts']), lowBound=0)

#### Objective Function
problem += pulp.lpSum(data['Profit'][k] * x[k] for k in range(data['NumProducts'])), "Total_Profit"

#### Constraints
for m in range(data['NumMachines']):
    problem += (pulp.lpSum(data['ProduceTime'][k][m] * x[k] for k in range(data['NumProducts'])) <= data['AvailableTime'][m]), f"Machine_{m+1}_Time_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

