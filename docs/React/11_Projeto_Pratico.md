---
id: 11_Projeto_Pratico
title: 11 - Projeto Prático: Lista de Países Completa
---

# 11 - **Projeto Prático: Lista de Países Completa**

Neste módulo, construiremos um projeto prático completo que evolui de dados estáticos para o consumo de APIs reais. Nossa **Lista de Países** passará por três estágios: dados locais → arquivo JSON → API externa, demonstrando diferentes abordagens para carregar dados em React.

---

## **Objetivos do Módulo**
- Implementar um projeto prático evolutivo
- Dominar diferentes fontes de dados (local, JSON, API)
- Aplicar todos os conceitos aprendidos (componentes, estado, useEffect)
- Preparar base sólida para consumo de APIs reais
- Criar uma aplicação robusta com tratamento de erros

---

## **🎯 Projeto: Lista de Países - Evolução Completa**

### **Fase 1: Dados Locais (Hardcoded)**
Começamos com dados estáticos para focar na estrutura de componentes.

### **Fase 2: Arquivo JSON Local**
Evoluímos para dados em arquivo JSON para simular uma fonte externa.

### **Fase 3: API Fake (JSON Server)**
Implementamos servidor fake para simular API real com loading e erros.

### **Fase 4: API Real (REST Countries)**
Conectamos com API real do mundo, aplicando todos os conceitos.

---

## **📁 Estrutura do Projeto**

```
src/
├── components/
│   ├── CountryCard.jsx
│   ├── CountryGrid.jsx
│   ├── SearchBar.jsx
│   ├── FilterButtons.jsx
│   ├── Loading.jsx
│   └── ErrorMessage.jsx
├── data/
│   └── countries.json
├── hooks/
│   └── useCountries.js
├── services/
│   └── countryAPI.js
└── App.jsx
```

---

## **🏗️ Fase 1: Dados Locais**

### **1.1 Estrutura Base de Dados**

```jsx
// src/data/countriesData.js
export const countriesData = [
  {
    cca3: "BRA",
    name: { common: "Brazil" },
    capital: ["Brasília"],
    region: "Americas",
    subregion: "South America",
    population: 215353593,
    area: 8515767,
    flag: "🇧🇷",
    flags: {
      png: "https://flagcdn.com/w320/br.png",
      svg: "https://flagcdn.com/br.svg"
    },
    languages: { por: "Portuguese" },
    currencies: {
      BRL: { name: "Brazilian real", symbol: "R$" }
    },
    timezones: ["UTC-05:00", "UTC-04:00", "UTC-03:00", "UTC-02:00"]
  },
  {
    cca3: "FRA",
    name: { common: "France" },
    capital: ["Paris"],
    region: "Europe",
    subregion: "Western Europe",
    population: 67391582,
    area: 551695,
    flag: "🇫🇷",
    flags: {
      png: "https://flagcdn.com/w320/fr.png",
      svg: "https://flagcdn.com/fr.svg"
    },
    languages: { fra: "French" },
    currencies: {
      EUR: { name: "Euro", symbol: "€" }
    },
    timezones: ["UTC+01:00"]
  },
  {
    cca3: "JPN",
    name: { common: "Japan" },
    capital: ["Tokyo"],
    region: "Asia",
    subregion: "Eastern Asia",
    population: 125836021,
    area: 377930,
    flag: "🇯🇵",
    flags: {
      png: "https://flagcdn.com/w320/jp.png",
      svg: "https://flagcdn.com/jp.svg"
    },
    languages: { jpn: "Japanese" },
    currencies: {
      JPY: { name: "Japanese yen", symbol: "¥" }
    },
    timezones: ["UTC+09:00"]
  },
  {
    cca3: "AUS",
    name: { common: "Australia" },
    capital: ["Canberra"],
    region: "Oceania",
    subregion: "Australia and New Zealand",
    population: 25687041,
    area: 7692024,
    flag: "🇦🇺",
    flags: {
      png: "https://flagcdn.com/w320/au.png",
      svg: "https://flagcdn.com/au.svg"
    },
    languages: { eng: "English" },
    currencies: {
      AUD: { name: "Australian dollar", symbol: "$" }
    },
    timezones: ["UTC+05:00", "UTC+06:30", "UTC+07:00", "UTC+08:00", "UTC+09:30", "UTC+10:00", "UTC+10:30", "UTC+11:00"]
  }
];
```

