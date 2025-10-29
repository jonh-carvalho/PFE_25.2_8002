---
id: 13_Filtros_Busca
title: 13 - Filtros e Busca Inteligente
---

# 13 - **Filtros e Busca Inteligente**

Chegamos ao módulo final! Agora vamos implementar funcionalidades avançadas de **busca e filtros** em nossa Lista de Países, criando uma experiência de usuário completa e profissional. Este módulo consolida todo o aprendizado do curso em um projeto final robusto.

---

## **Objetivos do Módulo**
- Implementar busca em tempo real por múltiplos critérios
- Criar filtros combinados (região + população + área)
- Adicionar ordenação dinâmica dos resultados
- Desenvolver funcionalidades avançadas de UX
- Finalizar o projeto completo "Lista de Países"

---

## **🔍 Sistema de Busca Inteligente**

### **1. Hook de Busca Avançada**

```jsx
// src/hooks/useCountrySearch.js
import { useState, useEffect, useMemo } from 'react';
import useDebounce from './useDebounce';

function useCountrySearch(countries) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRegion, setSelectedRegion] = useState('all');
  const [populationRange, setPopulationRange] = useState({ min: 0, max: Infinity });
  const [sortBy, setSortBy] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');
  
  // Debounce da busca para otimização
  const debouncedSearchTerm = useDebounce(searchTerm, 300);
  
  // Filtros e busca com useMemo para performance
  const filteredAndSortedCountries = useMemo(() => {
    let filtered = countries;
    
    // 1. Filtro por busca textual
    if (debouncedSearchTerm.trim()) {
      const search = debouncedSearchTerm.toLowerCase();
      filtered = filtered.filter(country =>
        country.name.common.toLowerCase().includes(search) ||
        country.capital?.[0]?.toLowerCase().includes(search) ||
        country.region.toLowerCase().includes(search) ||
        country.subregion?.toLowerCase().includes(search) ||
        Object.values(country.languages || {}).some(lang => 
          lang.toLowerCase().includes(search)
        )
      );
    }
    
    // 2. Filtro por região
    if (selectedRegion !== 'all') {
      filtered = filtered.filter(country => 
        country.region.toLowerCase() === selectedRegion.toLowerCase()
      );
    }
    
    // 3. Filtro por população
    filtered = filtered.filter(country => 
      country.population >= populationRange.min && 
      country.population <= populationRange.max
    );
    
    // 4. Ordenação
    filtered.sort((a, b) => {
      let valueA, valueB;
      
      switch (sortBy) {
        case 'name':
          valueA = a.name.common;
          valueB = b.name.common;
          break;
        case 'population':
          valueA = a.population;
          valueB = b.population;
          break;
        case 'area':
          valueA = a.area;
          valueB = b.area;
          break;
        case 'region':
          valueA = a.region;
          valueB = b.region;
          break;
        default:
          return 0;
      }
      
      if (typeof valueA === 'string') {
        valueA = valueA.toLowerCase();
        valueB = valueB.toLowerCase();
      }
      
      if (sortOrder === 'asc') {
        return valueA > valueB ? 1 : -1;
      } else {
        return valueA < valueB ? 1 : -1;
      }
    });
    
    return filtered;
  }, [countries, debouncedSearchTerm, selectedRegion, populationRange, sortBy, sortOrder]);
  
  // Estatísticas dos resultados
  const searchStats = useMemo(() => {
    return {
      totalCountries: countries.length,
      filteredCount: filteredAndSortedCountries.length,
      regions: [...new Set(countries.map(c => c.region))].sort(),
      avgPopulation: Math.round(
        filteredAndSortedCountries.reduce((sum, c) => sum + c.population, 0) / 
        filteredAndSortedCountries.length || 0
      ),
      totalPopulation: filteredAndSortedCountries.reduce((sum, c) => sum + c.population, 0)
    };
  }, [countries, filteredAndSortedCountries]);
  
  const clearAllFilters = () => {
    setSearchTerm('');
    setSelectedRegion('all');
    setPopulationRange({ min: 0, max: Infinity });
    setSortBy('name');
    setSortOrder('asc');
  };
  
  return {
    // Estados
    searchTerm,
    selectedRegion,
    populationRange,
    sortBy,
    sortOrder,
    
    // Setters
    setSearchTerm,
    setSelectedRegion,
    setPopulationRange,
    setSortBy,
    setSortOrder,
    
    // Dados processados
    filteredCountries: filteredAndSortedCountries,
    searchStats,
    
    // Ações
    clearAllFilters
  };
}

export default useCountrySearch;
```

