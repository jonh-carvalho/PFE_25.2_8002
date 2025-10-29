---
id: 10_useEffect
title: 10 - useEffect e Ciclo de Vida
---

# 10 - **useEffect e Ciclo de Vida**

Neste módulo, você aprenderá o hook `useEffect`, essencial para gerenciar efeitos colaterais e o ciclo de vida de componentes React. Implementaremos o carregamento automático de dados na nossa **Lista de Países** conectando com APIs.

---

## **Objetivos do Módulo**
- Dominar o hook `useEffect` e suas dependências
- Entender o ciclo de vida de componentes funcionais
- Implementar carregamento automático de dados
- Conectar nossa Lista de Países com APIs reais
- Gerenciar cleanup e memory leaks

---

## **1. Introdução ao useEffect**

### **O que é useEffect?**

O `useEffect` é um hook que permite executar **efeitos colaterais** em componentes funcionais. Efeitos colaterais são operações que afetam algo fora do componente:

- 🌐 **Chamadas de API**
- ⏰ **Timers e intervalos**
- 🎧 **Event listeners**
- 📄 **Manipulação do DOM**
- 🧹 **Cleanup de recursos**

### **Sintaxe Básica**

```jsx
import { useEffect } from 'react';

useEffect(() => {
  // Código do efeito
}, [dependências]);
```

### **Anatomia do useEffect**

```jsx
useEffect(
  () => {
    // 1. Código que executa
    console.log('Efeito executado!');
    
    // 2. Cleanup (opcional)
    return () => {
      console.log('Cleanup executado!');
    };
  },
  [dependência1, dependência2] // 3. Array de dependências
);
```

---

## **2. Padrões de Dependências**

### **2.1 Sem Array de Dependências**

```jsx
useEffect(() => {
  console.log('Executa a cada render!');
});
// ⚠️ Cuidado: pode causar loops infinitos
```

### **2.2 Array Vazio `[]`**

```jsx
useEffect(() => {
  console.log('Executa apenas uma vez (componentDidMount)');
}, []);
// ✅ Ideal para: carregar dados iniciais, configurar listeners
```

### **2.3 Com Dependências Específicas**

```jsx
const [count, setCount] = useState(0);

useEffect(() => {
  console.log(`Count mudou para: ${count}`);
}, [count]);
// ✅ Executa apenas quando 'count' muda
```

### **2.4 Múltiplas Dependências**

```jsx
const [name, setName] = useState('');
const [age, setAge] = useState(0);

useEffect(() => {
  console.log(`Dados atualizados: ${name}, ${age}`);
}, [name, age]);
// ✅ Executa quando 'name' OU 'age' mudam
```

---

## **3. Ciclo de Vida com useEffect**

### **Comparação com Class Components**

| Class Component | Functional Component |
|-----------------|---------------------|
| `componentDidMount` | `useEffect(() => {}, [])` |
| `componentDidUpdate` | `useEffect(() => {}, [dep])` |
| `componentWillUnmount` | `useEffect(() => { return () => {} }, [])` |

### **Exemplo Prático: Timer**

```jsx
import React, { useState, useEffect } from 'react';

function Timer() {
  const [seconds, setSeconds] = useState(0);
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    let interval = null;

    if (isRunning) {
      // Configurar timer
      interval = setInterval(() => {
        setSeconds(prevSeconds => prevSeconds + 1);
      }, 1000);
    }

    // Cleanup function
    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [isRunning]); // Reexecuta quando isRunning muda

  return (
    <div>
      <h2>Timer: {seconds}s</h2>
      <button onClick={() => setIsRunning(!isRunning)}>
        {isRunning ? 'Pausar' : 'Iniciar'}
      </button>
      <button onClick={() => setSeconds(0)}>Reset</button>
    </div>
  );
}
```

---

## **4. useEffect com APIs - Evoluindo a Lista de Países**

Vamos conectar nossa Lista de Países com a API REST Countries usando useEffect:

### **4.1 Carregamento Inicial de Dados**

