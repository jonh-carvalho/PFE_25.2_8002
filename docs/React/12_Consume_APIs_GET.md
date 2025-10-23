---
id: 12_Consume_APIs_GET
title: 12 - Consumindo APIs GET com React
---

# 12 - **Consumindo APIs GET com React**

Agora chegou o momento de conectar nossa **Lista de Países** com dados reais! Neste módulo, vamos evoluir nosso projeto para consumir a **API REST Countries**, aplicando todos os conceitos aprendidos: useEffect, useState, fetch, e tratamento de estados de loading e erro.

---

## **Objetivos do Módulo**
- Conectar com API real (REST Countries)
- Implementar fetch dentro de componentes React
- Dominar tratamento de estados (loading, error, success)
- Aplicar padrões profissionais de consumo de APIs
- Preparar base sólida para filtros e busca avançados

---

## **🌐 A API REST Countries**

A **REST Countries** é uma API gratuita e confiável que fornece informações completas sobre todos os países do mundo.

### **🔗 Endpoints Principais:**

```javascript
// Todos os países (dados básicos)
https://restcountries.com/v3.1/all

// Todos os países (campos específicos) - RECOMENDADO
https://restcountries.com/v3.1/all?fields=name,capital,population,region,subregion,area,flag,flags,languages,currencies,cca3

// País específico por código
https://restcountries.com/v3.1/alpha/br

// Busca por nome
https://restcountries.com/v3.1/name/brasil

// Países por região
https://restcountries.com/v3.1/region/americas
```

### **📊 Estrutura dos Dados:**

```json
{
  "name": { "common": "Brazil" },
  "capital": ["Brasília"],
  "region": "Americas",
  "subregion": "South America", 
  "population": 215353593,
  "area": 8515767,
  "flag": "🇧🇷",
  "flags": {
    "png": "https://flagcdn.com/w320/br.png",
    "svg": "https://flagcdn.com/br.svg"
  },
  "languages": { "por": "Portuguese" },
  "currencies": {
    "BRL": { "name": "Brazilian real", "symbol": "R$" }
  },
  "cca3": "BRA"
}
```

---

## **🔄 Evolução do useCountries Hook**

Vamos evoluir nosso hook personalizado para trabalhar com a API real:

```jsx
// src/hooks/useCountries.js
import { useState, useEffect } from 'react';

const REST_COUNTRIES_API = 'https://restcountries.com/v3.1/all?fields=name,capital,population,region,subregion,area,flag,flags,languages,currencies,cca3';

function useCountries() {
  const [countries, setCountries] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Função para buscar países da API
  const fetchCountries = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      console.log('🌐 Buscando países da API REST Countries...');
      
      const response = await fetch(REST_COUNTRIES_API);
      
      // Verificar se a requisição foi bem-sucedida
      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status} - ${response.statusText}`);
      }
      
      const data = await response.json();
      
      // Ordenar países por nome para melhor UX
      const sortedCountries = data.sort((a, b) => 
        a.name.common.localeCompare(b.name.common)
      );
      
      console.log(`✅ ${sortedCountries.length} países carregados com sucesso!`);
      setCountries(sortedCountries);
      
    } catch (error) {
      console.error('❌ Erro ao buscar países:', error);
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Carregar países ao montar o componente
  useEffect(() => {
    fetchCountries();
  }, []);

  // Função para recarregar dados
  const refetch = () => {
    fetchCountries();
  };

  return { 
    countries, 
    isLoading, 
    error, 
    refetch 
  };
}

export default useCountries;
```

---

## **🎯 Componente App com API Real**

```jsx
// src/App.jsx
import React, { useState, useEffect } from 'react';
import CountryCard from './components/CountryCard';
import SearchBar from './components/SearchBar';
import FilterButtons from './components/FilterButtons';
import Loading from './components/Loading';
import ErrorMessage from './components/ErrorMessage';
import useCountries from './hooks/useCountries';
import './App.css';