### **1.2 Componente CountryCard Completo**

```jsx
// src/components/CountryCard.jsx
import React from 'react';

function CountryCard({ country, isFavorite, onToggleFavorite, onViewDetails }) {
  const formatPopulation = (pop) => {
    return new Intl.NumberFormat('pt-BR').format(pop);
  };

  const formatArea = (area) => {
    return new Intl.NumberFormat('pt-BR').format(area);
  };

  const getLanguages = (languages) => {
    return Object.values(languages || {}).join(', ') || 'N/A';
  };

  const getCurrency = (currencies) => {
    if (!currencies) return 'N/A';
    const currency = Object.values(currencies)[0];
    return `${currency.name} (${currency.symbol})`;
  };

  return (
    <div className="country-card">
      <div className="country-header">
        <img 
          src={country.flags.png} 
          alt={`Bandeira de ${country.name.common}`}
          className="country-flag-img"
        />
        <div className="country-flag-emoji">{country.flag}</div>
      </div>
      
      <div className="country-info">
        <h2 className="country-name">{country.name.common}</h2>
        
        <div className="country-details">
          <div className="detail-row">
            <span className="label">Capital:</span>
            <span className="value">{country.capital?.[0] || 'N/A'}</span>
          </div>
          
          <div className="detail-row">
            <span className="label">Região:</span>
            <span className="value">{country.region}</span>
          </div>
          
          <div className="detail-row">
            <span className="label">Sub-região:</span>
            <span className="value">{country.subregion}</span>
          </div>
          
          <div className="detail-row">
            <span className="label">População:</span>
            <span className="value">{formatPopulation(country.population)}</span>
          </div>
          
          <div className="detail-row">
            <span className="label">Área:</span>
            <span className="value">{formatArea(country.area)} km²</span>
          </div>
          
          <div className="detail-row">
            <span className="label">Idiomas:</span>
            <span className="value">{getLanguages(country.languages)}</span>
          </div>
          
          <div className="detail-row">
            <span className="label">Moeda:</span>
            <span className="value">{getCurrency(country.currencies)}</span>
          </div>
        </div>
        
        <div className="country-actions">
          <button 
            className={`favorite-btn ${isFavorite ? 'favorited' : ''}`}
            onClick={() => onToggleFavorite(country.cca3)}
            title={isFavorite ? 'Remover dos favoritos' : 'Adicionar aos favoritos'}
          >
            {isFavorite ? '❤️' : '🤍'} 
            {isFavorite ? 'Favorito' : 'Favoritar'}
          </button>
          
          <button 
            className="details-btn"
            onClick={() => onViewDetails(country)}
            title="Ver detalhes completos"
          >
            📋 Detalhes
          </button>
        </div>
      </div>
    </div>
  );
}

export default CountryCard;
```

### **1.3 App Principal - Fase 1**

