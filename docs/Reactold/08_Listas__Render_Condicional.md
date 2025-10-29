---
id: 08_Listas_e_Render_Condicional
title: 08 - Listas e Renderização Condicional
---

# 08 - **Listas e Renderização Condicional**

Neste módulo, você aprenderá como criar listas dinâmicas e implementar lógica condicional na renderização de componentes React. Continuaremos evoluindo nosso projeto **Lista de Países** para incluir múltiplos países e funcionalidades interativas.

---

## **Objetivos do Módulo**
- Renderizar listas de dados usando o método `.map()`
- Entender a importância da prop `key` em listas
- Implementar renderização condicional (operadores `&&` e ternário)
- Evoluir o projeto Lista de Países com dados dinâmicos

---

## **1. Renderizando Listas com `.map()`**

O método `.map()` é fundamental no React para transformar arrays de dados em arrays de elementos JSX.

### **Conceito Básico**

```jsx
const numeros = [1, 2, 3, 4, 5];
const listaElementos = numeros.map(numero => <li key={numero}>{numero}</li>);
```

### **Evoluindo Nossa Lista de Países**

Vamos transformar nosso componente estático em uma lista dinâmica:

```jsx
// src/App.jsx
import React, { useState } from 'react';
import './App.css';

function App() {
  // Array de países (simulando dados que virão de uma API)
  const [paises] = useState([
    {
      id: 1,
      nome: "Brasil",
      capital: "Brasília",
      populacao: "215 milhões",
      bandeira: "🇧🇷",
      regiao: "América do Sul"
    },
    {
      id: 2,
      nome: "França",
      capital: "Paris",
      populacao: "67 milhões",
      bandeira: "🇫🇷",
      regiao: "Europa"
    },
    {
      id: 3,
      nome: "Japão",
      capital: "Tóquio",
      populacao: "125 milhões",
      bandeira: "🇯🇵",
      regiao: "Ásia"
    },
    {
      id: 4,
      nome: "Austrália",
      capital: "Camberra",
      populacao: "26 milhões",
      bandeira: "🇦🇺",
      regiao: "Oceania"
    }
  ]);

  const [favoritos, setFavoritos] = useState([]);

  const toggleFavorito = (paisId) => {
    setFavoritos(prev => 
      prev.includes(paisId)
        ? prev.filter(id => id !== paisId)
        : [...prev, paisId]
    );
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🌍 Lista de Países</h1>
        <p>Descubra informações sobre países ao redor do mundo</p>
      </header>

      <main className="countries-grid">
        {paises.map(pais => (
          <CountryCard 
            key={pais.id}
            pais={pais}
            isFavorito={favoritos.includes(pais.id)}
            onToggleFavorito={() => toggleFavorito(pais.id)}
          />
        ))}
      </main>
    </div>
  );
}

// Componente CountryCard atualizado
function CountryCard({ pais, isFavorito, onToggleFavorito }) {
  return (
    <div className="country-card">
      <div className="country-flag">{pais.bandeira}</div>
      <div className="country-info">
        <h2>{pais.nome}</h2>
        <p><strong>Capital:</strong> {pais.capital}</p>
        <p><strong>População:</strong> {pais.populacao}</p>
        <p><strong>Região:</strong> {pais.regiao}</p>
        
        <button 
          className={`favorite-btn ${isFavorito ? 'favorited' : ''}`}
          onClick={onToggleFavorito}
        >
          {isFavorito ? '❤️ Remover' : '🤍 Favoritar'}
        </button>
      </div>
    </div>
  );
}

export default App;
```

---

## **2. A Importância da Prop `key`**

### **Por que usar `key`?**

O React usa a prop `key` para identificar quais itens da lista mudaram, foram adicionados ou removidos, otimizando as atualizações do DOM.

### **❌ Exemplo Problemático**
```jsx
// NUNCA faça isso - índice como key pode causar problemas
{paises.map((pais, index) => (
  <CountryCard key={index} pais={pais} />
))}
```

### **✅ Exemplo Correto**
```jsx
// Use um identificador único estável
{paises.map(pais => (
  <CountryCard key={pais.id} pais={pais} />
))}
```

---

## **3. Renderização Condicional**

### **Operador Lógico `&&`**

Use quando quiser mostrar algo **apenas se** uma condição for verdadeira:

```jsx
function App() {
  const [paises] = useState([...]);
  const [favoritos, setFavoritos] = useState([1, 3]);

  return (
    <div className="app">
      {/* Mostrar contador apenas se há favoritos */}
      {favoritos.length > 0 && (
        <div className="favorites-counter">
          <p>❤️ Você tem {favoritos.length} países favoritos</p>
        </div>
      )}

      {/* Lista de países */}
      <main className="countries-grid">
        {paises.map(pais => (
          <CountryCard 
            key={pais.id}
            pais={pais}
            isFavorito={favoritos.includes(pais.id)}
            onToggleFavorito={() => toggleFavorito(pais.id)}
          />
        ))}
      </main>

      {/* Mostrar mensagem se não há países */}
      {paises.length === 0 && (
        <div className="empty-state">
          <p>🌍 Nenhum país encontrado</p>
        </div>
      )}
    </div>
  );
}
```

