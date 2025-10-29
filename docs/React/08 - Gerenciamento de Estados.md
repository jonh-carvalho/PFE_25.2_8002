---
id: 08 - Gerenciamento de Estados 
title: 08 - Gerenciamento de Estados 
---

# 08 - **Gerenciamento de Estados**

Agora vamos além do básico de listas e estados! Aprenderemos a gerenciar **múltiplos estados simultâneos** e criar funcionalidades interativas avançadas na nossa **Lista de Países**. Trabalharemos com favoritos, filtros, contadores dinâmicos e preparação para consumir dados externos.

---

## **Objetivos do Módulo**
- Gerenciar múltiplos estados simultâneos (favoritos, filtros, busca)
- Sincronizar estados entre componentes pai e filho
- Implementar renderização condicional complexa
- Criar filtros locais e contadores dinâmicos
- Preparar estrutura para consumir APIs (próximo módulo)

---


**Agora vamos elevar o nível:**

- Gerenciar múltiplos estados relacionados
- Sincronizar estados entre componentes
- Criar funcionalidades interativas complexas
- Preparar para consumir dados de APIs

---

## **1. Gerenciando Múltiplos Estados Simultâneos**

Em aplicações reais, raramente trabalhamos com apenas um estado. Vamos gerenciar **vários estados que interagem entre si**.

### **Cenário Real: Lista de Países com Funcionalidades**

Nossa aplicação terá:

1. **Lista de países** (dados)
2. **Favoritos** (array de IDs)
3. **Filtro por região** (string)
4. **Termo de busca** (string)
5. **Modo de visualização** (grid/list)

### **Estrutura de Estados no App.jsx**