### **2. Componente de Busca Avançada**

```jsx
// src/components/AdvancedSearchBar.jsx
import React from 'react';

function AdvancedSearchBar({ 
  searchTerm, 
  onSearchChange, 
  selectedRegion, 
  onRegionChange,
  regions,
  sortBy,
  onSortByChange,
  sortOrder,
  onSortOrderChange,
  populationRange,
  onPopulationRangeChange,
  onClearFilters,
  searchStats
}) {
  const populationPresets = [
    { label: 'Todos', min: 0, max: Infinity },
    { label: 'Pequenos (< 1M)', min: 0, max: 1000000 },
    { label: 'Médios (1M - 10M)', min: 1000000, max: 10000000 },
    { label: 'Grandes (10M - 100M)', min: 10000000, max: 100000000 },
    { label: 'Muito Grandes (> 100M)', min: 100000000, max: Infinity }
  ];

  return (
    <div className="advanced-search-container">
      {/* Busca Principal */}
      <div className="search-main">
        <div className="search-input-container">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            placeholder="Buscar por país, capital, região ou idioma..."
            value={searchTerm}
            onChange={(e) => onSearchChange(e.target.value)}
            className="search-input-advanced"
          />
          {searchTerm && (
            <button 
              onClick={() => onSearchChange('')}
              className="clear-search-btn"
              title="Limpar busca"
            >
              ✕
            </button>
          )}
        </div>
      </div>

      {/* Filtros */}
      <div className="filters-container">
        {/* Filtro por Região */}
        <div className="filter-group">
          <label>🌍 Região:</label>
          <select 
            value={selectedRegion} 
            onChange={(e) => onRegionChange(e.target.value)}
            className="filter-select"
          >
            <option value="all">Todas as regiões</option>
            {regions.map(region => (
              <option key={region} value={region}>{region}</option>
            ))}
          </select>
        </div>

        {/* Filtro por População */}
        <div className="filter-group">
          <label>👥 População:</label>
          <select 
            onChange={(e) => {
              const preset = populationPresets[e.target.value];
              onPopulationRangeChange(preset);
            }}
            className="filter-select"
          >
            {populationPresets.map((preset, index) => (
              <option key={index} value={index}>{preset.label}</option>
            ))}
          </select>
        </div>

        {/* Ordenação */}
        <div className="filter-group">
          <label>📊 Ordenar por:</label>
          <select 
            value={sortBy} 
            onChange={(e) => onSortByChange(e.target.value)}
            className="filter-select"
          >
            <option value="name">Nome</option>
            <option value="population">População</option>
            <option value="area">Área</option>
            <option value="region">Região</option>
          </select>
          
          <button 
            onClick={() => onSortOrderChange(sortOrder === 'asc' ? 'desc' : 'asc')}
            className="sort-order-btn"
            title={`Ordem: ${sortOrder === 'asc' ? 'Crescente' : 'Decrescente'}`}
          >
            {sortOrder === 'asc' ? '↑' : '↓'}
          </button>
        </div>

        {/* Botão Limpar */}
        <button onClick={onClearFilters} className="clear-all-btn">
          🗑️ Limpar Tudo
        </button>
      </div>

      {/* Estatísticas */}
      <div className="search-stats">
        <div className="stat">
          <span className="stat-value">{searchStats.filteredCount}</span>
          <span className="stat-label">países encontrados</span>
        </div>
        <div className="stat">
          <span className="stat-value">
            {new Intl.NumberFormat('pt-BR').format(searchStats.totalPopulation)}
          </span>
          <span className="stat-label">população total</span>
        </div>
        <div className="stat">
          <span className="stat-value">
            {new Intl.NumberFormat('pt-BR').format(searchStats.avgPopulation)}
          </span>
          <span className="stat-label">população média</span>
        </div>
      </div>
    </div>
  );
}

export default AdvancedSearchBar;
```

