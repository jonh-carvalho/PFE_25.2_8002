---
id: 10_useEffect
title: 10 - useEffect - Carregamento Automático
---

# 10 - useEffect: Carregamento Automático de Dados

Aprenda o hook mais importante para side effects no React! Vamos automatizar o carregamento de países e entender o ciclo de vida dos componentes.

---

## Objetivos do Módulo

- Automatizar o carregamento da API do IBGE usando `useEffect`
- Entender o ciclo de vida de componentes funcionais
- Gerenciar estados de loading, error e success
- Trabalhar com array de dependências do useEffect
- Mapear dados da API para o formato da aplicação

---

## 1. O Problema: Carregamento Manual

No Módulo 09, precisávamos clicar num botão para carregar os países:

```jsx
// Problema: usuário precisa clicar para ver dados
function App() {
  const [countries, setCountries] = useState([]);
  
  const loadCountries = () => {
    fetch('https://servicodados.ibge.gov.br/api/v1/paises')
      .then(r => r.json())
      .then(data => {
        const mapped = data.map(pais => ({
          cca3: pais.id['ISO-3166-1-ALPHA-3'],
          name: pais.nome.abreviado,
          // ... outros campos
        }));
        setCountries(mapped);
      });
  };

  return (
    <div>
      <button onClick={loadCountries}>Carregar Países</button>
    </div>
  );
}
```

### Queremos:

- Carregar automaticamente ao abrir a página
- Mostrar loading enquanto carrega
- Exibir mensagens de erro amigáveis
- Mapear dados da API do IBGE para o formato esperado

---

## 2. Introdução ao useEffect

### O que é useEffect?

`useEffect` é o hook que permite executar código em momentos específicos do ciclo de vida do componente.

```jsx
import { useEffect } from 'react';

useEffect(() => {
  // Este código roda depois que o componente renderiza
  console.log('Componente montado ou atualizado!');
}, [dependências]);
```

### Quando usar useEffect?

- Requisições HTTP (APIs, fetch)
- localStorage/sessionStorage
- Timers (setTimeout, setInterval)
- Event listeners (scroll, resize, teclado)
- Manipulação do DOM (document.title, focus)

---

## 3. Padrões de Dependências

### 3.1 Array Vazio - Executa UMA VEZ

```jsx
useEffect(() => {
  console.log('Executa apenas quando componente MONTA');
}, []); // Array vazio = roda 1x só
```

**Uso:** Carregar dados iniciais, configurar subscriptions

### 3.2 Com Dependências - Executa quando MUDA

```jsx
const [search, setSearch] = useState('');

useEffect(() => {
  console.log('Search mudou para:', search);
}, [search]); // Roda quando 'search' muda
```

**Uso:** Reagir a mudanças de estado/props

### 3.3 Sem Array - Executa TODA RENDER

```jsx
useEffect(() => {
  console.log('Executa em TODA render');
}); // Cuidado! Pode causar loops
```

**Uso:** Raro, geralmente evitar

---

## 4. Carregamento Automático - Versão Simples

```jsx
// src/App.jsx - Carregamento Automático
import { useEffect, useState } from 'react';
import './App.css';
import CountryGrid from './components/CountryGrid';

function App() {
  const [countries, setCountries] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // useEffect: carregar países AUTOMATICAMENTE ao montar componente
  useEffect(() => {
    console.log('useEffect executado! Carregando países...');
    
    const loadCountries = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        const response = await fetch('https://servicodados.ibge.gov.br/api/v1/paises');
        
        if (!response.ok) {
          throw new Error(`Erro HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Países carregados:', data.length);
        
        // Mapeia os dados do IBGE para o formato esperado
        const mapped = data.map(pais => ({
          cca3: pais.id['ISO-3166-1-ALPHA-3'],
          flag: `https://flagcdn.com/${pais.id['ISO-3166-1-ALPHA-2'].toLowerCase()}.svg`,
          name: pais.nome.abreviado,
          capital: pais.governo?.capital?.nome || 'N/A',
          population: 0,
          region: pais.localizacao.regiao.nome,
          subregion: pais.localizacao['sub-regiao']?.nome || 'N/A'
        }));
        
        setCountries(mapped);
        console.log('✅ Países mapeados:', mapped.length, 'países');
        
      } catch (err) {
        console.error('Erro:', err);
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    loadCountries();
  }, []); // Array vazio = executa apenas UMA VEZ na montagem

  const toggleFavorite = (countryCode) => {
    setFavorites(prev => 
      prev.includes(countryCode)
        ? prev.filter(code => code !== countryCode)
        : [...prev, countryCode]
    );
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Lista de Países do Mundo</h1>
        <p>Carregamento automático com useEffect</p>
        
        {/* Debug: sempre mostrar para testar */}
        <div className="header-stats">
          <span>{countries.length} países</span>
          <span>{favorites.length} favoritos</span>
        </div>
      </header>

      <main className="main-content">
        {/* Loading State */}
        {isLoading && (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <h2>Carregando países...</h2>
            <p>Buscando dados da API do IBGE</p>
          </div>
        )}
        
        {/* Error State */}
        {error && (
          <div className="error-container">
            <div className="error-icon">❌</div>
            <h2>Ops! Algo deu errado</h2>
            <p className="error-message">{error}</p>
            <button onClick={() => window.location.reload()} className="retry-btn">
              Tentar Novamente
            </button>
          </div>
        )}
        
        {/* Success State */}
        {!isLoading && !error && (
          <CountryGrid 
            countries={countries}
            favorites={favorites}
            onToggleFavorite={toggleFavorite}
          />
        )}
      </main>
    </div>
  );
}

