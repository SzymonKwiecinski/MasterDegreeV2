# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MIP
PROBLEM INFO:

- The knapsack problem has a significant place in the study of integer programming models with binary variables. 
- In the knapsack problem, one needs to pack a set of items in a container.
- Each item \var{k} has value \var{value_{k}} and size \var{size_{k}}.
- And the container has maximum capacity \var{C}. 
- If the total size of the items exceeds the capacity, we can't pack them all. 
- In that case, the problem is to choose a subset of the items of maximum total value that will fit in the container. 

INPUT FORMAT:

{
	"C": C,
	"value": [value_{k} for k in 1,...,K],
	"size": [size_{k} for k in 1,...,K]
}


OBJECTIVE: Maximize the total value of the packed items

OUTPUT INFO:

- \var{isincluded} represents whether each item is included in the container

OUTPUT FORMAT:

{
	"isincluded": [isincluded_{k} for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Knapsack Problem Formulation}

\textbf{Parameters:}
\begin{itemize}
    \item \( C \): Maximum capacity of the container.
    \item \( K \): Total number of items.
    \item \( \text{value}_{k} \): Value of item \( k \) for \( k = 1, \ldots, K \).
    \item \( \text{size}_{k} \): Size of item \( k \) for \( k = 1, \ldots, K \).
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( x_{k} \in \{0, 1\} \): Binary variable that indicates whether item \( k \) is included in the container (1 if included, 0 otherwise).
\end{itemize}

\textbf{Objective:}
\begin{equation}
    \text{Maximize } Z = \sum_{k=1}^{K} \text{value}_{k} \cdot x_{k}
\end{equation}

\textbf{Constraints:}
\begin{equation}
    \sum_{k=1}^{K} \text{size}_{k} \cdot x_{k} \leq C
\end{equation}
\begin{equation}
    x_{k} \in \{0, 1\} \quad \forall k = 1, \ldots, K
\end{equation}

\textbf{Output:}
\begin{itemize}
    \item \( \text{isincluded} = [x_{1}, x_{2}, \ldots, x_{K}] \): A list indicating whether each item is included in the container.
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

\section*{Knapsack Problem Formulation}

\textbf{Parameters:}
\begin{itemize}
    \item \( C \): Maximum capacity of the container.
    \item \( K \): Total number of items.
    \item \( \text{value}_{k} \): Value of item \( k \) for \( k = 1, \ldots, K \).
    \item \( \text{size}_{k} \): Size of item \( k \) for \( k = 1, \ldots, K \).
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( x_{k} \in \{0, 1\} \): Binary variable that indicates whether item \( k \) is included in the container (1 if included, 0 otherwise).
\end{itemize}

\textbf{Objective:}
\begin{equation}
    \text{Maximize } Z = \sum_{k=1}^{K} \text{value}_{k} \cdot x_{k}
\end{equation}

\textbf{Constraints:}
\begin{equation}
    \sum_{k=1}^{K} \text{size}_{k} \cdot x_{k} \leq C
\end{equation}
\begin{equation}
    x_{k} \in \{0, 1\} \quad \forall k = 1, \ldots, K
\end{equation}

\textbf{Output:}
\begin{itemize}
    \item \( \text{isincluded} = [x_{1}, x_{2}, \ldots, x_{K}] \): A list indicating whether each item is included in the container.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'C': 10, 'value': [10, 20], 'size': [8, 6]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data input
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

#### Capacity constraint
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "Capacity_Constraint"

#### Solve the problem
problem.solve()

#### Output the results
isincluded = [int(x[k].value()) for k in range(K)]
print(f' (Included items): {isincluded}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

