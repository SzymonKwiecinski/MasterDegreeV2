# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>\documentclass{article}
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

\end{document}</MATH_MODEL>
<DATA>{'C': 10, 'value': [10, 20], 'size': [8, 6]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']

#### Number of items
K = len(values)

#### Create the problem variable
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), cat='Binary')

#### Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "Total_Value"

#### Constraints
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "Total_Size_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