---

## **🎯 App Final Completo**

```jsx
// src/App.jsx - Versão Final
import React, { useState, useEffect } from 'react';
import CountryCard from './components/CountryCard';
import AdvancedSearchBar from './components/AdvancedSearchBar';
import Loading from './components/Loading';
import ErrorMessage from './components/ErrorMessage';
import CountryModal from './components/CountryModal';
import useCountries from './hooks/useCountries';
import useCountrySearch from './hooks/useCountrySearch';
import './App.css';

function App() {
  // Estados principais
  const { countries, isLoading, error, refetch } = useCountries();
  const [favorites, setFavorites] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState(null);
  const [viewMode, setViewMode] = useState('grid'); // 'grid' ou 'list'
  
  // Hook de busca
  const {
    searchTerm,
    selectedRegion,
    populationRange,
    sortBy,
    sortOrder,
    setSearchTerm,
    setSelectedRegion,
    setPopulationRange,
    setSortBy,
    setSortOrder,
    filteredCountries,
    searchStats,
    clearAllFilters
  } = useCountrySearch(countries);

  // Carregar favoritos
  useEffect(() => {
    const savedFavorites = localStorage.getItem('countryFavorites');
    if (savedFavorites) {
      setFavorites(JSON.parse(savedFavorites));
    }
  }, []);

  // Salvar favoritos
  useEffect(() => {
    localStorage.setItem('countryFavorites', JSON.stringify(favorites));
  }, [favorites]);

  // Funções
  const toggleFavorite = (countryCode) => {
    setFavorites(prev => 
      prev.includes(countryCode)
        ? prev.filter(code => code !== countryCode)
        : [...prev, countryCode]
    );
  };

  const handleViewDetails = (country) => {
    setSelectedCountry(country);
  };

  const closeModal = () => {
    setSelectedCountry(null);
  };

  // Estados de carregamento
  if (isLoading) {
    return <Loading message="Carregando base de dados mundial..." />;
  }

  if (error) {
    return (
      <ErrorMessage 
        title="Erro ao Carregar Base de Dados"
        message={error}
        onRetry={refetch}
      />
    );
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1>🌍 Explorador de Países</h1>
          <p className="header-subtitle">
            Descubra informações sobre todos os países do mundo
          </p>
          
          <div className="header-stats">
            <div className="header-stat">
              <span className="stat-number">{countries.length}</span>
              <span className="stat-text">países</span>
            </div>
            <div className="header-stat">
              <span className="stat-number">{searchStats.regions.length}</span>
              <span className="stat-text">regiões</span>
            </div>
            <div className="header-stat">
              <span className="stat-number">{favorites.length}</span>
              <span className="stat-text">favoritos</span>
            </div>
          </div>
        </div>
      </header>

      {/* Busca e Filtros */}
      <div className="search-section">
        <AdvancedSearchBar
          searchTerm={searchTerm}
          onSearchChange={setSearchTerm}
          selectedRegion={selectedRegion}
          onRegionChange={setSelectedRegion}
          regions={searchStats.regions}
          sortBy={sortBy}
          onSortByChange={setSortBy}
          sortOrder={sortOrder}
          onSortOrderChange={setSortOrder}
          populationRange={populationRange}
          onPopulationRangeChange={setPopulationRange}
          onClearFilters={clearAllFilters}
          searchStats={searchStats}
        />
      </div>

      {/* Controles de Visualização */}
      <div className="view-controls">
        <div className="view-mode-toggle">
          <button 
            className={`view-btn ${viewMode === 'grid' ? 'active' : ''}`}
            onClick={() => setViewMode('grid')}
            title="Visualização em Grade"
          >
            ⊞ Grade
          </button>
          <button 
            className={`view-btn ${viewMode === 'list' ? 'active' : ''}`}
            onClick={() => setViewMode('list')}
            title="Visualização em Lista"
          >
            ☰ Lista
          </button>
        </div>
        
        <div className="results-summary">
          Exibindo {filteredCountries.length} de {countries.length} países
        </div>
      </div>

      {/* Lista de Países */}
      <main className="countries-container">
        {filteredCountries.length > 0 ? (
          <div className={`countries-${viewMode}`}>
            {filteredCountries.map(country => (
              <CountryCard
                key={country.cca3}
                country={country}
                isFavorite={favorites.includes(country.cca3)}
                onToggleFavorite={toggleFavorite}
                onViewDetails={handleViewDetails}
                viewMode={viewMode}
              />
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-icon">🔍</div>
            <h3>Nenhum país encontrado</h3>
            <p>Tente ajustar os critérios de busca e filtros.</p>
            <button onClick={clearAllFilters} className="btn-primary">
              Mostrar Todos os Países
            </button>
          </div>
        )}
      </main>

      {/* Modal de Detalhes */}
      {selectedCountry && (
        <CountryModal 
          country={selectedCountry} 
          onClose={closeModal}
          isFavorite={favorites.includes(selectedCountry.cca3)}
          onToggleFavorite={toggleFavorite}
        />
      )}

      {/* Footer */}
      <footer className="app-footer">
        <p>
          💻 Projeto desenvolvido com React + REST Countries API
          <br />
          📚 Curso completo de React - Do básico ao avançado
        </p>
      </footer>
    </div>
  );
}

export default App;
```

