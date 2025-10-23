---
id: introreact
title: 02 - Criando um App React com Vite
---

# **Criando um App React com Vite**


### **Por que usar [Vite](https://vite.dev/)?**

Vite é uma ferramenta de construção de front-end que oferece um desenvolvimento rápido e uma experiência de usuário aprimorada, especialmente para projetos React. Ela é mais leve e rápida que ferramentas como Webpack, proporcionando hot module replacement (HMR) quase instantâneo.

### **Criando o Projeto**

**1. Instale o Node.js e npm (ou yarn):**

* Certifique-se de ter o Node.js instalado em sua máquina. Você pode baixá-lo em [https://nodejs.org/](https://nodejs.org/). Dê Preferência a versão LTS. No seu desktop ou notebook use a versão com o instalador.

* No laboratório se não estiver instalado faça o download do [node.js LTS binary](https://nodejs.org/dist/v22.20.0/node-v22.20.0-win-x64.zip) for Windows e extraia o zip para o **local desejado(Ex: c:\node)** e adicione **PATH** da pasta do node na variável de ambiente PATH.

> Tecla Windows + R => digite:

```bash
rundll32 sysdm.cpl,EditEnvironmentVariables
```

**2. Crie um novo projeto:**

```bash
npm create vite@latest my-react-app --template react
```

Substitua `my-react-app` pelo nome desejado para seu projeto.

### **Estrutura de Pastas do Projeto Vite + React**

Após criar o projeto, você terá a seguinte estrutura:

```
my-react-app/
├── public/
│   ├── vite.svg          # Ícone do Vite
│   └── index.html        # Template HTML principal
├── src/
│   ├── assets/           # Imagens, ícones e outros recursos
│   ├── App.jsx           # Componente principal da aplicação
│   ├── App.css           # Estilos do componente App
│   ├── index.css         # Estilos globais
│   └── main.jsx          # Ponto de entrada da aplicação
├── package.json          # Dependências e scripts do projeto
├── vite.config.js        # Configurações do Vite
└── README.md             # Documentação do projeto
```

**Arquivos importantes:**
- **src/main.jsx**: Ponto de entrada onde o React é inicializado
- **src/App.jsx**: Componente principal da sua aplicação
- **public/index.html**: Template base do HTML
- **vite.config.js**: Configurações específicas do Vite

**3. Instale as dependências:**

```bash
cd my-react-app
npm install
```

**4. Inicie o servidor de desenvolvimento:**

```bash
npm run dev
```

Seu aplicativo estará disponível em `http://localhost:5173/` (porta padrão do Vite).

### **Troubleshooting Comum**

**Problemas frequentes e soluções:**

1. **Erro de porta ocupada:**
   ```bash
   # Se a porta 5173 estiver ocupada, o Vite automaticamente usará a próxima disponível
   # Ou você pode especificar uma porta:
   npm run dev -- --port 3000
   ```

2. **Erro de permissão no Windows:**
   ```bash
   # Execute o PowerShell como administrador ou use:
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Erro "command not found":**
    - Verifique se o Node.js está instalado: `node --version`
    - Verifique se o npm está funcionando: `npm --version`
    - Reinstale as dependências: `npm install`

4. **Página em branco:**
    - Verifique o console do navegador (F12)
    - Certifique-se de que não há erros de sintaxe no código

### Construindo o App: Um Contador Simples

**1. Abra o arquivo `src/App.jsx`:**

```jsx
import React, { useState } from 'react';

function App() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Você clicou {count} vezes</p>
      <button onClick={() => setCount(count + 1)}>
        Clique para incrementar
      </button>
    </div>
  );
}

export default App;
```

**Explicação:**

* **useState:** Hook do React que permite gerenciar o estado local de um componente.
* **count:** Variável de estado que armazena o número de cliques.
* **setCount:** Função para atualizar o valor de count.
* **onClick:** Manipulador de eventos que incrementa o valor de count quando o botão é clicado.

#### Demonstração de Outros Conceitos

Outro pontos fundamentais do React:

* **Componentes:** Criar componentes funcionais e de classe para modularizar seu código.
* **Props:** Passar dados entre componentes usando props.
* **JSX:** Utilizar JSX para criar a estrutura HTML de seus componentes.
* **Ciclo de vida:** Entender os métodos do ciclo de vida de um componente (componentDidMount, componentDidUpdate, etc.).
* **Condicionalmente renderizar elementos:** Usar operadores lógicos para mostrar ou ocultar elementos.
* **Listas:** Renderizar listas de elementos usando o método `map`.
* **Eventos:** Manipular diversos tipos de eventos (e.g., `onMouseOver`, `onSubmit`).

#### Próximos Passos

* **Redux:** Gerencie o estado global de sua aplicação.
* **React Router:** Crie rotas para navegar entre diferentes páginas.
* **Hooks:** Utilize hooks personalizados para criar lógica reutilizável.
* **Styled Components:** Estilize seus componentes de forma mais declarativa.

### **Exemplo mais completo: Uma lista de tarefas**

```jsx
import React, { useState } from 'react';

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState('');

  const handleAddTask = () => {
    if (newTask.trim() !== '') {
      setTasks([...tasks, newTask]);
      setNewTask('');
    }
  };

  return (
    <div>
      <input 
        type="text" 
        value={newTask} 
        onChange={(e) => setNewTask(e.target.value)} 
        placeholder="Digite uma nova tarefa"
      />
      <button onClick={handleAddTask}>Adicionar</button>
      <ul>
        {tasks.map((task, index) => (
          <li key={index}>{task}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
```

**Este exemplo demonstra:**

* **Múltiplos estados:** `tasks` para armazenar a lista de tarefas e `newTask` para o valor do input.
* **Manipulação de eventos:** `onChange` para atualizar o valor do input e `onClick` para adicionar uma nova tarefa.
* **Renderização de listas:** Usando o método `map` para renderizar cada tarefa como um item de lista.