```jsx
// src/App.jsx
import React, { useState, useEffect } from 'react';
import Loading from './components/Loading';
import ErrorMessage from './components/ErrorMessage';

function App() {
  const [paises, setPaises] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);
  const [favoritos, setFavoritos] = useState([]);

  // useEffect para carregar dados iniciais
  useEffect(() => {
    const carregarPaises = async () => {
      try {
        setCarregando(true);
        setErro(null);

        const response = await fetch('https://restcountries.com/v3.1/all?fields=name,capital,population,region,flag,cca3');
        
        if (!response.ok) {
          throw new Error(`Erro HTTP: ${response.status}`);
        }

        const data = await response.json();
        
        // Limitar a 20 países para performance
        const paisesLimitados = data.slice(0, 20);
        setPaises(paisesLimitados);

      } catch (error) {
        setErro(error.message);
      } finally {
        setCarregando(false);
      }
    };

    carregarPaises();
  }, []); // Array vazio = executa apenas uma vez

  // useEffect para salvar favoritos no localStorage
  useEffect(() => {
    localStorage.setItem('favoritos', JSON.stringify(favoritos));
  }, [favoritos]); // Executa quando favoritos mudam

  // useEffect para carregar favoritos do localStorage
  useEffect(() => {
    const favoritosSalvos = localStorage.getItem('favoritos');
    if (favoritosSalvos) {
      setFavoritos(JSON.parse(favoritosSalvos));
    }
  }, []); // Executa apenas uma vez

  const toggleFavorito = (paisCodigo) => {
    setFavoritos(prev => 
      prev.includes(paisCodigo)
        ? prev.filter(codigo => codigo !== paisCodigo)
        : [...prev, paisCodigo]
    );
  };

  const recarregarDados = () => {
    // Força recarregamento mudando uma dependência
    window.location.reload();
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🌍 Lista de Países</h1>
        <p>Dados carregados automaticamente via useEffect</p>
        
        {paises.length > 0 && (
          <div className="stats">
            <span>📊 {paises.length} países</span>
            <span>❤️ {favoritos.length} favoritos</span>
            <button onClick={recarregarDados} className="reload-btn">
              🔄 Recarregar
            </button>
          </div>
        )}
      </header>

      <main className="main-content">
        {carregando && <Loading />}
        
        {erro && (
          <ErrorMessage 
            mensagem={erro} 
            onTentar={recarregarDados}
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
      </main>
    </div>
  );
}

export default App;
```

### **4.2 Hook Customizado para API**

```jsx
// src/hooks/usePaises.js
import { useState, useEffect } from 'react';

function usePaises() {
  const [paises, setPaises] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    let cancelado = false; // Flag para evitar memory leaks

    const buscarPaises = async () => {
      try {
        setCarregando(true);
        setErro(null);

        const response = await fetch('https://restcountries.com/v3.1/all?fields=name,capital,population,region,flag,cca3');
        
        if (!response.ok) {
          throw new Error(`Erro: ${response.status}`);
        }

        const data = await response.json();

        // Verificar se o componente ainda está montado
        if (!cancelado) {
          setPaises(data.slice(0, 20));
        }

      } catch (error) {
        if (!cancelado) {
          setErro(error.message);
        }
      } finally {
        if (!cancelado) {
          setCarregando(false);
        }
      }
    };

    buscarPaises();

    // Cleanup: cancelar operação se componente for desmontado
    return () => {
      cancelado = true;
    };
  }, []);

  return { paises, carregando, erro };
}

export default usePaises;
```

### **4.3 Usando o Hook Customizado**

```jsx
// src/App.jsx (versão simplificada)
import React, { useState, useEffect } from 'react';
import usePaises from './hooks/usePaises';

function App() {
  const { paises, carregando, erro } = usePaises();
  const [favoritos, setFavoritos] = useState([]);

  // Carregar favoritos do localStorage
  useEffect(() => {
    const favoritosSalvos = localStorage.getItem('favoritos');
    if (favoritosSalvos) {
      setFavoritos(JSON.parse(favoritosSalvos));
    }
  }, []);

  // Salvar favoritos no localStorage
  useEffect(() => {
    localStorage.setItem('favoritos', JSON.stringify(favoritos));
  }, [favoritos]);

  // ... resto do componente
}
```

---

## **5. Padrões Avançados com useEffect**