export default App;
```

### O que mudou?

| Antes (Módulo 09) | Agora (Módulo 10) |
|-------------------|-------------------|
| Botão "Carregar Países" | Carrega automaticamente |
| onClick={loadCountries} | useEffect(() => {...}, []) |
| Usuário inicia ação | Componente inicia ação |
| Sem loading/error states | Loading e error com JSX inline |

---

## 5. Entendendo o Código

### 5.1 Estados de Controle

```jsx
const [isLoading, setIsLoading] = useState(true);
const [error, setError] = useState(null);
```

**Por que iniciar com `true`?**
- Quando o componente monta, já começamos carregando
- Evita piscar de conteúdo vazio

**Estados possíveis:**
1. ⏳ Loading: `isLoading=true, error=null` → Mostra spinner
2. ❌ Error: `isLoading=false, error="mensagem"` → Mostra erro
3. ✅ Success: `isLoading=false, error=null` → Mostra países

### 5.2 Mapeamento de Dados do IBGE

A API do IBGE retorna dados em formato diferente do esperado:

```jsx
// Formato do IBGE (nested):
{
  "id": {
    "ISO-3166-1-ALPHA-3": "BRA",
    "ISO-3166-1-ALPHA-2": "BR"
  },
  "nome": {
    "abreviado": "Brasil"
  },
  "governo": {
    "capital": {
      "nome": "Brasília"
    }
  },
  "localizacao": {
    "regiao": {
      "nome": "Americas"
    },
    "sub-regiao": {
      "nome": "South America"
    }
  }
}

// Formato da aplicação (flat):
{
  cca3: "BRA",
  flag: "https://flagcdn.com/br.svg",
  name: "Brasil",
  capital: "Brasília",
  population: 0,
  region: "Americas",
  subregion: "South America"
}
```

**Mapeamento com `.map()`:**

```jsx
const mapped = data.map(pais => ({
  cca3: pais.id['ISO-3166-1-ALPHA-3'],
  flag: `https://flagcdn.com/${pais.id['ISO-3166-1-ALPHA-2'].toLowerCase()}.svg`,
  name: pais.nome.abreviado,
  capital: pais.governo?.capital?.nome || 'N/A',
  population: 0, // IBGE não fornece
  region: pais.localizacao.regiao.nome,
  subregion: pais.localizacao['sub-regiao']?.nome || 'N/A'
}));
```

### 5.3 Renderização Condicional (3 Estados)

```jsx
return (
  <main>
    {/* Estado 1: Loading */}
    {isLoading && (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <h2>Carregando países...</h2>
        <p>Buscando dados da API do IBGE</p>
      </div>
    )}
    
    {/* Estado 2: Error */}
    {error && (
      <div className="error-container">
        <div className="error-icon">❌</div>
        <h2>Ops! Algo deu errado</h2>
        <p className="error-message">{error}</p>
        <button onClick={() => window.location.reload()}>
          Tentar Novamente
        </button>
      </div>
    )}
    
    {/* Estado 3: Success */}
    {!isLoading && !error && (
      <CountryGrid 
        countries={countries}
        favorites={favorites}
        onToggleFavorite={toggleFavorite}
      />
    )}
  </main>
);
```

**Lógica:**
- Se `isLoading=true` → Mostra loading
- Se `error` existe → Mostra erro
- Se nenhum dos dois → Mostra grid de países

---

## 6. Estilos para Loading e Error

Adicione ao `App.css`:

```css
/* Loading State */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
}