```jsx
// src/App.jsx
import { useState } from 'react';
import Header from './components/Header';
import CountryGrid from './components/CountryGrid';
import './App.css';

function App() {
  // Estado 1: Dados dos países (simulando o que virá de API)
  const [countries] = useState([
    {
      id: 1,
      cca3: "BRA",
      name: "Brasil",
      capital: "Brasília",
      population: 215000000,
      region: "Americas",
      subregion: "South America",
      flag: "🇧🇷"
    },
    {
      id: 2,
      cca3: "ARG",
      name: "Argentina",
      capital: "Buenos Aires",
      population: 45000000,
      region: "Americas",
      subregion: "South America",
      flag: "🇦🇷"
    },
    {
      id: 3,
      cca3: "FRA",
      name: "França",
      capital: "Paris",
      population: 67000000,
      region: "Europe",
      subregion: "Western Europe",
      flag: "🇫🇷"
    },
    {
      id: 4,
      cca3: "JPN",
      name: "Japão",
      capital: "Tóquio",
      population: 125000000,
      region: "Asia",
      subregion: "Eastern Asia",
      flag: "🇯🇵"
    },
    {
      id: 5,
      cca3: "AUS",
      name: "Austrália",
      capital: "Canberra",
      population: 26000000,
      region: "Oceania",
      subregion: "Australia and New Zealand",
      flag: "🇦🇺"
    },
    {
      id: 6,
      cca3: "ZAF",
      name: "África do Sul",
      capital: "Pretória",
      population: 60000000,
      region: "Africa",
      subregion: "Southern Africa",
      flag: "🇿🇦"
    }
  ]);

  // Estado 2: Favoritos (array de códigos de países)
  const [favorites, setFavorites] = useState([]);

  // Estado 3: Região selecionada no filtro
  const [selectedRegion, setSelectedRegion] = useState('all');

  // Estado 4: Termo de busca
  const [searchTerm, setSearchTerm] = useState('');

  // Estado 5: Modo de visualização
  const [showOnlyFavorites, setShowOnlyFavorites] = useState(false);

  // Função para alternar favorito
  const toggleFavorite = (countryCode) => {
    setFavorites(prev => 
      prev.includes(countryCode)
        ? prev.filter(code => code !== countryCode)  // Remove
        : [...prev, countryCode]                     // Adiciona
    );
  };

  // Aplicar filtros combinados
  const getFilteredCountries = () => {
    let filtered = countries;

    // Filtro 1: Apenas favoritos (se ativado)
    if (showOnlyFavorites) {
      filtered = filtered.filter(country => favorites.includes(country.cca3));
    }

    // Filtro 2: Por região
    if (selectedRegion !== 'all') {
      filtered = filtered.filter(country => country.region === selectedRegion);
    }

    // Filtro 3: Por busca textual
    if (searchTerm.trim()) {
      const search = searchTerm.toLowerCase();
      filtered = filtered.filter(country =>
        country.name.toLowerCase().includes(search) ||
        country.capital.toLowerCase().includes(search) ||
        country.region.toLowerCase().includes(search)
      );
    }

    return filtered;
  };

  const filteredCountries = getFilteredCountries();

  // Extrair regiões únicas para o filtro
  const regions = ['all', ...new Set(countries.map(c => c.region))];

  return (
    <div className="app">
      <Header 
        title="🌍 Lista de Países da América do Sul"
        subtitle="Gerenciamento de estados complexos em React"
        totalCountries={countries.length}
        favoriteCount={favorites.length}
        filteredCount={filteredCountries.length}
      />
      
      {/* Controles de Filtro */}
      <div className="controls">
        {/* Busca */}
        <div className="search-box">
          <input
            type="text"
            placeholder="🔍 Buscar por país, capital ou região..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
          {searchTerm && (
            <button 
              onClick={() => setSearchTerm('')}
              className="clear-btn"
              title="Limpar busca"
            >
              ✕
            </button>
          )}
        </div>

        {/* Filtro de Região */}
        <div className="filter-region">
          <label>🌍 Região:</label>
          <select 
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
            className="region-select"
          >
            {regions.map(region => (
              <option key={region} value={region}>
                {region === 'all' ? 'Todas as regiões' : region}
              </option>
            ))}
          </select>
        </div>

        {/* Toggle Favoritos */}
        <button 
          className={`filter-btn ${showOnlyFavorites ? 'active' : ''}`}
          onClick={() => setShowOnlyFavorites(!showOnlyFavorites)}
        >
          {showOnlyFavorites ? '📋 Mostrar Todos' : '❤️ Mostrar Favoritos'}
        </button>

        {/* Limpar Filtros */}
        {(searchTerm || selectedRegion !== 'all' || showOnlyFavorites) && (
          <button 
            onClick={() => {
              setSearchTerm('');
              setSelectedRegion('all');
              setShowOnlyFavorites(false);
            }}
            className="clear-all-btn"
          >
            🗑️ Limpar Filtros
          </button>
        )}
      </div>

      {/* Resultados */}
      <div className="results-info">
        <p>
          Exibindo <strong>{filteredCountries.length}</strong> de {countries.length} países
          {showOnlyFavorites && ' (somente favoritos)'}
          {searchTerm && ` - Busca: "${searchTerm}"`}
          {selectedRegion !== 'all' && ` - Região: ${selectedRegion}`}
        </p>
      </div>
      
      {/* Grid de Países */}
      {filteredCountries.length > 0 ? (
        <CountryGrid 
          countries={filteredCountries}
          favorites={favorites}
          onToggleFavorite={toggleFavorite}
        />
      ) : (
        <div className="empty-state">
          <p className="empty-icon">🔍</p>
          <h3>Nenhum país encontrado</h3>
          <p>Tente ajustar os filtros de busca ou região.</p>
          <button 
            onClick={() => {
              setSearchTerm('');
              setSelectedRegion('all');
              setShowOnlyFavorites(false);
            }}
            className="btn-reset"
          >
            Resetar Filtros
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
```

---

## **2. Sincronizando Estados com Componentes Filhos**

Agora vamos atualizar os componentes para trabalhar com os estados do pai:

### **Header Component (Recebe props de estado)**

```jsx
// src/components/Header.jsx
function Header({ title, subtitle, totalCountries, favoriteCount, filteredCount }) {
  return (
    <header className="app-header">
      <h1>{title}</h1>
      {subtitle && <p className="subtitle">{subtitle}</p>}

      <div className="header-stats">
        <div className="stat-box">
          <span className="stat-value">{totalCountries}</span>
          <span className="stat-label">países</span>
        </div>
        <div className="stat-box">
          <span className="stat-value">{favoriteCount}</span>
          <span className="stat-label">favoritos</span>
        </div>
        <div className="stat-box">
          <span className="stat-value">{filteredCount}</span>
          <span className="stat-label">exibidos</span>
        </div>
      </div>
    </header>
  );
}

export default Header;
```

