# START: OR_ModelCreator 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. You receive task description between <TASK_DESCRIPTION> and </TASK_DESCRIPTION>. You receive target objective between <OBJECTIVE> and </OBJECTIVE>. You receive description of constraints between <CONSTRAINTS> and </CONSTRAINTS>. You receive all 'parameters' which you have to use in model with symbol and shape between <PARAMETERS> and </PARAMETERS>. 
## START MESSAGE 0 
### ROLE: Role.USER
<TASK_DESCRIPTION>: The manufacturer is looking to determine the optimal combination of various alloys to produce a specified total quantity with certain target components at minimal cost.</TASK_DESCRIPTION>.
<OBJECTIVE>: Minimize the sum of the costs of the alloys used in the production </OBJECTIVE>
<CONSTRAINTS>
<CONSTRAINT>The total quantity of alloys produced is exactly AlloyQuantity</CONSTRAINT>
<CONSTRAINT>The quantity of each target component in the alloy must be met or exceeded</CONSTRAINT>
<CONSTRAINT>The quantity of component k in alloy m must adhere to the specified Ratio</CONSTRAINT>
<CONSTRAINT>Each alloy's quantity is non-negative</CONSTRAINT>
</CONSTRAINTS>
<PARAMETERS>
<PARAMETER>
<DEFINITION>Quantity of alloy to produce</DEFINITION>
<SYMBOL>AlloyQuantity</SYMBOL>
<SHAPE>constant</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Quantity of target components in the alloy</DEFINITION>
<SYMBOL>Target</SYMBOL>
<SHAPE>['M']</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Ratio of each component k in the alloy m</DEFINITION>
<SYMBOL>Ratio</SYMBOL>
<SHAPE>['K', 'M']</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Price of each alloy k</DEFINITION>
<SYMBOL>Price</SYMBOL>
<SHAPE>['K']</SHAPE>
 </PARAMETER>
</PARAMETERS>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Alloy Production}

\subsection*{Objective}
Minimize the total cost of the alloys used in the production:
\[
\text{Minimize} \quad \sum_{k=1}^{K} \text{Price}_k \cdot x_k
\]

\subsection*{Constraints}
1. The total quantity of alloys produced is exactly \(\text{AlloyQuantity}\):
\[
\sum_{k=1}^{K} x_k = \text{AlloyQuantity}
\]

2. The quantity of each target component in the alloy must be met or exceeded:
\[
\sum_{k=1}^{K} \text{Ratio}_{k,m} \cdot x_k \geq \text{Target}_m \quad \forall m \in \{1, 2, \ldots, M\}
\]

3. The quantity of component \(k\) in alloy \(m\) must adhere to the specified \(\text{Ratio}\):
\[
\text{Ratio}_{k,m} \cdot x_k \quad \text{(implicitly included in the above constraint)}
\]

4. Each alloy's quantity is non-negative:
\[
x_k \geq 0 \quad \forall k \in \{1, 2, \ldots, K\}
\]

\subsection*{Parameters}
\begin{itemize}
    \item \(\text{AlloyQuantity}\): Total quantity of alloy to produce (constant)
    \item \(\text{Target}_m\): Quantity of target components in the alloy for each \(m \in \{1, 2, \ldots, M\}\)
    \item \(\text{Ratio}_{k,m}\): Ratio of each component \(k\) in the alloy \(m\) for each \(k \in \{1, 2, \ldots, K\}\) and \(m \in \{1, 2, \ldots, M\}\)
    \item \(\text{Price}_k\): Price of each alloy \(k\) for each \(k \in \{1, 2, \ldots, K\}\)
\end{itemize}

\subsection*{Decision Variables}
\[
x_k \quad \text{(quantity of alloy } k \text{ to produce)}
\]

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

\section*{Mathematical Model for Alloy Production}

\subsection*{Objective}
Minimize the total cost of the alloys used in the production:
\[
\text{Minimize} \quad \sum_{k=1}^{K} \text{Price}_k \cdot x_k
\]

\subsection*{Constraints}
1. The total quantity of alloys produced is exactly \(\text{AlloyQuantity}\):
\[
\sum_{k=1}^{K} x_k = \text{AlloyQuantity}
\]

2. The quantity of each target component in the alloy must be met or exceeded:
\[
\sum_{k=1}^{K} \text{Ratio}_{k,m} \cdot x_k \geq \text{Target}_m \quad \forall m \in \{1, 2, \ldots, M\}
\]

3. The quantity of component \(k\) in alloy \(m\) must adhere to the specified \(\text{Ratio}\):
\[
\text{Ratio}_{k,m} \cdot x_k \quad \text{(implicitly included in the above constraint)}
\]

4. Each alloy's quantity is non-negative:
\[
x_k \geq 0 \quad \forall k \in \{1, 2, \ldots, K\}
\]

\subsection*{Parameters}
\begin{itemize}
    \item \(\text{AlloyQuantity}\): Total quantity of alloy to produce (constant)
    \item \(\text{Target}_m\): Quantity of target components in the alloy for each \(m \in \{1, 2, \ldots, M\}\)
    \item \(\text{Ratio}_{k,m}\): Ratio of each component \(k\) in the alloy \(m\) for each \(k \in \{1, 2, \ldots, K\}\) and \(m \in \{1, 2, \ldots, M\}\)
    \item \(\text{Price}_k\): Price of each alloy \(k\) for each \(k \in \{1, 2, \ldots, K\}\)
\end{itemize}

\subsection*{Decision Variables}
\[
x_k \quad \text{(quantity of alloy } k \text{ to produce)}
\]

\end{document}
```
<DATA>
{'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}
</DATA>

## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

#### Parameters
alloy_quantity = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

K = len(price)  #### Number of alloys
M = len(target)  #### Number of target components

#### Create the linear programming problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  #### Quantity of each alloy

#### Objective function
problem += pulp.lpSum(price[k] * x[k] for k in range(K)), "Total_Cost"

#### Constraints
#### Total alloy quantity constraint
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quantity, "Total_Quantity"

#### Target component constraints
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * x[k] for k in range(K)) >= target[m], f"Target_Component_{m+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

