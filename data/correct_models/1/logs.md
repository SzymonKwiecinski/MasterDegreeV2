# START: OR_ModelCreator 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. You receive task description between <TASK_DESCRIPTION> and </TASK_DESCRIPTION>. You receive target objective between <OBJECTIVE> and </OBJECTIVE>. You receive description of constraints between <CONSTRAINTS> and </CONSTRAINTS>. You receive all 'parameters' which you have to use in model with symbol and shape between <PARAMETERS> and </PARAMETERS>. 
## START MESSAGE 0 
### ROLE: Role.USER
<TASK_DESCRIPTION>: A firm produces multiple goods using different raw materials. Each good requires certain amounts of the raw materials and generates specific revenue.</TASK_DESCRIPTION>.
<OBJECTIVE>: Maximize the firm's total revenue from goods production </OBJECTIVE>
<CONSTRAINTS>
<CONSTRAINT>All goods quantities are non-negative</CONSTRAINT>
<CONSTRAINT>The quantity of raw material i used cannot exceed Available amount</CONSTRAINT>
</CONSTRAINTS>
<PARAMETERS>
<PARAMETER>
<DEFINITION>Number of different goods produced by the firm</DEFINITION>
<SYMBOL>M</SYMBOL>
<SHAPE>constant</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Number of different raw materials used by the firm</DEFINITION>
<SYMBOL>N</SYMBOL>
<SHAPE>constant</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Available amount of each raw material</DEFINITION>
<SYMBOL>Available</SYMBOL>
<SHAPE>['N']</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Requirement of material j for producing one unit of good i</DEFINITION>
<SYMBOL>Requirements</SYMBOL>
<SHAPE>['M', 'N']</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Revenue earned from selling one unit of good j</DEFINITION>
<SYMBOL>Prices</SYMBOL>
<SHAPE>['M']</SHAPE>
 </PARAMETER>
</PARAMETERS>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Maximizing Firm's Total Revenue}

\subsection*{Parameters}
\begin{itemize}
    \item $M$: Number of different goods produced by the firm.
    \item $N$: Number of different raw materials used by the firm.
    \item $Available_i$: Available amount of raw material $i$ for $i = 1, 2, \ldots, N$.
    \item $Requirements_{ij}$: Requirement of material $j$ for producing one unit of good $i$ for $i = 1, 2, \ldots, M$ and $j = 1, 2, \ldots, N$.
    \item $Prices_i$: Revenue earned from selling one unit of good $i$ for $i = 1, 2, \ldots, M$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Quantity of good $i$ produced for $i = 1, 2, \ldots, M$.
\end{itemize}

\subsection*{Objective Function}
Maximize the total revenue:
\[
\text{Maximize } Z = \sum_{i=1}^{M} Prices_i \cdot x_i
\]

\subsection*{Constraints}
\begin{itemize}
    \item Non-negativity constraints for goods quantities:
    \[
    x_i \geq 0 \quad \text{for } i = 1, 2, \ldots, M
    \]
    \item Raw material availability constraints:
    \[
    \sum_{i=1}^{M} Requirements_{ij} \cdot x_i \leq Available_j \quad \text{for } j = 1, 2, \ldots, N
    \]
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

\section*{Mathematical Model for Maximizing Firm's Total Revenue}

\subsection*{Parameters}
\begin{itemize}
    \item $M$: Number of different goods produced by the firm.
    \item $N$: Number of different raw materials used by the firm.
    \item $Available_i$: Available amount of raw material $i$ for $i = 1, 2, \ldots, N$.
    \item $Requirements_{ij}$: Requirement of material $j$ for producing one unit of good $i$ for $i = 1, 2, \ldots, M$ and $j = 1, 2, \ldots, N$.
    \item $Prices_i$: Revenue earned from selling one unit of good $i$ for $i = 1, 2, \ldots, M$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Quantity of good $i$ produced for $i = 1, 2, \ldots, M$.
\end{itemize}

\subsection*{Objective Function}
Maximize the total revenue:
\[
\text{Maximize } Z = \sum_{i=1}^{M} Prices_i \cdot x_i
\]

\subsection*{Constraints}
\begin{itemize}
    \item Non-negativity constraints for goods quantities:
    \[
    x_i \geq 0 \quad \text{for } i = 1, 2, \ldots, M
    \]
    \item Raw material availability constraints:
    \[
    \sum_{i=1}^{M} Requirements_{ij} \cdot x_i \leq Available_j \quad \text{for } j = 1, 2, \ldots, N
    \]
\end{itemize}

\end{document}
```
<DATA>
{'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 'Prices': [7, 10, 5, 9]}
</DATA>

## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'M': 4,
    'N': 5,
    'Available': [10, 20, 15, 35, 25],
    'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]],
    'Prices': [7, 10, 5, 9]
}

#### Create the LP problem
problem = pulp.LpProblem("Maximize_Total_Revenue", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(data['M']), lowBound=0)

#### Objective Function
problem += pulp.lpSum(data['Prices'][i] * x[i] for i in range(data['M'])), "Total_Revenue"

#### Constraints
for j in range(data['N']):
    problem += pulp.lpSum(data['Requirements'][i][j] * x[i] for i in range(data['M'])) <= data['Available'][j], f"Raw_Material_Constraint_{j}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