### **CountryGrid Component**

```jsx
// src/components/CountryGrid.jsx
import CountryCard from './CountryCard';

function CountryGrid({ countries, favorites, onToggleFavorite }) {
  return (
    <div className="country-grid">
      {countries.map((country) => (
        <CountryCard 
          key={country.cca3}
          id={country.id}
          cca3={country.cca3}
          flag={country.flag}
          name={country.name}
          capital={country.capital}
          population={country.population}
          region={country.region}
          subregion={country.subregion}
          isFavorite={favorites.includes(country.cca3)}
          onToggleFavorite={onToggleFavorite}
        />
      ))}
    </div>
  );
}

export default CountryGrid;
```

### **CountryCard Component (Sem estado local)**

```jsx
// src/components/CountryCard.jsx
function CountryCard({ 
  cca3, 
  flag, 
  name, 
  capital, 
  population, 
  region,
  subregion,
  isFavorite, 
  onToggleFavorite 
}) {
  const formatPopulation = (pop) => {
    return new Intl.NumberFormat('pt-BR').format(pop);
  };

  return (
    <div className={`country-card ${isFavorite ? 'favorite' : ''}`}>
      <div className="country-header">
        <span className="flag">{flag}</span>
        <h3>{name}</h3>
      </div>

      <div className="country-info">
        <div className="info-row">
          <span className="label">Capital:</span>
          <span className="value">{capital}</span>
        </div>
        <div className="info-row">
          <span className="label">População:</span>
          <span className="value">{formatPopulation(population)}</span>
        </div>
        <div className="info-row">
          <span className="label">Região:</span>
          <span className="value">{region}</span>
        </div>
        <div className="info-row">
          <span className="label">Sub-região:</span>
          <span className="value">{subregion}</span>
        </div>
      </div>

      <button 
        className={`favorite-btn ${isFavorite ? 'favorited' : ''}`}
        onClick={() => onToggleFavorite(cca3)}
        title={isFavorite ? 'Remover dos favoritos' : 'Adicionar aos favoritos'}
      >
        {isFavorite ? '❤️ Favorito' : '🤍 Favoritar'}
      </button>
    </div>
  );
}

export default CountryCard;
```

---

## **3. Renderização Condicional Avançada**

### **Padrão 1: Operador Lógico `&&`**

Use quando quiser mostrar algo **apenas se** uma condição for verdadeira:

```jsx
{/* Mostrar botão APENAS se houver filtros ativos */}
{(searchTerm || selectedRegion !== 'all') && (
  <button onClick={clearFilters}>
    Limpar Filtros
  </button>
)}

{/* Mostrar estatística APENAS se houver favoritos */}
{favorites.length > 0 && (
  <div className="favorite-counter">
    ❤️ {favorites.length} países favoritos
  </div>
)}
```

### **Padrão 2: Operador Ternário**

Use quando quiser mostrar **uma coisa OU outra**:

```jsx
{/* Texto do botão muda baseado no estado */}
<button>
  {showOnlyFavorites ? 'Mostrar Todos' : 'Mostrar Favoritos'}
</button>

{/* Renderizar grid OU mensagem vazia */}
{filteredCountries.length > 0 ? (
  <CountryGrid countries={filteredCountries} />
) : (
  <EmptyState message="Nenhum país encontrado" />
)}
```

### **Padrão 3: Classes Condicionais**

```jsx
{/* Adicionar classe CSS baseada em estado */}
<div className={`country-card ${isFavorite ? 'favorite' : ''}`}>

{/* Classes múltiplas condicionais */}
<button className={`filter-btn ${showOnlyFavorites ? 'active' : ''} ${hasResults ? 'enabled' : 'disabled'}`}>
```

---

## **4. Padrões de Gerenciamento de Estados**

### **Padrão 1: Estado Derivado**

Estados que podem ser calculados a partir de outros estados:

