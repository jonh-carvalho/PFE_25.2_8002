---
id: 05_Props_e_Comunicação
title: 05 - Props e Comunicação Entre Componentes
---

# 05 - **Props e Comunicação Entre Componentes**

## Introdução

**Props** (propriedades) são a forma principal de passar dados entre componentes no React. Eles tornam os componentes dinâmicos e reutilizáveis, permitindo que o mesmo componente exiba informações diferentes dependendo dos dados que recebe.

### O que são Props?

- **Definição**: Argumentos passados para componentes React
- **Finalidade**: Permitir comunicação entre componentes pai e filho
- **Características**: São somente leitura (imutáveis)
- **Analogia**: Como parâmetros de uma função JavaScript

### Por que usar Props?

- **Reutilização**: Um componente pode exibir dados diferentes
- **Dinâmico**: Conteúdo muda baseado nos dados recebidos
- **Modularidade**: Separação clara entre dados e apresentação
- **Manutenção**: Facilita alterações e correções

### Sintaxe Básica de Props

**Passando props (componente pai):**

```jsx
// App.jsx
function App() {
  return (
    <div>
      <CountryCard 
        flag="🇧🇷"
        name="Brasil"
        capital="Brasília"
        population="215 milhões"
      />
      <CountryCard 
        flag="🇦🇷"
        name="Argentina"
        capital="Buenos Aires"
        population="45 milhões"
      />
    </div>
  );
}
```

**Recebendo props (componente filho):**

```jsx
// CountryCard.jsx
function CountryCard(props) {
  return (
    <div className="country-card">
      <h3>{props.flag} {props.name}</h3>
      <p>Capital: {props.capital}</p>
      <p>População: {props.population}</p>
    </div>
  );
}
```

### Destruturação de Props

Uma forma mais limpa de trabalhar com props:

```jsx
// Versão com destruturação
function CountryCard({ flag, name, capital, population }) {
  return (
    <div className="country-card">
      <h3>{flag} {name}</h3>
      <p>Capital: {capital}</p>
      <p>População: {population}</p>
    </div>
  );
}
```

## Evoluindo o Projeto: Tornando os Componentes Dinâmicos

Vamos pegar nosso projeto "Lista de Países" e torná-lo dinâmico usando props.

### Versão Anterior (Estática):

```jsx
// CountryCard.jsx - Dados fixos
function CountryCard() {
  return (
    <div className="country-card">
      <h3>🇧🇷 Brasil</h3>
      <p>Capital: Brasília</p>
    </div>
  );
}
```

### Nova Versão (Dinâmica com Props):

**1. CountryCard atualizado:**

```jsx
// src/components/CountryCard.jsx
function CountryCard({ flag, name, capital, population, language }) {
  return (
    <div className="country-card">
      <div className="country-header">
        <span className="flag">{flag}</span>
        <h3>{name}</h3>
      </div>
      <div className="country-info">
        <p><strong>Capital:</strong> {capital}</p>
        <p><strong>População:</strong> {population}</p>
        <p><strong>Idioma:</strong> {language}</p>
      </div>
    </div>
  );
}

export default CountryCard;
```

**2. CountryGrid atualizado:**

```jsx
// src/components/CountryGrid.jsx
import CountryCard from './CountryCard';

function CountryGrid() {
  return (
    <div className="country-grid">
      <CountryCard 
        flag="🇧🇷"
        name="Brasil"
        capital="Brasília"
        population="215 milhões"
        language="Português"
      />
      <CountryCard 
        flag="🇦🇷"
        name="Argentina"
        capital="Buenos Aires"
        population="45 milhões"
        language="Espanhol"
      />
      <CountryCard 
        flag="🇨🇱"
        name="Chile"
        capital="Santiago"
        population="19 milhões"
        language="Espanhol"
      />
      <CountryCard 
        flag="🇺🇾"
        name="Uruguai"
        capital="Montevidéu"
        population="3.5 milhões"
        language="Espanhol"
      />
      <CountryCard 
        flag="🇵🇪"
        name="Peru"
        capital="Lima"
        population="33 milhões"
        language="Espanhol"
      />
      <CountryCard 
        flag="🇨🇴"
        name="Colômbia"
        capital="Bogotá"
        population="51 milhões"
        language="Espanhol"
      />
    </div>
  );
}

export default CountryGrid;
```