```jsx
// src/App.jsx - Fase 1: Dados Locais
import React, { useState, useEffect } from 'react';
import CountryCard from './components/CountryCard';
import SearchBar from './components/SearchBar';
import FilterButtons from './components/FilterButtons';
import { countriesData } from './data/countriesData';
import './App.css';

function App() {
  const [countries, setCountries] = useState([]);
  const [filteredCountries, setFilteredCountries] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRegion, setSelectedRegion] = useState('all');
  const [isLoading, setIsLoading] = useState(true);

  // Simular carregamento inicial
  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true);
      // Simular delay de rede
      await new Promise(resolve => setTimeout(resolve, 1000));
      setCountries(countriesData);
      setFilteredCountries(countriesData);
      setIsLoading(false);
    };

    loadData();
  }, []);

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

  // Filtrar países por busca e região
  useEffect(() => {
    let filtered = countries;

    // Filtro por região
    if (selectedRegion !== 'all') {
      filtered = filtered.filter(country => 
        country.region.toLowerCase() === selectedRegion.toLowerCase()
      );
    }

    // Filtro por busca
    if (searchTerm) {
      filtered = filtered.filter(country =>
        country.name.common.toLowerCase().includes(searchTerm.toLowerCase()) ||
        country.capital?.[0]?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        country.region.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFilteredCountries(filtered);
  }, [countries, searchTerm, selectedRegion]);

  const toggleFavorite = (countryCode) => {
    setFavorites(prev => 
      prev.includes(countryCode)
        ? prev.filter(code => code !== countryCode)
        : [...prev, countryCode]
    );
  };

  const handleViewDetails = (country) => {
    alert(`Detalhes completos de ${country.name.common} serão implementados em módulos futuros!`);
  };

  const regions = ['all', 'Africa', 'Americas', 'Asia', 'Europe', 'Oceania'];

  if (isLoading) {
    return (
      <div className="app">
        <div className="loading">
          <div className="loading-spinner"></div>
          <p>Carregando países...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🌍 Lista de Países</h1>
        <p>Fase 1: Dados Locais - {countries.length} países carregados</p>
        
        <div className="app-stats">
          <span>📊 {filteredCountries.length} países exibidos</span>
          <span>❤️ {favorites.length} favoritos</span>
        </div>
      </header>

      <div className="app-controls">
        <SearchBar 
          searchTerm={searchTerm}
          onSearchChange={setSearchTerm}
          placeholder="Buscar por país, capital ou região..."
        />
        
        <FilterButtons 
          regions={regions}
          selectedRegion={selectedRegion}
          onRegionChange={setSelectedRegion}
        />
      </div>

      <main className="countries-container">
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
            <h3>🔍 Nenhum país encontrado</h3>
            <p>Tente ajustar os filtros de busca ou região.</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
```

---

## **🗂️ Fase 2: Arquivo JSON Local**

### **2.1 Criando Dados em JSON**

```json
// public/countries-data.json
[
  {
    "cca3": "BRA",
    "name": { "common": "Brazil" },
    "capital": ["Brasília"],
    "region": "Americas",
    "subregion": "South America",
    "population": 215353593,
    "area": 8515767,
    "flag": "🇧🇷",
    "flags": {
      "png": "https://flagcdn.com/w320/br.png"
    },
    "languages": { "por": "Portuguese" },
    "currencies": {
      "BRL": { "name": "Brazilian real", "symbol": "R$" }
    }
  },
  {
    "cca3": "FRA",
    "name": { "common": "France" },
    "capital": ["Paris"],
    "region": "Europe",
    "subregion": "Western Europe",
    "population": 67391582,
    "area": 551695,
    "flag": "🇫🇷",
    "flags": {
      "png": "https://flagcdn.com/w320/fr.png"
    },
    "languages": { "fra": "French" },
    "currencies": {
      "EUR": { "name": "Euro", "symbol": "€" }
    }
  }
]
```

### **2.2 Hook Personalizado para Dados**

```jsx
// src/hooks/useCountries.js
import { useState, useEffect } from 'react';

function useCountries(source = 'local') {
  const [countries, setCountries] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCountries = async () => {
      setIsLoading(true);
      setError(null);

      try {
        let data;
        
        switch (source) {
          case 'json':
            // Buscar do arquivo JSON local
            const response = await fetch('/countries-data.json');
            if (!response.ok) {
              throw new Error(`Erro HTTP: ${response.status}`);
            }
            data = await response.json();
            break;
            
          case 'api':
            // Buscar de API real (implementado na Fase 4)
            const apiResponse = await fetch('https://restcountries.com/v3.1/all?fields=name,capital,population,region,subregion,area,flag,flags,languages,currencies,cca3');
            if (!apiResponse.ok) {
              throw new Error(`Erro na API: ${apiResponse.status}`);
            }
            data = await apiResponse.json();
            break;
            
          default:
            // Dados locais (hardcoded)
            const { countriesData } = await import('../data/countriesData.js');
            data = countriesData;
        }

        // Simular delay para demonstração
        await new Promise(resolve => setTimeout(resolve, 800));
        
        setCountries(data);
      } catch (err) {
        setError(err.message);
        console.error('Erro ao carregar países:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchCountries();
  }, [source]);

  return { countries, isLoading, error };
}

export default useCountries;
```

