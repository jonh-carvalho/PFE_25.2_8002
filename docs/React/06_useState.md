---
id: 06_useState
title: 06 - Estado com useState
---

# 06 - **Estado com useState**

## Introdução

**Estado** é uma das características mais importantes do React. Ele permite que componentes "lembrem" de informações e reajam a mudanças, tornando a interface dinâmica e interativa.

### O que é Estado?

- **Definição**: Dados que podem mudar ao longo do tempo em um componente
- **Reatividade**: Quando o estado muda, o componente re-renderiza automaticamente
- **Local**: Cada componente gerencia seu próprio estado
- **useState**: Hook que permite adicionar estado a componentes funcionais

### Por que usar Estado?

- **Interatividade**: Responder a ações do usuário (cliques, digitação)
- **Dinamismo**: Conteúdo que muda baseado em condições
- **Experiência**: Interfaces mais ricas e responsivas
- **Dados temporários**: Armazenar informações que não vem de props

### Sintaxe do useState

```jsx
import { useState } from 'react';

function MeuComponente() {
  // [variável, função para atualizar] = useState(valor inicial)
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');
  const [isVisible, setIsVisible] = useState(true);

  return (
    <div>
      <p>Contador: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Incrementar
      </button>
    </div>
  );
}
```

### Regras Importantes

1. **Importe useState**: `import { useState } from 'react'`
2. **Use no topo**: Sempre no início da função do componente
3. **Não em loops/condições**: useState deve ser sempre executado
4. **Estado é imutável**: Use sempre a função set para atualizar

## Evoluindo o Projeto: Adicionando Interatividade

Vamos adicionar funcionalidades interativas ao nosso projeto "Lista de Países" usando useState.

### Funcionalidades a Implementar:

1. **Favoritar países**: Marcar/desmarcar países como favoritos
2. **Contador de favoritos**: Mostrar quantos países foram favoritados
3. **Filtro de favoritos**: Mostrar apenas países favoritos
4. **Adicionar país**: Permitir adicionar novos países à lista

### 1. Componente com Estado - Favoritos

```jsx
// src/components/CountryCard.jsx
function CountryCard({ id, flag, name, capital, population, language, isFavorite = false, onToggleFavorite }) {
  
  const handleCardClick = () => {
    onToggleFavorite?.(id);
  };

  return (
    <div 
      className={`country-card ${isFavorite ? 'favorite' : ''}`}
      onClick={handleCardClick}
    >
      <div className="country-header">
        <span className="flag">{flag}</span>
        <h3>{name}</h3>
        <button 
          className="favorite-btn"
          onClick={(e) => { e.stopPropagation(); onToggleFavorite?.(id); }}
          title={isFavorite ? 'Remover dos favoritos' : 'Adicionar aos favoritos'}
        >
          {isFavorite ? '❤️' : '🤍'}
        </button>
      </div>
      <div className="country-info">
        <p><strong>Capital:</strong> {capital}</p>
        <p><strong>População:</strong> {population}</p>
        <p><strong>Idioma:</strong> {language}</p>
        {isFavorite && <p className="favorite-badge">⭐ Favorito</p>}
      </div>
    </div>
  );
}

export default CountryCard;
```

### 2. Contador de Favoritos no Header

```jsx
// src/components/Header.jsx
function Header({ title, subtitle, favoriteCount  }) {
  return (
    <header className="app-header">
      <h1>{title}</h1>
      {subtitle && <p>{subtitle}</p>}

      <div className="favorite-counter">
        <span>❤️ {favoriteCount} países favoritos</span>
      </div>

    </header>
  );
}
export default Header;
```

### 3. App com Estado Global

```jsx
// src/App.jsx
import { useState } from 'react';
import './App.css';
import CountryGrid from './components/CountryGrid';
import Header from './components/Header';

function App() {
  const [countries, setCountries] = useState([
    { id: 1, flag: "🇧🇷", name: "Brasil", capital: "Brasília", population: "215 milhões", language: "Português" },
    { id: 2, flag: "🇦🇷", name: "Argentina", capital: "Buenos Aires", population: "45 milhões", language: "Espanhol" },
    { id: 3, flag: "🇨🇱", name: "Chile", capital: "Santiago", population: "19 milhões", language: "Espanhol" },
    { id: 4, flag: "🇺🇾", name: "Uruguai", capital: "Montevidéu", population: "3.5 milhões", language: "Espanhol" },
    { id: 5, flag: "🇵🇪", name: "Peru", capital: "Lima", population: "33 milhões", language: "Espanhol" },
    { id: 6, flag: "🇨🇴", name: "Colômbia", capital: "Bogotá", population: "51 milhões", language: "Espanhol" }
  ]);
  // Armazena os IDs dos países favoritos
  const [favorites, setFavorites] = useState([]);
  const [showOnlyFavorites, setShowOnlyFavorites] = useState(false);

  const toggleFavorite = (id) => {
    setFavorites((prev) =>
      prev.includes(id) ? prev.filter((fid) => fid !== id) : [...prev, id]
    );
  };

  const favoriteCount = favorites.length;

  const visibleCountries = showOnlyFavorites
    ? countries.filter((c) => favorites.includes(c.id))
    : countries;

  return (
    <div className="app">
      <Header 
        title="🌍 Lista de Países da América do Sul"
        subtitle="Explore países sul-americanos e suas informações"
        favoriteCount={favoriteCount}
      />
      
      <div className="controls">
        <button 
          className={`filter-btn ${showOnlyFavorites ? 'active' : ''}`}
          onClick={() => setShowOnlyFavorites(!showOnlyFavorites)}
        >
          {showOnlyFavorites ? 'Mostrar Todos' : 'Mostrar Favoritos'}
        </button>
      </div>
      
      <CountryGrid 
        countries={visibleCountries}
        favorites={favorites}
        onToggleFavorite={toggleFavorite}
      />
    </div>
  );
}

export default App;
```