**3. Header com props:**

```jsx
// src/components/Header.jsx
function Header({ title, subtitle }) {
  return (
    <header className="app-header">
      <h1>{title}</h1>
      {subtitle && <p>{subtitle}</p>}
    </header>
  );
}

export default Header;
```

**4. App.jsx atualizado:**

```jsx
// src/App.jsx
import Header from './components/Header';
import CountryGrid from './components/CountryGrid';
import './App.css';

function App() {
  return (
    <div className="app">
      <Header 
        title="🌍 Lista de Países da América do Sul"
        subtitle="Explore países sul-americanos e suas informações"
      />
      <CountryGrid />
    </div>
  );
}

export default App;
```

### CSS Atualizado para Melhor Visual

```css
/* App.css */
.app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Arial, sans-serif;
}

.app-header {
  text-align: center;
  margin-bottom: 40px;
  padding: 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.app-header h1 {
  margin: 0 0 10px 0;
  font-size: 2.8em;
}

.app-header p {
  margin: 0;
  opacity: 0.9;
  font-size: 1.1em;
}

.country-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 25px;
}

.country-card {
  border: 1px solid #e1e8ed;
  border-radius: 15px;
  padding: 25px;
  background: white;
  box-shadow: 0 3px 10px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.country-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.country-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.flag {
  font-size: 2.5em;
  margin-right: 15px;
}

.country-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.4em;
}

.country-info p {
  margin: 8px 0;
  color: #666;
  font-size: 1em;
}

.country-info strong {
  color: #333;
}
```

## Conceitos Importantes sobre Props

### 1. **Props são Imutáveis**
```jsx
function CountryCard({ name }) {
  // ❌ ERRO: Não pode modificar props
  // name = "Novo Nome";
  
  // ✅ CORRETO: Apenas usar props
  return <h3>{name}</h3>;
}
```

### 2. **Props Padrão (Default Props)**
```jsx
function CountryCard({ name = "País Desconhecido", population = "N/A" }) {
  return (
    <div>
      <h3>{name}</h3>
      <p>População: {population}</p>
    </div>
  );
}
```

### 3. **Tipos de Props**
```jsx
function CountryCard({ 
  name,           // string
  population,     // string ou number
  isVisited,      // boolean
  languages,      // array
  details         // object
}) {
  return (
    <div>
      <h3>{name}</h3>
      <p>População: {population}</p>
      {isVisited && <span>✅ Visitado</span>}
      <p>Idiomas: {languages.join(', ')}</p>
      <p>Área: {details.area} km²</p>
    </div>
  );
}
```

### 4. **Props Children**
```jsx
function Card({ children }) {
  return (
    <div className="card">
      {children}
    </div>
  );
}

// Uso:
<Card>
  <h2>Título do Card</h2>
  <p>Conteúdo do card</p>
</Card>
```

### Exercícios Práticos

**1. Expandir o CountryCard:**
- Adicione props para continente, moeda e fuso horário
- Implemente renderização condicional para props opcionais

**2. Criar novos componentes com props:**
- `StatCard` para exibir estatísticas (número, label, ícone)
- `Button` personalizado (texto, cor, tamanho)

**3. Praticar diferentes tipos de props:**
- Props string, number, boolean e array
- Props com valores padrão
- Props children para conteúdo aninhado

### Próximos Passos

No próximo módulo aprenderemos sobre **Estado (useState)**, que permitirá que nossos componentes tenham dados que mudam ao longo do tempo. Vamos adicionar interatividade ao nosso projeto, como favoritar países e adicionar novos à lista!

### Resumo

- **Props**: Permitem comunicação pai → filho
- **Imutáveis**: Não podem ser modificados pelo componente filho  
- **Dinâmicos**: Tornam componentes reutilizáveis
- **Tipos**: Strings, numbers, booleans, arrays, objects, functions
- **Destruturação**: Forma limpa de acessar props
- **Padrão**: Valores default para props opcionais
