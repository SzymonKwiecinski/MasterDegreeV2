# START: OR_ModelCreator 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. You receive task description between <TASK_DESCRIPTION> and </TASK_DESCRIPTION>. You receive target objective between <OBJECTIVE> and </OBJECTIVE>. You receive description of constraints between <CONSTRAINTS> and </CONSTRAINTS>. You receive all 'parameters' which you have to use in model with symbol and shape between <PARAMETERS> and </PARAMETERS>. 
## START MESSAGE 0 
### ROLE: Role.USER
<TASK_DESCRIPTION>: Determine the selection of items to include in a knapsack that has a fixed capacity, where each item has an associated value and size.</TASK_DESCRIPTION>.
<OBJECTIVE>: Maximize the total value of the items packed in the knapsack </OBJECTIVE>
<CONSTRAINTS>
<CONSTRAINT>The total size of the items in the knapsack must not exceed the capacity C</CONSTRAINT>
<CONSTRAINT>Each item can either be included or not in the knapsack - cannot be fractioned</CONSTRAINT>
<CONSTRAINT>The knapsack capacity C is non-negative</CONSTRAINT>
<CONSTRAINT>Each item k has a non-negative size</CONSTRAINT>
<CONSTRAINT>Each item k has a non-negative value</CONSTRAINT>
</CONSTRAINTS>
<PARAMETERS>
<PARAMETER>
<DEFINITION>Total Capacity of the Knapsack</DEFINITION>
<SYMBOL>C</SYMBOL>
<SHAPE>constant</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Value of item k</DEFINITION>
<SYMBOL>Value</SYMBOL>
<SHAPE>['K']</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Size of item k</DEFINITION>
<SYMBOL>Size</SYMBOL>
<SHAPE>['K']</SHAPE>
 </PARAMETER>
</PARAMETERS>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Knapsack Problem Formulation}

\subsection*{Objective}
Maximize the total value of the items packed in the knapsack.

\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{Value}_k \cdot x_k
\]

\subsection*{Constraints}
\begin{align}
& \sum_{k=1}^{K} \text{Size}_k \cdot x_k \leq C \quad & \text{(Total size constraint)} \\
& x_k \in \{0, 1\} \quad \forall k \in \{1, 2, \ldots, K\} \quad & \text{(Binary decision for each item)} \\
& C \geq 0 \quad & \text{(Non-negative knapsack capacity)} \\
& \text{Size}_k \geq 0 \quad \forall k \in \{1, 2, \ldots, K\} \quad & \text{(Non-negative size for each item)} \\
& \text{Value}_k \geq 0 \quad \forall k \in \{1, 2, \ldots, K\} \quad & \text{(Non-negative value for each item)}
\end{align}

\subsection*{Parameters}
\begin{itemize}
    \item $C$: Total Capacity of the Knapsack (constant)
    \item $\text{Value}_k$: Value of item $k$ (array of size $K$)
    \item $\text{Size}_k$: Size of item $k$ (array of size $K$)
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

\section*{Knapsack Problem Formulation}

\subsection*{Objective}
Maximize the total value of the items packed in the knapsack.

\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{Value}_k \cdot x_k
\]

\subsection*{Constraints}
\begin{align}
& \sum_{k=1}^{K} \text{Size}_k \cdot x_k \leq C \quad & \text{(Total size constraint)} \\
& x_k \in \{0, 1\} \quad \forall k \in \{1, 2, \ldots, K\} \quad & \text{(Binary decision for each item)} \\
& C \geq 0 \quad & \text{(Non-negative knapsack capacity)} \\
& \text{Size}_k \geq 0 \quad \forall k \in \{1, 2, \ldots, K\} \quad & \text{(Non-negative size for each item)} \\
& \text{Value}_k \geq 0 \quad \forall k \in \{1, 2, \ldots, K\} \quad & \text{(Non-negative value for each item)}
\end{align}

\subsection*{Parameters}
\begin{itemize}
    \item $C$: Total Capacity of the Knapsack (constant)
    \item $\text{Value}_k$: Value of item $k$ (array of size $K$)
    \item $\text{Size}_k$: Size of item $k$ (array of size $K$)
\end{itemize}

\end{document}
```
<DATA>
{'C': 10, 'value': [10, 20], 'size': [8, 6]}
</DATA>

## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

#### Create a linear programming problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), cat='Binary')

#### Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "TotalValue"

#### Constraints
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "TotalSizeConstraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