---

## **💫 Modal de Detalhes Completo**

```jsx
// src/components/CountryModal.jsx
import React from 'react';

function CountryModal({ country, onClose, isFavorite, onToggleFavorite }) {
  const formatNumber = (num) => new Intl.NumberFormat('pt-BR').format(num);
  
  const getLanguages = (languages) => {
    return Object.values(languages || {}).join(', ') || 'N/A';
  };
  
  const getCurrencies = (currencies) => {
    if (!currencies) return 'N/A';
    return Object.values(currencies)
      .map(curr => `${curr.name} (${curr.symbol})`)
      .join(', ');
  };

  const getTimezones = (timezones) => {
    return timezones?.slice(0, 3).join(', ') + 
           (timezones?.length > 3 ? '...' : '') || 'N/A';
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>✕</button>
        
        <div className="modal-header">
          <img 
            src={country.flags.png} 
            alt={`Bandeira de ${country.name.common}`}
            className="modal-flag"
          />
          <div className="modal-title">
            <h2>{country.name.common}</h2>
            <p className="country-official-name">
              {country.name.official}
            </p>
          </div>
          <div className="modal-emoji">{country.flag}</div>
        </div>

        <div className="modal-body">
          <div className="info-grid">
            <div className="info-section">
              <h3>📍 Localização</h3>
              <div className="info-item">
                <span className="label">Capital:</span>
                <span className="value">{country.capital?.[0] || 'N/A'}</span>
              </div>
              <div className="info-item">
                <span className="label">Região:</span>
                <span className="value">{country.region}</span>
              </div>
              <div className="info-item">
                <span className="label">Sub-região:</span>
                <span className="value">{country.subregion || 'N/A'}</span>
              </div>
              <div className="info-item">
                <span className="label">Coordenadas:</span>
                <span className="value">
                  {country.latlng ? `${country.latlng[0]}°, ${country.latlng[1]}°` : 'N/A'}
                </span>
              </div>
            </div>

            <div className="info-section">
              <h3>👥 Demografia</h3>
              <div className="info-item">
                <span className="label">População:</span>
                <span className="value">{formatNumber(country.population)}</span>
              </div>
              <div className="info-item">
                <span className="label">Área:</span>
                <span className="value">{formatNumber(country.area)} km²</span>
              </div>
              <div className="info-item">
                <span className="label">Densidade:</span>
                <span className="value">
                  {Math.round(country.population / country.area)} hab/km²
                </span>
              </div>
            </div>

            <div className="info-section">
              <h3>🗣️ Idiomas & Cultura</h3>
              <div className="info-item">
                <span className="label">Idiomas:</span>
                <span className="value">{getLanguages(country.languages)}</span>
              </div>
              <div className="info-item">
                <span className="label">Moedas:</span>
                <span className="value">{getCurrencies(country.currencies)}</span>
              </div>
              <div className="info-item">
                <span className="label">Fusos Horários:</span>
                <span className="value">{getTimezones(country.timezones)}</span>
              </div>
            </div>
          </div>

          <div className="modal-actions">
            <button 
              className={`favorite-modal-btn ${isFavorite ? 'favorited' : ''}`}
              onClick={() => onToggleFavorite(country.cca3)}
            >
              {isFavorite ? '❤️ Remover dos Favoritos' : '🤍 Adicionar aos Favoritos'}
            </button>
            
            <a
              href={`https://www.google.com/maps/search/${country.name.common}`}
              target="_blank"
              rel="noopener noreferrer"
              className="maps-btn"
            >
              🗺️ Ver no Maps
            </a>
            
            <a
              href={`https://pt.wikipedia.org/wiki/${country.name.common}`}
              target="_blank"
              rel="noopener noreferrer"
              className="wiki-btn"
            >
              📖 Wikipedia
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CountryModal;
```

---

## **🎨 Estilos Finais Completos**

```css
/* Busca Avançada */
.advanced-search-container {
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  margin-bottom: 30px;
}