### **2.3 App Atualizado - Fase 2**

```jsx
// src/App.jsx - Fase 2: JSON Local
import React, { useState, useEffect } from 'react';
import CountryCard from './components/CountryCard';
import useCountries from './hooks/useCountries';
import './App.css';

function App() {
  const [dataSource, setDataSource] = useState('local'); // 'local', 'json', 'api'
  const { countries, isLoading, error } = useCountries(dataSource);
  const [filteredCountries, setFilteredCountries] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRegion, setSelectedRegion] = useState('all');

  // Atualizar países filtrados quando dados mudarem
  useEffect(() => {
    setFilteredCountries(countries);
  }, [countries]);

  // Aplicar filtros
  useEffect(() => {
    let filtered = countries;

    if (selectedRegion !== 'all') {
      filtered = filtered.filter(country => 
        country.region.toLowerCase() === selectedRegion.toLowerCase()
      );
    }

    if (searchTerm) {
      filtered = filtered.filter(country =>
        country.name.common.toLowerCase().includes(searchTerm.toLowerCase()) ||
        country.capital?.[0]?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFilteredCountries(filtered);
  }, [countries, searchTerm, selectedRegion]);

  const getSourceLabel = () => {
    const labels = {
      'local': 'Dados Locais (Hardcoded)',
      'json': 'Arquivo JSON Local',
      'api': 'API REST Countries'
    };
    return labels[dataSource];
  };

  if (isLoading) {
    return (
      <div className="app">
        <div className="loading">
          <div className="loading-spinner"></div>
          <p>Carregando dados de: {getSourceLabel()}</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app">
        <div className="error-message">
          <h3>❌ Erro ao carregar dados</h3>
          <p>{error}</p>
          <button onClick={() => window.location.reload()}>
            🔄 Tentar Novamente
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🌍 Lista de Países - Evolução de Dados</h1>
        
        <div className="data-source-selector">
          <label>Fonte dos Dados:</label>
          <select 
            value={dataSource} 
            onChange={(e) => setDataSource(e.target.value)}
            className="source-select"
          >
            <option value="local">📝 Dados Locais</option>
            <option value="json">📄 Arquivo JSON</option>
            <option value="api">🌐 API REST Countries</option>
          </select>
        </div>
        
        <p>Fonte atual: {getSourceLabel()} - {countries.length} países</p>
      </header>

      <div className="app-controls">
        <input
          type="text"
          placeholder="Buscar países..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
        
        <select
          value={selectedRegion}
          onChange={(e) => setSelectedRegion(e.target.value)}
          className="region-select"
        >
          <option value="all">Todas as regiões</option>
          <option value="africa">África</option>
          <option value="americas">Américas</option>
          <option value="asia">Ásia</option>
          <option value="europe">Europa</option>
          <option value="oceania">Oceania</option>
        </select>
      </div>

      <main className="countries-container">
        <div className="results-info">
          <span>📊 Exibindo {filteredCountries.length} de {countries.length} países</span>
        </div>
        
        {filteredCountries.length > 0 ? (
          <div className="countries-grid">
            {filteredCountries.map(country => (
              <CountryCard
                key={country.cca3}
                country={country}
                isFavorite={favorites.includes(country.cca3)}
                onToggleFavorite={() => {
                  setFavorites(prev => 
                    prev.includes(country.cca3)
                      ? prev.filter(code => code !== country.cca3)
                      : [...prev, country.cca3]
                  );
                }}
                onViewDetails={(country) => {
                  console.log('Detalhes do país:', country);
                }}
              />
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <h3>🔍 Nenhum país encontrado</h3>
            <p>Tente ajustar os filtros de busca.</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
```

