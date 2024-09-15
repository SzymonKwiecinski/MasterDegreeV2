# START: OR_ModelCreator 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. You receive task description between <TASK_DESCRIPTION> and </TASK_DESCRIPTION>. You receive target objective between <OBJECTIVE> and </OBJECTIVE>. You receive description of constraints between <CONSTRAINTS> and </CONSTRAINTS>. You receive all 'parameters' which you have to use in model with symbol and shape between <PARAMETERS> and </PARAMETERS>. 
## START MESSAGE 0 
### ROLE: Role.USER
<TASK_DESCRIPTION>: A selection problem for hiring translators. Each translator can translate different sets of languages, and has an associated cost. The task is to cover all required languages at the minimum cost.</TASK_DESCRIPTION>.
<OBJECTIVE>: Minimize the total cost of translators while ensuring coverage for all M required languages </OBJECTIVE>
<CONSTRAINTS>
<CONSTRAINT>Each of the M required languages must be translated into</CONSTRAINT>
<CONSTRAINT>Only translators from the set of N translators can be selected</CONSTRAINT>
</CONSTRAINTS>
<PARAMETERS>
<PARAMETER>
<DEFINITION>Number of translators</DEFINITION>
<SYMBOL>N</SYMBOL>
<SHAPE>constant</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Cost of translator i</DEFINITION>
<SYMBOL>Cost</SYMBOL>
<SHAPE>['N']</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Set of languages that translator i can translate</DEFINITION>
<SYMBOL>Languages</SYMBOL>
<SHAPE>['N']</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Number of required languages</DEFINITION>
<SYMBOL>M</SYMBOL>
<SHAPE>constant</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>List of required languages</DEFINITION>
<SYMBOL>RequiredLanguages</SYMBOL>
<SHAPE>['M']</SHAPE>
 </PARAMETER>
</PARAMETERS>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Hiring Translators}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Number of translators
    \item $M$: Number of required languages
    \item $Cost_i$: Cost of hiring translator $i$, for $i = 1, 2, \ldots, N$
    \item $Languages_i$: Set of languages that translator $i$ can translate, for $i = 1, 2, \ldots, N$
    \item $RequiredLanguages$: List of required languages, indexed by $j = 1, 2, \ldots, M$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Binary variable indicating whether translator $i$ is hired (1) or not (0), for $i = 1, 2, \ldots, N$
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost of hiring translators:
\[
\min \sum_{i=1}^{N} Cost_i \cdot x_i
\]

\subsection*{Constraints}
\begin{itemize}
    \item Each required language must be covered by at least one hired translator:
    \[
    \forall j \in \{1, 2, \ldots, M\}, \quad \sum_{i: j \in Languages_i} x_i \geq 1
    \]
    \item Binary constraints for decision variables:
    \[
    \forall i \in \{1, 2, \ldots, N\}, \quad x_i \in \{0, 1\}
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

\section*{Mathematical Model for Hiring Translators}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Number of translators
    \item $M$: Number of required languages
    \item $Cost_i$: Cost of hiring translator $i$, for $i = 1, 2, \ldots, N$
    \item $Languages_i$: Set of languages that translator $i$ can translate, for $i = 1, 2, \ldots, N$
    \item $RequiredLanguages$: List of required languages, indexed by $j = 1, 2, \ldots, M$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Binary variable indicating whether translator $i$ is hired (1) or not (0), for $i = 1, 2, \ldots, N$
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost of hiring translators:
\[
\min \sum_{i=1}^{N} Cost_i \cdot x_i
\]

\subsection*{Constraints}
\begin{itemize}
    \item Each required language must be covered by at least one hired translator:
    \[
    \forall j \in \{1, 2, \ldots, M\}, \quad \sum_{i: j \in Languages_i} x_i \geq 1
    \]
    \item Binary constraints for decision variables:
    \[
    \forall i \in \{1, 2, \ldots, N\}, \quad x_i \in \{0, 1\}
    \]
\end{itemize}

\end{document}
```
<DATA>
{'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}
</DATA>

## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data from JSON format
data = json.loads('{"translators": [{"id": 1, "cost": 12000, "languages": ["FR", "AR", "IT"]}, {"id": 2, "cost": 16000, "languages": ["GE", "RU", "CH"]}, {"id": 3, "cost": 13000, "languages": ["AR", "CH"]}, {"id": 4, "cost": 15000, "languages": ["FR", "SP", "IT", "PO"]}, {"id": 5, "cost": 9000, "languages": ["FR", "GE", "RU", "SP"]}, {"id": 6, "cost": 7000, "languages": ["GE", "SP", "PO"]}], "required_languages": ["FR", "AR", "GE", "RU", "SP", "CH", "IT", "PO"]}')

#### Extract translators and required languages
translators = data['translators']
required_languages = data['required_languages']

#### Create a linear programming problem
problem = pulp.LpProblem("Translator_Hiring_Problem", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", [t['id'] for t in translators], cat='Binary')

#### Objective function
problem += pulp.lpSum([t['cost'] * x[t['id']] for t in translators]), "Total_Cost"

#### Constraints for required languages
for lang in required_languages:
    problem += pulp.lpSum([x[t['id']] for t in translators if lang in t['languages']]) >= 1, f"Cover_{lang}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