.search-main {
  margin-bottom: 20px;
}

.search-input-container {
  position: relative;
  max-width: 600px;
  margin: 0 auto;
}

.search-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #7f8c8d;
  font-size: 1.2rem;
}

.search-input-advanced {
  width: 100%;
  padding: 15px 15px 15px 45px;
  border: 2px solid #e1e8ed;
  border-radius: 25px;
  font-size: 1.1rem;
  transition: border-color 0.3s ease;
}

.search-input-advanced:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.clear-search-btn {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #95a5a6;
}

.filters-container {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
  min-width: 120px;
}

.sort-order-btn {
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 8px 10px;
  cursor: pointer;
  font-size: 1rem;
  margin-left: 5px;
}

.clear-all-btn {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}

.search-stats {
  display: flex;
  justify-content: center;
  gap: 30px;
  padding-top: 15px;
  border-top: 1px solid #ecf0f1;
}

.stat {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
}

.stat-label {
  display: block;
  font-size: 0.9rem;
  color: #7f8c8d;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 20px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

.modal-close {
  position: absolute;
  top: 15px;
  right: 20px;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #95a5a6;
  z-index: 10;
}

.modal-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 30px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.modal-flag {
  width: 80px;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.modal-title h2 {
  margin: 0;
  font-size: 2rem;
}

.country-official-name {
  margin: 5px 0 0 0;
  opacity: 0.9;
  font-style: italic;
}

.modal-emoji {
  font-size: 3rem;
  margin-left: auto;
}

.modal-body {
  padding: 30px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 25px;
  margin-bottom: 30px;
}

.info-section h3 {
  color: #2c3e50;
  margin: 0 0 15px 0;
  font-size: 1.2rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  padding: 8px 0;
  border-bottom: 1px solid #ecf0f1;
}

.info-item .label {
  font-weight: 600;
  color: #7f8c8d;
}

.info-item .value {
  color: #2c3e50;
  text-align: right;
  max-width: 60%;
  word-wrap: break-word;
}

.modal-actions {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  justify-content: center;
}

.favorite-modal-btn, .maps-btn, .wiki-btn {
  padding: 12px 20px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.favorite-modal-btn {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
}

.favorite-modal-btn.favorited {
  background: linear-gradient(135deg, #27ae60, #229954);
}

.maps-btn {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
}

.wiki-btn {
  background: linear-gradient(135deg, #9b59b6, #8e44ad);
  color: white;
}

/* View Controls */
.view-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 10px;
}

.view-mode-toggle {
  display: flex;
  gap: 10px;
}

.view-btn {
  padding: 10px 15px;
  border: 2px solid #e1e8ed;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-btn.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.countries-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.countries-list .country-card {
  display: flex;
  align-items: center;
  padding: 15px;
  margin: 0;
}

.countries-list .country-header {
  height: 60px;
  width: 80px;
  flex-shrink: 0;
  margin-right: 20px;
}

.countries-list .country-info {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Footer */
.app-footer {
  background: #2c3e50;
  color: white;
  text-align: center;
  padding: 30px 20px;
  margin-top: 50px;
}

/* Responsividade */
@media (max-width: 768px) {
  .filters-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-group {
    justify-content: space-between;
  }
  
  .search-stats {
    flex-direction: column;
    gap: 15px;
  }
  
  .modal-header {
    flex-direction: column;
    text-align: center;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .view-controls {
    flex-direction: column;
    gap: 15px;
  }
}
```

---

## **📝 Exercício Final**

### 🎯 **Objetivo**
Implementar o sistema completo de busca e filtros no projeto Lista de Países

### 📋 **Requisitos Finais**
- [ ] Busca em tempo real por múltiplos critérios
- [ ] Filtros combinados (região + população)
- [ ] Ordenação dinâmica dos resultados
- [ ] Modal de detalhes completo
- [ ] Alternância entre visualização em grade/lista
- [ ] Persistência de favoritos
- [ ] Estatísticas em tempo real
- [ ] Interface responsiva completa

### 🚀 **Funcionalidades Bonus**
- [ ] Exportar lista de favoritos
- [ ] Modo escuro/claro
- [ ] Comparar países side-by-side
- [ ] Gráficos de população por região

---

## **🎓 Conclusão do Curso**

**Parabéns!** Você completou o curso completo de React! 

### **📚 O que você aprendeu:**
- ✅ **JSX e Componentes**: Base sólida do React
- ✅ **Props e Estado**: Comunicação e gerenciamento
- ✅ **Hooks**: useState, useEffect, hooks customizados
- ✅ **APIs**: Consumo e tratamento de dados
- ✅ **UX Avançada**: Loading, erros, filtros, busca
- ✅ **Projeto Real**: Aplicação completa e funcional

### **🚀 Próximos Passos:**
1. **React Router**: Navegação entre páginas
2. **Context API**: Gerenciamento global de estado
3. **React Query**: Cache e sincronização de dados
4. **TypeScript**: Tipagem estática
5. **Testes**: Jest e React Testing Library
6. **Deploy**: Vercel, Netlify, Azure

### **💼 Portfolio:**
Sua **Lista de Países** está pronta para o portfólio! É um projeto completo que demonstra:
- Consumo de APIs reais
- Interface moderna e responsiva
- Funcionalidades avançadas de UX
- Código limpo e organizado

**Continue praticando e construindo projetos incríveis com React!** 🚀

---

## **📚 Resumo do Módulo**

- ✅ **Busca Inteligente**: Múltiplos critérios e debounce
- ✅ **Filtros Avançados**: Região, população, ordenação
- ✅ **Modal Completo**: Detalhes e links externos
- ✅ **UX Profissional**: Estatísticas e visualizações
- ✅ **Projeto Finalizado**: Aplicação completa e robusta
- ✅ **Curso Concluído**: Base sólida para React moderno