.loading-spinner {
  width: 60px;
  height: 60px;
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

.loading-container h2 {
  color: #333;
  margin-bottom: 10px;
}

.loading-container p {
  color: #777;
  font-size: 0.95rem;
}

/* Error State */
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
  padding: 20px;
}

.error-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.error-container h2 {
  color: #e74c3c;
  margin-bottom: 10px;
}

.error-message {
  background: #ffe6e6;
  color: #c0392b;
  padding: 15px 25px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-family: monospace;
}

.retry-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  background: #2980b9;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
```

---

## 7. Testando o Comportamento

### 7.1 Testar Loading

1. Abra DevTools (F12) → Network
2. Selecione "Slow 3G" para simular internet lenta
3. Recarregue a página (F5)
4. Observe o spinner e mensagem de loading

### 7.2 Testar Error

**Opção 1: URL inválida**

```jsx
const response = await fetch('https://url-invalida.com/api');
```

**Opção 2: DevTools Offline**

1. F12 → Network
2. Selecione "Offline"
3. Recarregue a página
4. Deve aparecer mensagem de erro

### 7.3 Testar Success

1. Volte para "No throttling" no Network
2. Recarregue
3. Países devem aparecer normalmente

---

## 8. Exercícios Práticos

### Exercício 1: Adicionar Contador de Tempo

Mostre quanto tempo levou para carregar:

```jsx
useEffect(() => {
  const startTime = Date.now();
  
  const loadCountries = async () => {
    try {
      // ... código de loading
      
      const endTime = Date.now();
      const duration = ((endTime - startTime) / 1000).toFixed(2);
      console.log(`Carregou em ${duration} segundos`);
      
    } catch (err) {
      // ...
    }
  };
  
  loadCountries();
}, []);
```

### Exercício 2: Botão de Recarregar Avançado

Em vez de `window.location.reload()`, reexecute o fetch:

```jsx
const [refreshKey, setRefreshKey] = useState(0);

useEffect(() => {
  const loadCountries = async () => {
    // ... código de loading
  };
  
  loadCountries();
}, [refreshKey]); // Reexecuta quando refreshKey muda

// No botão:
<button onClick={() => setRefreshKey(prev => prev + 1)}>
  Tentar Novamente
</button>
```

### Exercício 3: Mensagens de Error Personalizadas

```jsx
const getErrorMessage = (error) => {
  if (error.message.includes('Failed to fetch')) {
    return 'Sem conexão com a internet. Verifique sua rede.';
  }
  if (error.message.includes('404')) {
    return 'API não encontrada. Verifique a URL.';
  }
  if (error.message.includes('500')) {
    return 'Erro no servidor. Tente novamente mais tarde.';
  }
  return error.message;
};

// No catch:
setError(getErrorMessage(err));
```

### Exercício 4: Mostrar Progresso

Adicione um texto mostrando progresso durante o carregamento:

```jsx
const [loadingProgress, setLoadingProgress] = useState('Iniciando...');

const loadCountries = async () => {
  try {
    setLoadingProgress('Conectando à API...');
    const response = await fetch('...');
    
    setLoadingProgress('Recebendo dados...');
    const data = await response.json();
    
    setLoadingProgress('Mapeando países...');
    const mapped = data.map(...);
    
    setLoadingProgress('Finalizando...');
    setCountries(mapped);
    
  } catch (err) {
    // ...
  }
};

// No JSX:
<p>{loadingProgress}</p>
```

---

## 9. Resumo do Módulo

### O que aprendemos?

✅ `useEffect` executa código após renderização  
✅ Array de dependências `[]` faz executar 1x só  
✅ Try-catch-finally gerencia loading/error/success  
✅ Renderização condicional com 3 estados  
✅ Mapeamento de dados de APIs externas  
✅ Estados inline são mais simples que componentes separados  

### Padrão Completo:

```jsx
function Component() {
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const res = await fetch('url');
        const json = await res.json();
        setData(json);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    
    loadData();
  }, []);
  
  if (isLoading) return <Loading />;
  if (error) return <Error message={error} />;
  return <Data items={data} />;
}
```

---

## 10. Próximos Passos

No **Módulo 11**, vamos aprender:

- Filtros e busca de países
- useEffect com dependências (reagir a mudanças)
- Debouncing de inputs
- Múltiplos filtros simultâneos

Continue praticando! 🚀
