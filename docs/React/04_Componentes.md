---
id: 04_Componentes
title: 04 - Componentes Básicos
---
# 04 - **Componentes Básicos**

## Introdução aos Componentes

**Componentes** são os blocos de construção fundamentais do React. Eles permitem dividir a interface do usuário em partes independentes e reutilizáveis, facilitando a manutenção e organização do código.

### O que são Componentes?

- **Definição**: Funções JavaScript que retornam JSX
- **Reutilização**: Podem ser usados múltiplas vezes
- **Isolamento**: Cada componente tem sua própria lógica e estilo
- **Composição**: Componentes podem usar outros componentes

### Vantagens dos Componentes

- **Reutilização de código**: Escreva uma vez, use várias vezes
- **Manutenção**: Mais fácil de encontrar e corrigir problemas
- **Organização**: Código dividido em partes lógicas
- **Colaboração**: Diferentes desenvolvedores podem trabalhar em componentes diferentes

### Anatomia de um Componente

```jsx
// Componente simples
function MinhasMensagem() {
  return <h1>Olá, mundo!</h1>;
}

// Componente com múltiplos elementos
function CartaoUsuario() {
  return (
    <div className="cartao">
      <h2>João Silva</h2>
      <p>Desenvolvedor React</p>
      <button>Ver Perfil</button>
    </div>
  );
}
```

### Regras Importantes

1. **Nome com letra maiúscula**: `MinhaComponente` (não `minhaComponente`)
2. **Deve retornar JSX**: Sempre retorne algo renderizável
3. **Um elemento raiz**: Use `<div>` ou `<>` para envolver múltiplos elementos
4. **Export/Import**: Use `export default` para exportar

## Evoluindo o Projeto: Componentizando a Lista de Países

Vamos pegar nosso projeto do módulo anterior e dividi-lo em componentes reutilizáveis.

### Versão Anterior (Monolítica):

```jsx
// App.jsx - Tudo em um componente
function App() {
  return (
    <div className="app">
      <h1>🌍 Lista de Países</h1>
      <div className="country-grid">
        <div className="country-card">
          <h3>🇧🇷 Brasil</h3>
          <p>Capital: Brasília</p>
        </div>
        <div className="country-card">
          <h3>🇦🇷 Argentina</h3>
          <p>Capital: Buenos Aires</p>
        </div>
        <div className="country-card">
          <h3>🇨🇱 Chile</h3>
          <p>Capital: Santiago</p>
        </div>
      </div>
    </div>
  );
}
```

### Nova Versão (Componentizada):

**1. Criando o componente CountryCard:**

```jsx
// src/components/CountryCard.jsx
function CountryCard() {
  return (
    <div className="country-card">
      <h3>🇧🇷 Brasil</h3>
      <p>Capital: Brasília</p>
    </div>
  );
}

export default CountryCard;
```

**2. Criando o componente Header:**

```jsx
// src/components/Header.jsx
function Header() {
  return (
    <header className="app-header">
      <h1>🌍 Lista de Países</h1>
      <p>Explore países ao redor do mundo</p>
    </header>
  );
}

export default Header;
```

**3. Criando o componente CountryGrid:**

```jsx
// src/components/CountryGrid.jsx
import CountryCard from './CountryCard';

function CountryGrid() {
  return (
    <div className="country-grid">
      <CountryCard />
      <CountryCard />
      <CountryCard />
    </div>
  );
}

export default CountryGrid;
```

**4. App.jsx simplificado:**

```jsx
// src/App.jsx
import Header from './components/Header';
import CountryGrid from './components/CountryGrid';
import './App.css';

function App() {
  return (
    <div className="app">
      <Header />
      <CountryGrid />
    </div>
  );
}

export default App;
```

### Estrutura de Pastas Organizada

```
src/
├── components/
│   ├── Header.jsx
│   ├── CountryCard.jsx
│   └── CountryGrid.jsx
├── App.jsx
├── App.css
└── main.jsx
```

### CSS Atualizado

```css
/* App.css */
.app {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Arial, sans-serif;
}

.app-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 10px;
}

.app-header h1 {
  margin: 0 0 10px 0;
  font-size: 2.5em;
}

.app-header p {
  margin: 0;
  opacity: 0.9;
}

.country-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.country-card {
  border: 1px solid #e1e8ed;
  border-radius: 12px;
  padding: 20px;
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.country-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.country-card h3 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 1.3em;
}

.country-card p {
  margin: 5px 0;
  color: #666;
}
```

## Conceitos Importantes de Componentes

### 1. **Reutilização**
- O mesmo componente pode ser usado várias vezes
- Cada instância é independente
- Facilita manutenção do código

### 2. **Responsabilidade Única**
- Cada componente deve ter uma função específica
- Header → cabeçalho da aplicação
- CountryCard → exibir informações de um país
- CountryGrid → organizar múltiplos países

### 3. **Hierarquia de Componentes**
```
App
├── Header
└── CountryGrid
    ├── CountryCard
    ├── CountryCard
    └── CountryCard
```

### 4. **Import/Export**
```jsx
// Exportar (no final do arquivo)
export default CountryCard;

// Importar (no início do arquivo)
import CountryCard from './CountryCard';
```

### Exercícios Práticos

**1. Criar novos componentes:**
- Crie um componente `Footer` com informações do site
- Adicione um componente `Navigation` com links fictícios

**2. Modificar componentes existentes:**
- Adicione mais informações no `CountryCard` (população, idioma)
- Personalize as cores e estilos

**3. Experimentar com estrutura:**
- Mova os componentes para subpastas organizadas
- Crie variações do `CountryCard` (pequeno, médio, grande)

### Próximos Passos

No próximo módulo aprenderemos sobre **Props**, que permitirão passar dados para os componentes, tornando-os verdadeiramente dinâmicos e reutilizáveis. Transformaremos nossos cartões de países estáticos em componentes que podem exibir informações diferentes!