```jsx
// NÃO faça isso - estado redundante
const [countries, setCountries] = useState([...]);
const [filteredCountries, setFilteredCountries] = useState([...]);

// Faça isso - calcule na renderização
const [countries, setCountries] = useState([...]);
const filteredCountries = countries.filter(...); // Derivado!
```

### ** Padrão 2: Update Funcional**

Sempre use função quando o novo estado depende do anterior:

```jsx
// Perigoso - pode ter valor antigo
const toggleFavorite = (id) => {
  if (favorites.includes(id)) {
    setFavorites(favorites.filter(f => f !== id));
  } else {
    setFavorites([...favorites, id]);
  }
};

// Seguro - sempre usa valor mais recente
const toggleFavorite = (id) => {
  setFavorites(prev => 
    prev.includes(id)
      ? prev.filter(f => f !== id)
      : [...prev, id]
  );
};
```

### **Padrão 3: Estados Independentes**

Separe estados que não têm relação direta:

```jsx
// BOM - Estados independentes
const [searchTerm, setSearchTerm] = useState('');
const [selectedRegion, setSelectedRegion] = useState('all');
const [favorites, setFavorites] = useState([]);

// RUIM - Tudo em um objeto (dificulta updates)
const [filters, setFilters] = useState({
  search: '',
  region: 'all',
  favorites: []
});
```

---

## **5. Preparando para Dados de API**

No próximo módulo, vamos conectar com uma API real. Vamos preparar nossa estrutura:

### **Estrutura de Dados Compatível com API**

```jsx
// Estrutura que usaremos com REST Countries API
const countryFromAPI = {
  cca3: "BRA",           // Código do país (key única)
  name: "Brazil",        // Nome comum
  capital: ["Brasília"], // Array de capitais
  population: 215353593, // População (número)
  region: "Americas",    // Região
  subregion: "South America", // Sub-região
  flag: "🇧🇷"           // Emoji da bandeira
};

// Nossa estrutura local é similar, facilitando a migração
const ourCountry = {
  id: 1,
  cca3: "BRA",
  name: "Brasil",
  capital: "Brasília",
  population: 215000000,
  region: "Americas",
  subregion: "South America",
  flag: "🇧🇷"
};
```

### **Estado Preparado para Loading**

```jsx
// Preparando para o próximo módulo
function App() {
  const [countries, setCountries] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  
  // Simulando estrutura que usaremos com API
  const loadCountries = () => {
    setIsLoading(true);
    // No próximo módulo: fetch('api...')
    setTimeout(() => {
      setCountries(localData);
      setIsLoading(false);
    }, 1000);
  };
  
  if (isLoading) {
    return <div>Carregando...</div>;
  }
  
  return <div>{/* Resto do app */}</div>;
}
```

---

## **6. Atualização do CSS**

