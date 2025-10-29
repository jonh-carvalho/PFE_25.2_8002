---
id: 09_HTTP_APIs
title: 09 - HTTP e APIs
---
# 09 - **HTTP e APIs**

Neste módulo, você aprenderá os conceitos fundamentais de HTTP, APIs e como buscar dados externos para alimentar aplicações React. Prepararemos nosso projeto **Lista de Países** para receber dados reais de uma API externa.

---

## **Objetivos do Módulo**
- Entender o protocolo HTTP e métodos de requisição
- Conhecer APIs REST e como elas funcionam
- Usar `fetch()` para fazer requisições HTTP
- Preparar a Lista de Países para consumir dados externos
- Tratar erros e estados de carregamento

---

## **1. Introdução ao HTTP**

### **O que é HTTP?**

**HTTP** (Hypertext Transfer Protocol) é o protocolo que permite a comunicação entre navegadores e servidores na web.

### **Como funciona?**

1. **Cliente faz uma requisição** → Seu navegador/app solicita dados
2. **Servidor processa** → Analisa a solicitação
3. **Servidor responde** → Envia os dados ou erro
4. **Cliente recebe** → Processa a resposta

```
Cliente (React App) ←→ Servidor (API)
      ↓ GET /countries     ↓ 200 OK + dados
      ↓ POST /favorites    ↓ 201 Created
```

### **Métodos HTTP Principais**

| Método | Propósito | Exemplo de Uso |
|--------|-----------|----------------|
| **GET** | Buscar dados | Listar países |
| **POST** | Criar dados | Adicionar favorito |
| **PUT** | Atualizar (substituir) | Editar país completo |
| **PATCH** | Atualizar (parcial) | Editar apenas nome |
| **DELETE** | Remover dados | Excluir favorito |

### **Códigos de Status HTTP**

| Código | Significado | Exemplo |
|--------|-------------|---------|
| **200** | ✅ Sucesso | Dados recebidos |
| **201** | ✅ Criado | Favorito adicionado |
| **400** | ❌ Erro do cliente | Dados inválidos |
| **404** | ❌ Não encontrado | País inexistente |
| **500** | ❌ Erro do servidor | Servidor offline |

---

## **2. APIs e JSON**

### **O que é uma API?**

**API** (Application Programming Interface) é um conjunto de regras que permite que aplicações conversem entre si.

### **API REST**

REST é um padrão arquitetural para APIs que usa HTTP de forma organizada:

```
GET    /countries          → Lista todos os países
GET    /countries/brazil   → Busca país específico
POST   /countries          → Cria novo país
PUT    /countries/brazil   → Atualiza país completo
DELETE /countries/brazil   → Remove país
```

### **Formato JSON**

APIs geralmente retornam dados em formato **JSON** (JavaScript Object Notation):

```json
{
  "name": {
    "common": "Brazil",
    "official": "Federative Republic of Brazil"
  },
  "capital": ["Brasília"],
  "population": 215353593,
  "region": "Americas",
  "subregion": "South America",
  "flag": "🇧🇷",
  "flags": {
    "png": "https://flagcdn.com/w320/br.png"
  }
}
```

---

## **3. Usando `fetch()` no JavaScript**

### **Sintaxe Básica**

```javascript
fetch(url)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### **Exemplo Prático: API REST Countries**

```javascript
// Buscar todos os países
const buscarPaises = async () => {
  try {
    const response = await fetch('https://restcountries.com/v3.1/all');
    
    if (!response.ok) {
      throw new Error(`Erro HTTP: ${response.status}`);
    }
    
    const paises = await response.json();
    console.log(paises);
  } catch (error) {
    console.error('Erro ao buscar países:', error);
  }
};
```

### **Configurações Avançadas do Fetch**

```javascript
// Requisição POST com dados
const adicionarFavorito = async (pais) => {
  try {
    const response = await fetch('/api/favoritos', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        nome: pais.name.common,
        codigo: pais.cca3
      })
    });
    
    if (!response.ok) {
      throw new Error('Erro ao adicionar favorito');
    }
    
    const resultado = await response.json();
    return resultado;
  } catch (error) {
    console.error('Erro:', error);
    throw error;
  }
};
```

---

## **4. Preparando a Lista de Países para APIs**

Vamos evoluir nosso projeto para se preparar para dados reais:

### **Componente de Carregamento**

```jsx
// src/components/Loading.jsx
import React from 'react';

function Loading() {
  return (
    <div className="loading">
      <div className="loading-spinner"></div>
      <p>Carregando países...</p>
    </div>
  );
}

export default Loading;
```

### **Componente de Erro**

```jsx
// src/components/ErrorMessage.jsx
import React from 'react';

function ErrorMessage({ mensagem, onTentar }) {
  return (
    <div className="error-message">
      <h3>❌ Ops! Algo deu errado</h3>
      <p>{mensagem}</p>
      <button onClick={onTentar} className="retry-btn">
        🔄 Tentar Novamente
      </button>
    </div>
  );
}

export default ErrorMessage;
```

### **App.jsx Preparado para APIs**

```jsx
// src/App.jsx
import React, { useState } from 'react';
import Loading from './components/Loading';
import ErrorMessage from './components/ErrorMessage';
import './App.css';