function App() {
  // Hook personalizado para dados da API
  const { countries, isLoading, error, refetch } = useCountries();
  
  // Estados locais para filtros e favoritos
  const [filteredCountries, setFilteredCountries] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRegion, setSelectedRegion] = useState('all');

  // Carregar favoritos do localStorage
  useEffect(() => {
    const savedFavorites = localStorage.getItem('countryFavorites');
    if (savedFavorites) {
      setFavorites(JSON.parse(savedFavorites));
    }
  }, []);

  // Salvar favoritos no localStorage
  useEffect(() => {
    localStorage.setItem('countryFavorites', JSON.stringify(favorites));
  }, [favorites]);

  // Aplicar filtros sempre que dados ou filtros mudarem
  useEffect(() => {
    let filtered = countries;

    // Filtro por região
    if (selectedRegion !== 'all') {
      filtered = filtered.filter(country => 
        country.region.toLowerCase() === selectedRegion.toLowerCase()
      );
    }

    // Filtro por busca (nome, capital, região)
    if (searchTerm.trim()) {
      const search = searchTerm.toLowerCase();
      filtered = filtered.filter(country =>
        country.name.common.toLowerCase().includes(search) ||
        country.capital?.[0]?.toLowerCase().includes(search) ||
        country.region.toLowerCase().includes(search) ||
        country.subregion?.toLowerCase().includes(search)
      );
    }

    setFilteredCountries(filtered);
  }, [countries, searchTerm, selectedRegion]);

  // Funções de controle
  const toggleFavorite = (countryCode) => {
    setFavorites(prev => 
      prev.includes(countryCode)
        ? prev.filter(code => code !== countryCode)
        : [...prev, countryCode]
    );
  };

  const handleViewDetails = (country) => {
    alert(`
🌍 ${country.name.common}
📍 Capital: ${country.capital?.[0] || 'N/A'}
👥 População: ${new Intl.NumberFormat('pt-BR').format(country.population)}
🗺️ Região: ${country.region} (${country.subregion})
📏 Área: ${new Intl.NumberFormat('pt-BR').format(country.area)} km²

💡 Em módulos futuros criaremos um modal detalhado!
    `);
  };

  const clearSearch = () => {
    setSearchTerm('');
    setSelectedRegion('all');
  };

  // Estados de carregamento e erro
  if (isLoading) {
    return <Loading message="Carregando países da API REST Countries..." />;
  }

  if (error) {
    return (
      <ErrorMessage 
        title="Erro ao Carregar Países"
        message={error}
        onRetry={refetch}
        details="Verifique sua conexão com a internet e tente novamente."
      />
    );
  }

  // Renderização principal
  return (
    <div className="app">
      <header className="app-header">
        <h1>🌍 Lista de Países</h1>
        <p className="api-status">
          ✅ Conectado à API REST Countries - {countries.length} países disponíveis
        </p>
        
        <div className="app-stats">
          <div className="stat-item">
            <span className="stat-icon">📊</span>
            <span>{filteredCountries.length} países exibidos</span>
          </div>
          <div className="stat-item">
            <span className="stat-icon">❤️</span>
            <span>{favorites.length} favoritos</span>
          </div>
          <div className="stat-item">
            <span className="stat-icon">🌐</span>
            <span>API em tempo real</span>
          </div>
        </div>
      </header>

      <div className="app-controls">
        <SearchBar 
          searchTerm={searchTerm}
          onSearchChange={setSearchTerm}
          placeholder="Buscar por país, capital ou região..."
        />
        
        <FilterButtons 
          regions={['all', 'Africa', 'Americas', 'Asia', 'Europe', 'Oceania']}
          selectedRegion={selectedRegion}
          onRegionChange={setSelectedRegion}
        />
        
        {(searchTerm || selectedRegion !== 'all') && (
          <button onClick={clearSearch} className="clear-filters-btn">
            🗑️ Limpar Filtros
          </button>
        )}
      </div>

      <main className="countries-container">
        <div className="results-header">
          <h2>Resultados da Busca</h2>
          <span className="results-count">
            {filteredCountries.length} de {countries.length} países
          </span>
        </div>
        
        {filteredCountries.length > 0 ? (
          <div className="countries-grid">
            {filteredCountries.map(country => (
              <CountryCard
                key={country.cca3}
                country={country}
                isFavorite={favorites.includes(country.cca3)}
                onToggleFavorite={toggleFavorite}
                onViewDetails={handleViewDetails}
              />
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-icon">🔍</div>
            <h3>Nenhum país encontrado</h3>
            <p>
              {searchTerm || selectedRegion !== 'all'
                ? 'Tente ajustar os filtros de busca ou região.'
                : 'Carregando dados...'}
            </p>
            {(searchTerm || selectedRegion !== 'all') && (
              <button onClick={clearSearch} className="btn-secondary">
                Limpar Filtros
              </button>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
```

---

## **🔧 Componentes de Estado: Loading e Error**

### **Loading Component:**

```jsx
// src/components/Loading.jsx
import React from 'react';

function Loading({ message = "Carregando..." }) {
  return (
    <div className="loading-container">
      <div className="loading-content">
        <div className="loading-spinner">
          <div className="spinner-circle"></div>
        </div>
        <h2>🌍 {message}</h2>
        <p>Aguarde enquanto buscamos os dados da API...</p>
        
        <div className="loading-steps">
          <div className="step active">📡 Conectando à API</div>
          <div className="step active">⬇️ Baixando dados</div>
          <div className="step active">⚡ Processando informações</div>
        </div>
      </div>
    </div>
  );
}

export default Loading;
```

### **Error Component:**

```jsx
// src/components/ErrorMessage.jsx
import React from 'react';

function ErrorMessage({ 
  title = "Ops! Algo deu errado", 
  message, 
  onRetry, 
  details 
}) {
  return (
    <div className="error-container">
      <div className="error-content">
        <div className="error-icon">❌</div>
        <h2>{title}</h2>
        <p className="error-message">{message}</p>
        {details && <p className="error-details">{details}</p>}
        
        <div className="error-actions">
          <button onClick={onRetry} className="btn-retry">
            🔄 Tentar Novamente
          </button>
          <button 
            onClick={() => window.location.reload()} 
            className="btn-reload"
          >
            ⟳ Recarregar Página
          </button>
        </div>
        
        <div className="error-tips">
          <h4>💡 Dicas para resolver:</h4>
          <ul>
            <li>Verifique sua conexão com a internet</li>
            <li>A API pode estar temporariamente indisponível</li>
            <li>Tente recarregar a página</li>
            <li>Se o problema persistir, tente mais tarde</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default ErrorMessage;
```

---

## **🎨 Estilos para Estados de Loading e Erro**

```css
/* Estados de Loading e Erro */
.loading-container, .error-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.loading-content, .error-content {
  text-align: center;
  background: white;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  max-width: 500px;
}

/* Loading Spinner */
.loading-spinner {
  margin: 20px 0;
}

.spinner-circle {
  width: 60px;
  height: 60px;
  border: 6px solid #f3f3f3;
  border-top: 6px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-steps {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 20px;
}

.step {
  padding: 8px 16px;
  background: #f8f9fa;
  border-radius: 20px;
  color: #6c757d;
  transition: all 0.3s ease;
}

.step.active {
  background: #e3f2fd;
  color: #1976d2;
}

/* Error States */
.error-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.error-message {
  font-size: 1.1rem;
  color: #e74c3c;
  font-weight: 600;
  margin: 15px 0;
}

.error-details {
  color: #7f8c8d;
  margin-bottom: 25px;
}

.error-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin: 25px 0;
}

.btn-retry, .btn-reload {
  padding: 12px 24px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-retry {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
}

.btn-reload {
  background: linear-gradient(135deg, #6c757d, #495057);
  color: white;
}

.btn-retry:hover, .btn-reload:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.error-tips {
  text-align: left;
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  margin-top: 20px;
}

.error-tips h4 {
  margin: 0 0 10px 0;
  color: #495057;
}

.error-tips ul {
  margin: 0;
  padding-left: 20px;
}

.error-tips li {
  margin: 5px 0;
  color: #6c757d;
}

/* API Status */
.api-status {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.1rem;
  margin: 10px 0;
}

.app-stats {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-top: 15px;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 16px;
  border-radius: 20px;
  color: white;
  font-size: 0.9rem;
}

.stat-icon {
  font-size: 1.1rem;
}

/* Clear Filters Button */
.clear-filters-btn {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.clear-filters-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
}

/* Results Header */
.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 10px;
}

.results-header h2 {
  color: #2c3e50;
  margin: 0;
}

.results-count {
  color: #7f8c8d;
  font-weight: 600;
}

/* Responsividade */
@media (max-width: 768px) {
  .app-stats {
    flex-direction: column;
    align-items: center;
  }
  
  .error-actions {
    flex-direction: column;
  }
  
  .results-header {
    flex-direction: column;
    gap: 10px;
    text-align: center;
  }
}
```

---

## **🔍 Otimizações e Boas Práticas**

### **1. Debounce para Busca:**

```jsx
// src/hooks/useDebounce.js
import { useState, useEffect } from 'react';

function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

export default useDebounce;
```

### **2. Cache Simples:**

```jsx
// src/services/countryAPI.js
const CACHE_KEY = 'countries_cache';
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutos

export const fetchCountriesWithCache = async () => {
  // Verificar cache
  const cached = localStorage.getItem(CACHE_KEY);
  if (cached) {
    const { data, timestamp } = JSON.parse(cached);
    if (Date.now() - timestamp < CACHE_DURATION) {
      console.log('📦 Dados carregados do cache');
      return data;
    }
  }

  // Buscar da API
  const response = await fetch(REST_COUNTRIES_API);
  if (!response.ok) {
    throw new Error(`Erro HTTP: ${response.status}`);
  }
  
  const data = await response.json();
  
  // Salvar no cache
  localStorage.setItem(CACHE_KEY, JSON.stringify({
    data,
    timestamp: Date.now()
  }));
  
  return data;
};
```

---

## **📝 Exercício Prático**

### 🎯 **Objetivo**
Implementar consumo da API REST Countries com tratamento completo de estados

### 📋 **Requisitos**
- [ ] Conectar com API REST Countries usando fetch
- [ ] Implementar estados de loading, erro e sucesso
- [ ] Adicionar tratamento de erro com retry
- [ ] Manter funcionalidade de favoritos
- [ ] Implementar busca em tempo real
- [ ] Adicionar filtro por região
- [ ] Incluir indicadores visuais de status da API

### 🚀 **Bonus**
- [ ] Implementar debounce na busca
- [ ] Adicionar cache local
- [ ] Criar modo offline
- [ ] Implementar lazy loading para imagens

---

## **🔮 Próximo Módulo**

No próximo módulo, implementaremos **filtros e busca avançados** na nossa Lista de Países, incluindo múltiplos critérios, ordenação e funcionalidades de pesquisa inteligente!

---

## **📚 Resumo do Módulo**

- ✅ **API Real**: Conexão com REST Countries  
- ✅ **Estados Robustos**: Loading, erro, sucesso
- ✅ **Tratamento de Erro**: Retry e feedback visual
- ✅ **Hook Personalizado**: Lógica reutilizável
- ✅ **UX Profissional**: Indicadores e transições
- ✅ **Base Sólida**: Preparação para módulos avançados
