# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- We assume that there are available at the market different foods and that the food \var{k} sells at a price \var{price_{k}} per unit. 
- In addition there are several basic nutritional ingredients and, to achieve a balanced diet, each individual must receive at least \var{demand_{m}} units of nutrient \var{m} per day. 
- Finally, we assume that each unit of food \var{k} contains \var{nutri_{k, m}} units of nutrition \var{m}

INPUT FORMAT:

{
	"price": [price_{k} for k in 1,...,K],
	"demand": [demand_{m} for m in 1,...,M],
	"nutrition": [[nutri_{k, m} for m in 1,...,M] for k in 1,...,K]
}


OBJECTIVE: We want to minimize the total prices of the foods to purchase.

OUTPUT INFO:

- \var{quantity} represents the quantity of each food to purchase

OUTPUT FORMAT:

{
	"quantity": [quantity_{k} for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Nutritional Optimization}

\subsection*{Variables}
Let \( x_k \) be the quantity of food \( k \) to purchase, where \( k = 1, 2, \ldots, K \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{price}_k \): price per unit of food \( k \)
    \item \( \text{demand}_m \): minimum required units of nutrient \( m \)
    \item \( \text{nutri}_{k,m} \): units of nutrient \( m \) in food \( k \)
\end{itemize}

\subsection*{Objective Function}
We want to minimize the total cost of the foods purchased:
\[
\text{Minimize } Z = \sum_{k=1}^K \text{price}_k \cdot x_k
\]

\subsection*{Constraints}
To satisfy the nutritional requirements, we have the following constraints for each nutrient \( m \):
\[
\sum_{k=1}^K \text{nutri}_{k,m} \cdot x_k \geq \text{demand}_m \quad \text{for each } m = 1, 2, \ldots, M
\]

Additionally, we assume that the quantities purchased cannot be negative:
\[
x_k \geq 0 \quad \text{for each } k = 1, 2, \ldots, K
\]

\subsection*{Summary}
The complete linear programming model can be summarized as follows:

\[
\begin{align*}
\text{Minimize } & Z = \sum_{k=1}^K \text{price}_k \cdot x_k \\
\text{subject to } & \sum_{k=1}^K \text{nutri}_{k,m} \cdot x_k \geq \text{demand}_m, \quad m = 1, 2, \ldots, M \\
& x_k \geq 0, \quad k = 1, 2, \ldots, K
\end{align*}
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

\section*{Linear Programming Model for Nutritional Optimization}

\subsection*{Variables}
Let \( x_k \) be the quantity of food \( k \) to purchase, where \( k = 1, 2, \ldots, K \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{price}_k \): price per unit of food \( k \)
    \item \( \text{demand}_m \): minimum required units of nutrient \( m \)
    \item \( \text{nutri}_{k,m} \): units of nutrient \( m \) in food \( k \)
\end{itemize}

\subsection*{Objective Function}
We want to minimize the total cost of the foods purchased:
\[
\text{Minimize } Z = \sum_{k=1}^K \text{price}_k \cdot x_k
\]

\subsection*{Constraints}
To satisfy the nutritional requirements, we have the following constraints for each nutrient \( m \):
\[
\sum_{k=1}^K \text{nutri}_{k,m} \cdot x_k \geq \text{demand}_m \quad \text{for each } m = 1, 2, \ldots, M
\]

Additionally, we assume that the quantities purchased cannot be negative:
\[
x_k \geq 0 \quad \text{for each } k = 1, 2, \ldots, K
\]

\subsection*{Summary}
The complete linear programming model can be summarized as follows:

\[
\begin{align*}
\text{Minimize } & Z = \sum_{k=1}^K \text{price}_k \cdot x_k \\
\text{subject to } & \sum_{k=1}^K \text{nutri}_{k,m} \cdot x_k \geq \text{demand}_m, \quad m = 1, 2, \ldots, M \\
& x_k \geq 0, \quad k = 1, 2, \ldots, K
\end{align*}
\]

\end{document}</MATH_MODEL>
<DATA>
{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

#### Variables
K = len(data['price'])  #### Number of food items
M = len(data['demand'])  #### Number of nutrients

#### Create a linear programming problem
problem = pulp.LpProblem("Nutritional_Optimization", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("food", range(K), lowBound=0)

#### Objective Function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K)), "Total_Cost"

#### Constraints for nutritional requirements
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * x[k] for k in range(K)) >= data['demand'][m], f"Nutrient_Requirement_{m}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