### **5.1 Debounce com useEffect**

```jsx
function SearchCountries() {
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (searchTerm) {
        // Buscar países depois de 500ms de pausa na digitação
        fetch(`https://restcountries.com/v3.1/name/${searchTerm}`)
          .then(response => response.json())
          .then(setResults);
      }
    }, 500);

    // Cleanup: cancelar timeout anterior
    return () => clearTimeout(timeoutId);
  }, [searchTerm]);

  return (
    <div>
      <input 
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Buscar país..."
      />
      {/* Renderizar results */}
    </div>
  );
}
```

### **5.2 Event Listeners**

```jsx
function WindowSize() {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });

  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight
      });
    };

    // Adicionar listener
    window.addEventListener('resize', handleResize);

    // Cleanup: remover listener
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []); // Array vazio = adiciona listener apenas uma vez

  return <p>Janela: {windowSize.width} x {windowSize.height}</p>;
}
```

---

## **6. Boas Práticas e Armadilhas**

### **✅ Boas Práticas**

1. **Sempre inclua dependências necessárias**
   ```jsx
   useEffect(() => {
     fetchData(userId);
   }, [userId]); // ✅ Inclui userId
   ```

2. **Use cleanup para evitar memory leaks**
   ```jsx
   useEffect(() => {
     const interval = setInterval(callback, 1000);
     return () => clearInterval(interval); // ✅ Cleanup
   }, []);
   ```

3. **Separe efeitos por responsabilidade**
   ```jsx
   // ✅ Um useEffect para cada responsabilidade
   useEffect(() => { /* carregar dados */ }, []);
   useEffect(() => { /* salvar no localStorage */ }, [data]);
   ```

### **❌ Armadilhas Comuns**

1. **Loops infinitos**
   ```jsx
   // ❌ Cria loop infinito
   useEffect(() => {
     setCount(count + 1);
   }); // Sem array de dependências
   ```

2. **Dependências faltando**
   ```jsx
   // ❌ useEffect depende de 'name' mas não está nas dependências
   useEffect(() => {
     fetchUserData(name);
   }, []); // Deveria ser [name]
   ```

3. **Cleanup inadequado**
   ```jsx
   // ❌ Não remove event listener
   useEffect(() => {
     window.addEventListener('scroll', handleScroll);
     // Faltou: return () => window.removeEventListener('scroll', handleScroll);
   }, []);
   ```

---

## **📝 Exercício Prático**

### 🎯 **Objetivo**
Implementar busca em tempo real na Lista de Países com debounce

### 📋 **Requisitos**
- [ ] Adicionar campo de busca que filtra países por nome
- [ ] Implementar debounce de 300ms para evitar muitas requisições
- [ ] Mostrar loading durante a busca
- [ ] Exibir mensagem quando nenhum país for encontrado
- [ ] Limpar busca com botão "X"

### 🚀 **Dica de Implementação**
```jsx
const [searchTerm, setSearchTerm] = useState('');
const [searchResults, setSearchResults] = useState([]);

useEffect(() => {
  const timeoutId = setTimeout(async () => {
    if (searchTerm.trim()) {
      try {
        const response = await fetch(`https://restcountries.com/v3.1/name/${searchTerm}`);
        const data = await response.json();
        setSearchResults(data);
      } catch (error) {
        setSearchResults([]);
      }
    } else {
      setSearchResults([]);
    }
  }, 300);

  return () => clearTimeout(timeoutId);
}, [searchTerm]);
```

---

## **🔮 Próximo Módulo**

No próximo módulo, criaremos um **Projeto Prático Completo** integrando todos os conceitos aprendidos: componentes, estado, efeitos e APIs para construir uma aplicação robusta!

---

## **📚 Resumo do Módulo**

- ✅ **useEffect**: Hook essencial para efeitos colaterais
- ✅ **Dependências**: Controlam quando o efeito executa
- ✅ **Cleanup**: Previne memory leaks e bugs
- ✅ **APIs**: Carregamento automático de dados
- ✅ **Hooks Customizados**: Reutilização de lógica
- ✅ **Boas Práticas**: Padrões para código limpo e performático  
  