```css
/* src/App.css */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #f5f7fa;
  min-height: 100vh;
}

/* Header */
.app-header {
  text-align: center;
  margin-bottom: 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 30px;
  border-radius: 15px;
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.app-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 20px;
}

.header-stats {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-top: 20px;
  flex-wrap: wrap;
}

.stat-box {
  background: rgba(255, 255, 255, 0.2);
  padding: 12px 20px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 100px;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.9;
  margin-top: 5px;
}

/* Controles */
.controls {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
  flex-wrap: wrap;
  align-items: center;
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.search-box {
  flex: 1;
  min-width: 250px;
  position: relative;
}

.search-input {
  width: 100%;
  padding: 12px 40px 12px 15px;
  border: 2px solid #e1e8ed;
  border-radius: 25px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.clear-btn {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #95a5a6;
  cursor: pointer;
  padding: 5px;
}

.filter-region {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-region label {
  font-weight: 600;
  color: #2c3e50;
}

.region-select {
  padding: 10px 15px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.region-select:focus {
  outline: none;
  border-color: #667eea;
}

.filter-btn, .clear-all-btn {
  padding: 10px 20px;
  border: 2px solid #e1e8ed;
  border-radius: 25px;
  background: white;
  color: #2c3e50;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn:hover, .clear-all-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.filter-btn.active {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
  border-color: #e74c3c;
}

.clear-all-btn {
  background: linear-gradient(135deg, #95a5a6, #7f8c8d);
  color: white;
  border-color: #95a5a6;
}

/* Informações de Resultados */
.results-info {
  background: white;
  padding: 15px 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.results-info p {
  color: #2c3e50;
  font-size: 1rem;
  margin: 0;
}

.results-info strong {
  color: #667eea;
  font-weight: 700;
}

/* Grid de Países */
.country-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.country-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  padding: 20px;
  text-align: center;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.country-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}

.country-card.favorite {
  border-color: #e74c3c;
  box-shadow: 0 4px 15px rgba(231, 76, 60, 0.2);
}

.country-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.flag {
  font-size: 4rem;
  margin-bottom: 10px;
}

.country-header h3 {
  color: #2c3e50;
  font-size: 1.5rem;
  margin: 0;
}

.country-info {
  text-align: left;
  margin-bottom: 15px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #ecf0f1;
}

.info-row:last-child {
  border-bottom: none;
}

.label {
  font-weight: 600;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.value {
  color: #2c3e50;
  font-weight: 500;
}

.favorite-btn {
  width: 100%;
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 25px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.favorite-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
}

.favorite-btn.favorited {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
}

/* Estado Vazio */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.empty-state h3 {
  color: #2c3e50;
  font-size: 1.8rem;
  margin-bottom: 10px;
}

.empty-state p {
  color: #7f8c8d;
  font-size: 1.1rem;
  margin-bottom: 20px;
}

.btn-reset {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-reset:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

/* Responsividade */
@media (max-width: 768px) {
  .controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box {
    width: 100%;
  }
  
  .filter-region {
    width: 100%;
    justify-content: space-between;
  }
  
  .region-select {
    flex: 1;
  }
  
  .header-stats {
    gap: 10px;
  }
  
  .stat-box {
    min-width: 80px;
  }
  
  .country-grid {
    grid-template-columns: 1fr;
  }
  
  .app-header h1 {
    font-size: 2rem;
  }
  
  .flag {
    font-size: 3rem;
  }
}
```

---

## **7. Conceitos-Chave do Módulo**

### **Gerenciamento de Estados Múltiplos**
- Estados independentes para funcionalidades diferentes
- Update funcional para estados que dependem do valor anterior
- Estados derivados calculados na renderização

### **Sincronização Pai-Filho**
- Pai gerencia estados, filhos recebem via props
- Callbacks para modificar estados do pai
- Componentes filhos sem estado local (controlled components)

### **Renderização Condicional**
- `&&` para renderização opcional
- Ternário para alternativas (A ou B)
- Classes CSS condicionais para estilos dinâmicos

### **Filtros Combinados**
- Aplicar múltiplos filtros em sequência
- Manter filtros independentes e combináveis
- UI clara mostrando filtros ativos

---

## **Exercício Prático**

### **Objetivo**
Implementar o sistema completo de gerenciamento de estados com filtros combinados

### **Requisitos**
- [ ] Gerenciar favoritos (adicionar/remover)
- [ ] Implementar busca textual (nome, capital ou região)
- [ ] Criar filtro por região
- [ ] Adicionar toggle para mostrar apenas favoritos
- [ ] Exibir contador dinâmico de países filtrados
- [ ] Mostrar estado vazio quando não houver resultados
- [ ] Implementar botão "Limpar Filtros"
- [ ] Adicionar estatísticas no header (total, favoritos, exibidos)

### **Desafio Bônus**
- [ ] Salvar favoritos no `localStorage`
- [ ] Adicionar animações nas transições
- [ ] Implementar filtro por população (pequeno/médio/grande)
- [ ] Criar modo de visualização lista/grid

### **Dicas**
```jsx
// localStorage para persistência
useEffect(() => {
  const saved = localStorage.getItem('favorites');
  if (saved) setFavorites(JSON.parse(saved));
}, []);

useEffect(() => {
  localStorage.setItem('favorites', JSON.stringify(favorites));
}, [favorites]);

// Regiões únicas do array
const regions = [...new Set(countries.map(c => c.region))];

// Filtros combinados
const filtered = countries
  .filter(c => showFavorites ? favorites.includes(c.id) : true)
  .filter(c => selectedRegion === 'all' ? true : c.region === selectedRegion)
  .filter(c => c.name.toLowerCase().includes(search.toLowerCase()));
```