function App() {
  // Estados para gerenciar dados da API
  const [paises, setPaises] = useState([]);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState(null);
  const [favoritos, setFavoritos] = useState([]);

  // Simulação de dados (será substituída por API real)
  const dadosSimulados = [
    {
      name: { common: "Brasil" },
      capital: ["Brasília"],
      population: 215353593,
      region: "Americas",
      flag: "🇧🇷",
      cca3: "BRA"
    },
    {
      name: { common: "França" },
      capital: ["Paris"],
      population: 67391582,
      region: "Europe",
      flag: "🇫🇷",
      cca3: "FRA"
    }
  ];

  // Função que simula busca da API
  const buscarPaises = async () => {
    setCarregando(true);
    setErro(null);
    
    try {
      // Simular delay de rede
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Simular possível erro (30% de chance)
      if (Math.random() < 0.3) {
        throw new Error('Erro de conexão com o servidor');
      }
      
      setPaises(dadosSimulados);
    } catch (error) {
      setErro(error.message);
    } finally {
      setCarregando(false);
    }
  };

  const toggleFavorito = (paisCodigo) => {
    setFavoritos(prev => 
      prev.includes(paisCodigo)
        ? prev.filter(codigo => codigo !== paisCodigo)
        : [...prev, paisCodigo]
    );
  };

  // Carregar dados na inicialização (será substituído por useEffect)
  React.useEffect(() => {
    buscarPaises();
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <h1>🌍 Lista de Países</h1>
        <p>Dados obtidos via API REST Countries</p>
        
        {paises.length > 0 && (
          <div className="stats">
            <span>📊 {paises.length} países</span>
            <span>❤️ {favoritos.length} favoritos</span>
          </div>
        )}
      </header>

      <main className="main-content">
        {carregando && <Loading />}
        
        {erro && (
          <ErrorMessage 
            mensagem={erro} 
            onTentar={buscarPaises}
          />
        )}
        
        {!carregando && !erro && paises.length > 0 && (
          <div className="countries-grid">
            {paises.map(pais => (
              <CountryCard 
                key={pais.cca3}
                pais={pais}
                isFavorito={favoritos.includes(pais.cca3)}
                onToggleFavorito={() => toggleFavorito(pais.cca3)}
              />
            ))}
          </div>
        )}
        
        {!carregando && !erro && paises.length === 0 && (
          <div className="empty-state">
            <p>🌍 Nenhum país encontrado</p>
            <button onClick={buscarPaises}>Carregar Países</button>
          </div>
        )}
      </main>
    </div>
  );
}

// Componente CountryCard atualizado para dados de API
function CountryCard({ pais, isFavorito, onToggleFavorito }) {
  return (
    <div className="country-card">
      <div className="country-flag">{pais.flag}</div>
      <div className="country-info">
        <h2>{pais.name.common}</h2>
        <p><strong>Capital:</strong> {pais.capital?.[0] || 'N/A'}</p>
        <p><strong>População:</strong> {pais.population.toLocaleString()}</p>
        <p><strong>Região:</strong> {pais.region}</p>
        
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

## **5. Estilos para Estados de Carregamento**

```css
/* src/App.css - Adições para loading e erro */

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 20px;
  color: #6c757d;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
  padding: 30px;
  border-radius: 10px;
  text-align: center;
  margin: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.error-message h3 {
  margin: 0 0 10px 0;
  font-size: 1.2rem;
}

.error-message p {
  margin: 10px 0 20px 0;
  opacity: 0.9;
}

.retry-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid white;
  padding: 10px 20px;
  border-radius: 25px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  background: white;
  color: #e74c3c;
}

.stats {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-top: 10px;
  font-size: 0.9rem;
  color: #7f8c8d;
}

.stats span {
  background: #f8f9fa;
  padding: 5px 12px;
  border-radius: 15px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #7f8c8d;
}

.empty-state button {
  background: #3498db;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  cursor: pointer;
  font-size: 1rem;
  margin-top: 20px;
  transition: all 0.3s ease;
}

.empty-state button:hover {
  background: #2980b9;
  transform: scale(1.05);
}
```

---

## **6. APIs Populares para Praticar**

### **🌍 REST Countries**
```
https://restcountries.com/v3.1/all
```
- Dados completos de países
- Gratuita e sem autenticação
- Perfeita para nosso projeto

### **🎬 JSONPlaceholder**
```
https://jsonplaceholder.typicode.com/posts
```
- API de testes com posts, usuários, comentários
- Ideal para aprender

### **🐱 Cat API**
```
https://api.thecatapi.com/v1/images/search
```
- Fotos aleatórias de gatos
- Divertida para testes

---

## **📝 Exercício Prático**

### 🎯 **Objetivo**
Testar diferentes APIs e implementar tratamento de erros

### 📋 **Requisitos**
- [ ] Testar a API REST Countries no navegador
- [ ] Implementar função que testa conectividade
- [ ] Adicionar botão "Atualizar Dados"
- [ ] Simular erros de rede
- [ ] Mostrar feedback visual para usuário

### 🚀 **Dica de Implementação**
```jsx
const testarAPI = async () => {
  const url = 'https://restcountries.com/v3.1/all?fields=name,capital,population';
  
  try {
    const response = await fetch(url);
    console.log('Status:', response.status);
    console.log('Headers:', response.headers);
    
    const data = await response.json();
    console.log('Primeiros 3 países:', data.slice(0, 3));
  } catch (error) {
    console.error('Erro:', error);
  }
};
```

---

## **🔮 Próximo Módulo**

No próximo módulo, aprenderemos sobre **useEffect e Ciclo de Vida**, onde implementaremos o carregamento automático de dados da API quando o componente for montado!