---

## **🎨 Estilos Completos**

```css
/* src/App.css */
.app {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.app-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 15px;
  color: white;
}

.app-header h1 {
  font-size: 2.5rem;
  margin: 0 0 20px 0;
}

.data-source-selector {
  margin: 15px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.source-select {
  padding: 8px 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 1rem;
}

.app-controls {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  flex-wrap: wrap;
  justify-content: center;
}

.search-input, .region-select {
  padding: 12px 16px;
  border: 2px solid #e1e8ed;
  border-radius: 25px;
  font-size: 1rem;
  min-width: 200px;
  transition: border-color 0.3s ease;
}

.search-input:focus, .region-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.countries-container {
  margin-top: 20px;
}

.results-info {
  text-align: center;
  margin-bottom: 20px;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 8px;
  color: #6c757d;
}

.countries-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 25px;
  margin-bottom: 30px;
}

.country-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.country-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
}

.country-header {
  position: relative;
  height: 120px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.country-flag-img {
  width: 80px;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.country-flag-emoji {
  position: absolute;
  top: 10px;
  right: 15px;
  font-size: 2rem;
}

.country-info {
  padding: 20px;
}

.country-name {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 15px 0;
  color: #2c3e50;
  text-align: center;
}

.country-details {
  margin-bottom: 20px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  padding: 4px 0;
}

.label {
  font-weight: 600;
  color: #7f8c8d;
}

.value {
  color: #2c3e50;
  text-align: right;
  max-width: 200px;
  word-wrap: break-word;
}

.country-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.favorite-btn, .details-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.favorite-btn {
  background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
  color: white;
}

.favorite-btn.favorited {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
}

.details-btn {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
}

.favorite-btn:hover, .details-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  color: #6c757d;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  text-align: center;
  padding: 40px;
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
  border-radius: 15px;
  margin: 20px;
}

.error-message button {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid white;
  padding: 10px 20px;
  border-radius: 25px;
  cursor: pointer;
  margin-top: 15px;
  transition: all 0.3s ease;
}

.error-message button:hover {
  background: white;
  color: #e74c3c;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #7f8c8d;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

/* Responsividade */
@media (max-width: 768px) {
  .countries-grid {
    grid-template-columns: 1fr;
  }
  
  .app-controls {
    flex-direction: column;
    align-items: center;
  }
  
  .search-input, .region-select {
    width: 100%;
    max-width: 300px;
  }
  
  .country-header {
    height: 100px;
  }
  
  .country-flag-img {
    width: 60px;
  }
}
```

---

## **📝 Exercício Prático**

### 🎯 **Objetivo**
Implementar as 3 fases do projeto com diferentes fontes de dados

### 📋 **Requisitos**
- [ ] **Fase 1**: Implementar com dados locais (hardcoded)
- [ ] **Fase 2**: Criar arquivo JSON e implementar carregamento
- [ ] **Fase 3**: Adicionar seletor de fonte de dados
- [ ] **Bonus**: Implementar persistência de favoritos
- [ ] **Bonus**: Adicionar filtros avançados (população, área)

### 🚀 **Próximos Passos**
1. Implementar busca com debounce
2. Adicionar ordenação (nome, população, área)
3. Criar modal de detalhes do país
4. Implementar modo offline

---

## **🔮 Próximo Módulo**

No próximo módulo, implementaremos o **consumo de APIs GET reais**, conectando nossa Lista de Países com a API REST Countries e adicionando recursos avançados como paginação, cache e tratamento robusto de erros!

---

## **📚 Resumo do Módulo**

- ✅ **Projeto Evolutivo**: Dados locais → JSON → API
- ✅ **Componentização**: Estrutura modular e reutilizável  
- ✅ **Estados Múltiplos**: Loading, erro, dados, filtros
- ✅ **Hooks Customizados**: Lógica reutilizável
- ✅ **Persistência**: localStorage para favoritos
- ✅ **UX Completa**: Loading, erro, estados vazios