### 4. CountryGrid para "impressão" de países usando map

```
// src/components/CountryGrid.jsx
import CountryCard from './CountryCard';

function CountryGrid({ countries, favorites = [], onToggleFavorite }) {
  return (
    <div className="country-grid">
      {countries.map((country) => (
        <CountryCard 
          key={country.id}
          id={country.id}
          flag={country.flag}
          name={country.name}
          capital={country.capital}
          population={country.population}
          language={country.language}
          isFavorite={favorites.includes(country.id)}
          onToggleFavorite={onToggleFavorite}
        />
      ))}
    </div>
  );
}

export default CountryGrid;
```

### 5. CSS Atualizado para Interatividade

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

.favorite-counter {
  margin-top: 15px;
  background: rgba(255,255,255,0.2);
  padding: 10px 20px;
  border-radius: 25px;
  display: inline-block;
  font-weight: bold;
}

.controls {
  text-align: center;
  margin-bottom: 30px;
}

.filter-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  background: #2980b9;
  transform: translateY(-2px);
}

.filter-btn.active {
  background: #e74c3c;
}

.country-card {
  border: 1px solid #e1e8ed;
  border-radius: 15px;
  padding: 25px;
  background: white;
  box-shadow: 0 3px 10px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.country-card.favorite {
  border-color: #e74c3c;
  box-shadow: 0 3px 15px rgba(231, 76, 60, 0.2);
}

.country-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 15px;
}

.favorite-btn {
  background: none;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
  padding: 5px;
  border-radius: 50%;
  transition: transform 0.2s ease;
}

.favorite-btn:hover {
  transform: scale(1.2);
}

.favorite-badge {
  color: #e74c3c;
  font-weight: bold;
  margin-top: 10px;
}
```

## Conceitos Importantes do useState

### 1. **Estado é Assíncrono**
```jsx
function Counter() {
  const [count, setCount] = useState(0);

  const handleClick = () => {
    setCount(count + 1);
    console.log(count); // ⚠️ Ainda mostra valor antigo
  };

  // ✅ Use useEffect para reagir a mudanças
  useEffect(() => {
    console.log(count); // Valor atualizado
  }, [count]);
}
```

### 2. **Atualizações por Função**
```jsx
// ❌ Problemático em múltiplas atualizações
setCount(count + 1);
setCount(count + 1); // Só incrementa 1

// ✅ Correto para múltiplas atualizações
setCount(prevCount => prevCount + 1);
setCount(prevCount => prevCount + 1); // Incrementa 2
```

### 3. **Estado com Objetos**
```jsx
const [user, setUser] = useState({ name: '', age: 0 });

// ❌ Não modifique diretamente
user.name = 'João'; // Não funciona

// ✅ Crie novo objeto
setUser({ ...user, name: 'João' });
```

### 4. **Estado com Arrays**
```jsx
const [items, setItems] = useState([]);

// Adicionar item
setItems([...items, novoItem]);

// Remover item
setItems(items.filter(item => item.id !== idToRemove));

// Atualizar item
setItems(items.map(item => 
  item.id === id ? { ...item, updated: true } : item
));
```

### Exercícios Práticos

**1. Contador Avançado:**
- Criar botões para incrementar, decrementar e resetar
- Adicionar limite mínimo e máximo
- Mostrar mensagens baseadas no valor

**2. Lista de Tarefas:**
- Adicionar novas tarefas
- Marcar como concluída
- Remover tarefas
- Contar tarefas pendentes

**3. Expandir o projeto de países:**
- Adicionar formulário para novos países
- Implementar busca por nome
- Adicionar modo escuro/claro

### Próximos Passos

No próximo módulo aprenderemos sobre **Eventos e Formulários**, onde combinaremos useState com manipulação de eventos para criar formulários interativos e validação de dados!

### Resumo

- **useState**: Hook para adicionar estado a componentes
- **Reatividade**: Mudanças no estado re-renderizam o componente
- **Imutabilidade**: Sempre criar novos valores, não modificar existentes
- **Assíncrono**: Atualizações de estado não são imediatas
- **Função setter**: Use funções para atualizações baseadas no valor anterior
- **Projeto prático**: Lista de países com funcionalidades interativas