### **Operador Ternário**

Use quando quiser mostrar **uma coisa OU outra**:

```jsx
function CountryCard({ pais, isFavorito, onToggleFavorito }) {
  return (
    <div className="country-card">
      {/* Condicional para o ícone */}
      <div className="country-status">
        {isFavorito ? '⭐ Favorito' : '🤍 Adicionar aos favoritos'}
      </div>
      
      <div className="country-flag">{pais.bandeira}</div>
      <div className="country-info">
        <h2>{pais.nome}</h2>
        <p><strong>Capital:</strong> {pais.capital}</p>
        
        {/* Condicional para população */}
        <p className={pais.populacao > 100 ? 'high-population' : 'low-population'}>
          <strong>População:</strong> {pais.populacao}
          {parseInt(pais.populacao) > 100 ? ' 📈' : ' 📊'}
        </p>
        
        <button 
          className={`favorite-btn ${isFavorito ? 'favorited' : ''}`}
          onClick={onToggleFavorito}
        >
          {isFavorito ? '❤️ Remover' : '🤍 Favoritar'}
        </button>
      </div>
    </div>
  );
}
```

---

## **4. Atualização do CSS**

```css
/* src/App.css */
.app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.app-header {
  text-align: center;
  margin-bottom: 30px;
}

.app-header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 10px;
}

.app-header p {
  font-size: 1.1rem;
  color: #7f8c8d;
}

.favorites-counter {
  background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
  color: white;
  padding: 15px;
  border-radius: 10px;
  text-align: center;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.countries-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.country-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.country-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.country-status {
  font-size: 0.9rem;
  margin-bottom: 10px;
  padding: 5px 10px;
  border-radius: 20px;
  background: #f8f9fa;
  color: #6c757d;
}

.country-flag {
  font-size: 4rem;
  margin: 15px 0;
}

.country-info h2 {
  color: #2c3e50;
  margin: 15px 0 10px 0;
  font-size: 1.5rem;
}

.country-info p {
  margin: 8px 0;
  color: #5a6c7d;
  line-height: 1.5;
}

.high-population {
  color: #e74c3c !important;
  font-weight: bold;
}

.low-population {
  color: #27ae60 !important;
}

.favorite-btn {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 25px;
  cursor: pointer;
  font-size: 1rem;
  margin-top: 15px;
  transition: all 0.3s ease;
}

.favorite-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(52, 152, 219, 0.3);
}

.favorite-btn.favorited {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #7f8c8d;
  font-size: 1.2rem;
}

/* Responsividade */
@media (max-width: 768px) {
  .countries-grid {
    grid-template-columns: 1fr;
  }
  
  .app-header h1 {
    font-size: 2rem;
  }
  
  .country-flag {
    font-size: 3rem;
  }
}
```

---

## **5. Conceitos Importantes**

### **🎯 Keys em React**
- Sempre use um identificador único e estável
- Evite usar índices do array como keys
- Keys ajudam o React a otimizar renderizações

### **🎯 Renderização Condicional**
- **`condição && <elemento>`**: Mostra elemento apenas se condição for true
- **`condição ? <elementoA> : <elementoB>`**: Mostra elementoA ou elementoB
- Use para criar interfaces dinâmicas e responsivas

### **🎯 Estado de Arrays**
- Use `useState` para gerenciar listas de dados
- Modifique arrays de forma imutável (spread operator, filter, map)

---

## **📝 Exercício Prático**

### 🎯 **Objetivo**
Adicionar funcionalidade de filtro por região à Lista de Países

### 📋 **Requisitos**
- [ ] Criar botões para filtrar por região (Todas, América do Sul, Europa, Ásia, Oceania)
- [ ] Implementar estado para região selecionada
- [ ] Mostrar apenas países da região selecionada
- [ ] Exibir contador de países visíveis
- [ ] Mostrar mensagem quando nenhum país for encontrado

### 🚀 **Dica de Implementação**
```jsx
const [regiaoSelecionada, setRegiaoSelecionada] = useState('Todas');

const paisesFiltrados = regiaoSelecionada === 'Todas' 
  ? paises 
  : paises.filter(pais => pais.regiao === regiaoSelecionada);
```

---

## **🔮 Próximo Módulo**

No próximo módulo, aprenderemos sobre **HTTP e APIs**, onde conectaremos nossa Lista de Países a uma API real para buscar dados de países do mundo todo!