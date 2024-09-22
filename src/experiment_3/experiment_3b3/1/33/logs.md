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

\title{Mathematical Model for the Knapsack Problem}
\author{}
\date{}
\maketitle

\section{Introduction}
In the knapsack problem, we aim to select a subset of items that maximizes the total value while staying within a specified capacity. Each item \( k \) has an associated value \( \text{value}_{k} \) and size \( \text{size}_{k} \). The capacity of the knapsack is denoted as \( C \).

\section{Mathematical Model}

\subsection{Indices}
\begin{itemize}
    \item \( k \): Index for items, where \( k = 1, \ldots, K \)
\end{itemize}

\subsection{Parameters}
\begin{itemize}
    \item \( C \): Maximum capacity of the knapsack
    \item \( \text{value}_{k} \): Value of item \( k \)
    \item \( \text{size}_{k} \): Size of item \( k \)
\end{itemize}

\subsection{Variables}
\begin{itemize}
    \item \( \text{isincluded}_{k} \): Binary variable which is 1 if item \( k \) is included in the knapsack, and 0 otherwise
\end{itemize}

\subsection{Objective Function}
We want to maximize the total value of the packed items:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{value}_{k} \cdot \text{isincluded}_{k}
\]

\subsection{Constraints}
The total size of the selected items must not exceed the capacity of the knapsack:
\[
\sum_{k=1}^{K} \text{size}_{k} \cdot \text{isincluded}_{k} \leq C
\]
Additionally, the decision variable must be binary:
\[
\text{isincluded}_{k} \in \{0, 1\}, \quad \forall k \in \{1, \ldots, K\}
\]

\section{Output Format}
The output will indicate which items are included in the knapsack:
\[
\text{output} = \{ \text{isincluded} = [\text{isincluded}_{k} \text{ for } k \text{ in } 1,\ldots,K] \}
\]

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

\title{Mathematical Model for the Knapsack Problem}
\author{}
\date{}
\maketitle

\section{Introduction}
In the knapsack problem, we aim to select a subset of items that maximizes the total value while staying within a specified capacity. Each item \( k \) has an associated value \( \text{value}_{k} \) and size \( \text{size}_{k} \). The capacity of the knapsack is denoted as \( C \).

\section{Mathematical Model}

\subsection{Indices}
\begin{itemize}
    \item \( k \): Index for items, where \( k = 1, \ldots, K \)
\end{itemize}

\subsection{Parameters}
\begin{itemize}
    \item \( C \): Maximum capacity of the knapsack
    \item \( \text{value}_{k} \): Value of item \( k \)
    \item \( \text{size}_{k} \): Size of item \( k \)
\end{itemize}

\subsection{Variables}
\begin{itemize}
    \item \( \text{isincluded}_{k} \): Binary variable which is 1 if item \( k \) is included in the knapsack, and 0 otherwise
\end{itemize}

\subsection{Objective Function}
We want to maximize the total value of the packed items:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{value}_{k} \cdot \text{isincluded}_{k}
\]

\subsection{Constraints}
The total size of the selected items must not exceed the capacity of the knapsack:
\[
\sum_{k=1}^{K} \text{size}_{k} \cdot \text{isincluded}_{k} \leq C
\]
Additionally, the decision variable must be binary:
\[
\text{isincluded}_{k} \in \{0, 1\}, \quad \forall k \in \{1, \ldots, K\}
\]

\section{Output Format}
The output will indicate which items are included in the knapsack:
\[
\text{output} = \{ \text{isincluded} = [\text{isincluded}_{k} \text{ for } k \text{ in } 1,\ldots,K] \}
\]

\end{document}</MATH_MODEL>
<DATA>
{'C': 10, 'value': [10, 20], 'size': [8, 6]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

#### Extract data
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

#### Create the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

#### Decision variables
isincluded = [pulp.LpVariable(f"isincluded_{k}", cat='Binary') for k in range(K)]

#### Objective function
problem += pulp.lpSum(values[k] * isincluded[k] for k in range(K)), "Total_Value"

#### Constraints
problem += pulp.lpSum(sizes[k] * isincluded[k] for k in range(K)) <= C, "Capacity_Constraint"

#### Solve the problem
problem.solve()

#### Output which items are included
output = {'isincluded': [pulp.value(isincluded[k]) for k in range(K)]}
print(f'Output: {output}')

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

