# START: OR_ModelCreator 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. You receive task description between <TASK_DESCRIPTION> and </TASK_DESCRIPTION>. You receive target objective between <OBJECTIVE> and </OBJECTIVE>. You receive description of constraints between <CONSTRAINTS> and </CONSTRAINTS>. You receive all 'parameters' which you have to use in model with symbol and shape between <PARAMETERS> and </PARAMETERS>. 
## START MESSAGE 0 
### ROLE: Role.USER
<TASK_DESCRIPTION>: The problem involves the distribution of electricity from multiple power plants to multiple cities, with the goal of minimizing the transmission costs while respecting the supply and demand constraints of the power plants and cities respectively.</TASK_DESCRIPTION>.
<OBJECTIVE>: Minimize the total transmission cost from power plants to cities </OBJECTIVE>
<CONSTRAINTS>
<CONSTRAINT>Each power plant has a limited supply capacity of Supply</CONSTRAINT>
<CONSTRAINT>Each city has a specific electricity demand of Demand</CONSTRAINT>
<CONSTRAINT>The total electricity supplied to each city must meet its demand</CONSTRAINT>
<CONSTRAINT>A power plant cannot send more electricity than its supply capacity</CONSTRAINT>
<CONSTRAINT>Electricity sent from any power plant to any city is non-negative</CONSTRAINT>
</CONSTRAINTS>
<PARAMETERS>
<PARAMETER>
<DEFINITION>Number of power plants</DEFINITION>
<SYMBOL>P</SYMBOL>
<SHAPE>constant</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Number of cities</DEFINITION>
<SYMBOL>C</SYMBOL>
<SHAPE>constant</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Electricity supply capacity of power plant p</DEFINITION>
<SYMBOL>Supply</SYMBOL>
<SHAPE>['P']</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Electricity demand of city c</DEFINITION>
<SYMBOL>Demand</SYMBOL>
<SHAPE>['C']</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Transmission cost from power plant p to city c</DEFINITION>
<SYMBOL>TransmissionCosts</SYMBOL>
<SHAPE>['P', 'C']</SHAPE>
 </PARAMETER>
</PARAMETERS>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model for Electricity Distribution}

\subsection*{Objective}
Minimize the total transmission cost from power plants to cities.

\begin{equation}
\text{Minimize} \quad Z = \sum_{p=1}^{P} \sum_{c=1}^{C} \text{TransmissionCosts}_{pc} \cdot x_{pc}
\end{equation}

\subsection*{Constraints}

\begin{align}
& \text{1. Each power plant has a limited supply capacity:} \nonumber \\
& \sum_{c=1}^{C} x_{pc} \leq \text{Supply}_p \quad \forall p = 1, \ldots, P \\
& \text{2. Each city has a specific electricity demand:} \nonumber \\
& \sum_{p=1}^{P} x_{pc} = \text{Demand}_c \quad \forall c = 1, \ldots, C \\
& \text{3. Electricity sent from any power plant to any city is non-negative:} \nonumber \\
& x_{pc} \geq 0 \quad \forall p = 1, \ldots, P, \; \forall c = 1, \ldots, C
\end{align}

\subsection*{Parameters}

\begin{itemize}
    \item $P$: Number of power plants (constant)
    \item $C$: Number of cities (constant)
    \item $\text{Supply}_p$: Electricity supply capacity of power plant $p$, for $p = 1, \ldots, P$
    \item $\text{Demand}_c$: Electricity demand of city $c$, for $c = 1, \ldots, C$
    \item $\text{TransmissionCosts}_{pc}$: Transmission cost from power plant $p$ to city $c$
\end{itemize}

\subsection*{Decision Variables}

\begin{itemize}
    \item $x_{pc}$: Amount of electricity transmitted from power plant $p$ to city $c$
\end{itemize}

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

\section*{Mathematical Model for Electricity Distribution}

\subsection*{Objective}
Minimize the total transmission cost from power plants to cities.

\begin{equation}
\text{Minimize} \quad Z = \sum_{p=1}^{P} \sum_{c=1}^{C} \text{TransmissionCosts}_{pc} \cdot x_{pc}
\end{equation}

\subsection*{Constraints}

\begin{align}
& \text{1. Each power plant has a limited supply capacity:} \nonumber \\
& \sum_{c=1}^{C} x_{pc} \leq \text{Supply}_p \quad \forall p = 1, \ldots, P \\
& \text{2. Each city has a specific electricity demand:} \nonumber \\
& \sum_{p=1}^{P} x_{pc} = \text{Demand}_c \quad \forall c = 1, \ldots, C \\
& \text{3. Electricity sent from any power plant to any city is non-negative:} \nonumber \\
& x_{pc} \geq 0 \quad \forall p = 1, \ldots, P, \; \forall c = 1, \ldots, C
\end{align}

\subsection*{Parameters}

\begin{itemize}
    \item $P$: Number of power plants (constant)
    \item $C$: Number of cities (constant)
    \item $\text{Supply}_p$: Electricity supply capacity of power plant $p$, for $p = 1, \ldots, P$
    \item $\text{Demand}_c$: Electricity demand of city $c$, for $c = 1, \ldots, C$
    \item $\text{TransmissionCosts}_{pc}$: Transmission cost from power plant $p$ to city $c$
\end{itemize}

\subsection*{Decision Variables}

\begin{itemize}
    \item $x_{pc}$: Amount of electricity transmitted from power plant $p$ to city $c$
\end{itemize}

\end{document}
```
<DATA>
{'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}
</DATA>

## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

#### Parameters
P = len(data['supply'])  #### Number of power plants
C = len(data['demand'])   #### Number of cities

#### Create a linear programming problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", (range(P), range(C)), lowBound=0)

#### Objective Function
problem += pulp.lpSum(data['transmission_costs'][p][c] * x[p][c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

#### Constraints
#### Supply constraints
for p in range(P):
    problem += pulp.lpSum(x[p][c] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_{p}"

#### Demand constraints
for c in range(C):
    problem += pulp.lpSum(x[p][c] for p in range(P)) == data['demand'][c], f"Demand_Constraint_{c}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

