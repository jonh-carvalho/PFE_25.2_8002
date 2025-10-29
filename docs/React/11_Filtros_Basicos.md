---
id: 11_Filtros_Basicos
title: 11 - Filtros e Busca na Lista de Países
---

# 11 - Filtros e Busca na Lista de Países

Aplique os conhecimentos de **useState** e **useEffect** para implementar filtros interativos! Vamos adicionar busca por nome e filtro por região na nossa Lista de Países.

---

## Objetivos do Módulo

- Implementar busca em tempo real por nome de país
- Criar filtros por região geográfica
- Combinar múltiplos filtros simultaneamente
- Aplicar lógica de filtragem com array methods
- Gerenciar estados interdependentes

---

## 1. A Aplicação Base

Vamos partir da aplicação funcional do Módulo 10:

```jsx
// src/App.jsx - Base do Módulo 10
import { useState, useEffect } from 'react';

function App() {
  const [countries, setCountries] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadCountries = async () => {
      try {
        const response = await fetch('https://servicodados.ibge.gov.br/api/v1/paises');
        if (!response.ok) throw new Error(`Erro: ${response.status}`);
        
        const data = await response.json();
        
        // Mapear dados do IBGE para formato da aplicação
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
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    loadCountries();
  }, []);

  if (isLoading) return <div>Carregando...</div>;
  if (error) return <div>Erro: {error}</div>;

  return (
    <div>
      <h1>Lista de Países</h1>
      <p>{countries.length} países carregados</p>
    </div>
  );
}
```

**Problema:** Usuário não consegue buscar países específicos ou filtrar por região.

---

## 2. Adicionando Busca por Nome

### 2.1 Estado da Busca

```jsx
// Adicionar estado para busca
const [searchTerm, setSearchTerm] = useState('');
```

### 2.2 Campo de Input

```jsx
// Componente de busca
<div className="search-container">
  <input
    type="text"
    placeholder="Buscar país..."
    value={searchTerm}
    onChange={(e) => setSearchTerm(e.target.value)}
    className="search-input"
  />
  {searchTerm && (
    <button 
      onClick={() => setSearchTerm('')}
      className="clear-btn"
    >
      ✕
    </button>
  )}
</div>
```

### 2.3 Filtragem dos Países

```jsx
// Calcular países filtrados
const filteredCountries = countries.filter(country => {
  const countryName = country.name.toLowerCase();
  const search = searchTerm.toLowerCase();
  return countryName.includes(search);
});
```

### 2.4 App Completo com Busca

```jsx
// src/App.jsx - Com Busca
import { useState, useEffect } from 'react';

function App() {
  const [countries, setCountries] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadCountries = async () => {
      try {
        const response = await fetch('https://servicodados.ibge.gov.br/api/v1/paises');
        if (!response.ok) throw new Error(`Erro: ${response.status}`);
        
        const data = await response.json();
        
        // Mapear dados do IBGE
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
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    loadCountries();
  }, []);

  // Filtrar países pela busca
  const filteredCountries = countries.filter(country => {
    const countryName = country.name.toLowerCase();
    const search = searchTerm.toLowerCase();
    return countryName.includes(search);
  });

  if (isLoading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Carregando países...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error">
        <h2>Erro ao carregar países</h2>
        <p>{error}</p>
        <button onClick={() => window.location.reload()}>
          Tentar Novamente
        </button>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🌍 Lista de Países</h1>
        <p>{countries.length} países disponíveis</p>
      </header>

      <div className="search-container">
        <input
          type="text"
          placeholder="Buscar país..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
        {searchTerm && (
          <button 
            onClick={() => setSearchTerm('')}
            className="clear-btn"
          >
            ✕
          </button>
        )}
      </div>

      <div className="results-info">
        <p>
          {filteredCountries.length === countries.length
            ? `Mostrando todos os ${countries.length} países`
            : `${filteredCountries.length} países encontrados`}
        </p>
      </div>

      <div className="countries-grid">
        {filteredCountries.length > 0 ? (
          filteredCountries.map(country => (
            <div key={country.cca3} className="country-card">
              <img 
                src={country.flag}
                alt={`Bandeira de ${country.name}`}
                className="flag-img"
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = `data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="60" height="45"><rect width="60" height="45" fill="%23ddd"/><text x="50%" y="50%" text-anchor="middle" dy=".3em" font-size="20">${country.name[0]}</text></svg>`;
                }}
              />
              <h3>{country.name}</h3>
              <p>📍 {country.capital}</p>
              <p>🌎 {country.region}</p>
              <p>�️ {country.subregion}</p>
            </div>
          ))
        ) : (
          <div className="empty-state">
            <h3>🔍 Nenhum país encontrado</h3>
            <p>Tente buscar por outro nome</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
```

**Testando:**
- Digite "bra" → Mostra Brasil
- Digite "port" → Mostra Portugal
- Digite "franc" → Mostra França
- Limpe a busca → Mostra todos os países novamente

---

## 3. Adicionando Filtro por Região

### 3.1 Estado da Região

```jsx
const [selectedRegion, setSelectedRegion] = useState('all');
```

### 3.2 Regiões Disponíveis

```jsx
const regions = [
  { value: 'all', label: 'Todas as Regiões' },
  { value: 'Africa', label: 'África' },
  { value: 'Americas', label: 'Américas' },
  { value: 'Asia', label: 'Ásia' },
  { value: 'Europe', label: 'Europa' },
  { value: 'Oceania', label: 'Oceania' },
  { value: 'Antarctic', label: 'Antártida' }
];
```

### 3.3 Filtro Select

```jsx
<div className="filter-container">
  <label htmlFor="region-filter">Filtrar por região:</label>
  <select
    id="region-filter"
    value={selectedRegion}
    onChange={(e) => setSelectedRegion(e.target.value)}
    className="region-select"
  >
    {regions.map(region => (
      <option key={region.value} value={region.value}>
        {region.label}
      </option>
    ))}
  </select>
</div>
```

---

## 4. Combinando Múltiplos Filtros

### 4.1 Lógica de Filtragem Completa

```jsx
// Filtrar por busca E região
const filteredCountries = countries.filter(country => {
  // Filtro de busca
  const matchesSearch = country.name
    .toLowerCase()
    .includes(searchTerm.toLowerCase());
  
  // Filtro de região
  const matchesRegion = selectedRegion === 'all' || 
    country.region === selectedRegion;
  
  // País deve passar por AMBOS os filtros
  return matchesSearch && matchesRegion;
});
```

### 4.2 Informações Detalhadas

```jsx
<div className="filter-info">
  {searchTerm && (
    <span className="filter-tag">
      Busca: "{searchTerm}"
      <button onClick={() => setSearchTerm('')}>✕</button>
    </span>
  )}
  {selectedRegion !== 'all' && (
    <span className="filter-tag">
      Região: {regions.find(r => r.value === selectedRegion)?.label}
      <button onClick={() => setSelectedRegion('all')}>✕</button>
    </span>
  )}
</div>
```

---

## 5. App Completo com Todos os Filtros

```jsx
// src/App.jsx - Versão Final do Módulo 11
import { useState, useEffect } from 'react';
import './App.css';

function App() {
  // Estados principais
  const [countries, setCountries] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRegion, setSelectedRegion] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Carregar países da API
  useEffect(() => {
    const loadCountries = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        const response = await fetch('https://servicodados.ibge.gov.br/api/v1/paises');
        
        if (!response.ok) {
          throw new Error(`Erro HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Mapear dados do IBGE para formato da aplicação
        const mapped = data.map(pais => ({
          cca3: pais.id['ISO-3166-1-ALPHA-3'],
          flag: `https://flagcdn.com/${pais.id['ISO-3166-1-ALPHA-2'].toLowerCase()}.svg`,
          name: pais.nome.abreviado,
          capital: pais.governo?.capital?.nome || 'N/A',
          population: 0,
          region: pais.localizacao.regiao.nome,
          subregion: pais.localizacao['sub-regiao']?.nome || 'N/A',
          area: 0
        }));
        
        setCountries(mapped);
        
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    loadCountries();
  }, []);

  // Regiões disponíveis
  const regions = [
    { value: 'all', label: 'Todas as Regiões' },
    { value: 'Africa', label: 'África' },
    { value: 'Americas', label: 'Américas' },
    { value: 'Asia', label: 'Ásia' },
    { value: 'Europe', label: 'Europa' },
    { value: 'Oceania', label: 'Oceania' },
    { value: 'Antarctic', label: 'Antártida' }
  ];

  // Filtrar países
  const filteredCountries = countries.filter(country => {
    // Filtro de busca
    const matchesSearch = country.name
      .toLowerCase()
      .includes(searchTerm.toLowerCase());
    
    // Filtro de região
    const matchesRegion = selectedRegion === 'all' || 
      country.region === selectedRegion;
    
    return matchesSearch && matchesRegion;
  });

  // Limpar todos os filtros
  const clearAllFilters = () => {
    setSearchTerm('');
    setSelectedRegion('all');
  };

  // Estados de carregamento/erro
  if (isLoading) {
    return (
      <div className="app">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Carregando países...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app">
        <div className="error-container">
          <h2>❌ Erro ao carregar países</h2>
          <p>{error}</p>
          <button onClick={() => window.location.reload()}>
            🔄 Tentar Novamente
          </button>
        </div>
      </div>
    );
  }

  // Verificar se há filtros ativos
  const hasActiveFilters = searchTerm !== '' || selectedRegion !== 'all';

  return (
    <div className="app">
      {/* Cabeçalho */}
      <header className="header">
        <h1>🌍 Lista de Países do Mundo</h1>
        <p className="subtitle">
          {countries.length} países disponíveis para explorar
        </p>
      </header>

      {/* Controles de Filtro */}
      <div className="controls">
        {/* Busca */}
        <div className="search-container">
          <input
            type="text"
            placeholder="Buscar país..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
          {searchTerm && (
            <button 
              onClick={() => setSearchTerm('')}
              className="clear-input-btn"
              title="Limpar busca"
            >
              ✕
            </button>
          )}
        </div>

        {/* Filtro de Região */}
        <div className="filter-container">
          <select
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
            className="region-select"
          >
            {regions.map(region => (
              <option key={region.value} value={region.value}>
                {region.label}
              </option>
            ))}
          </select>
        </div>

        {/* Botão Limpar Filtros */}
        {hasActiveFilters && (
          <button 
            onClick={clearAllFilters}
            className="clear-all-btn"
          >
            🗑️ Limpar Filtros
          </button>
        )}
      </div>

      {/* Filtros Ativos */}
      {hasActiveFilters && (
        <div className="active-filters">
          <span className="filter-label">Filtros ativos:</span>
          {searchTerm && (
            <span className="filter-tag">
              Busca: "{searchTerm}"
              <button onClick={() => setSearchTerm('')}>✕</button>
            </span>
          )}
          {selectedRegion !== 'all' && (
            <span className="filter-tag">
              Região: {regions.find(r => r.value === selectedRegion)?.label}
              <button onClick={() => setSelectedRegion('all')}>✕</button>
            </span>
          )}
        </div>
      )}

      {/* Informações dos Resultados */}
      <div className="results-info">
        {filteredCountries.length === countries.length ? (
          <p>📊 Mostrando todos os <strong>{countries.length}</strong> países</p>
        ) : (
          <p>
            📊 Encontrados <strong>{filteredCountries.length}</strong> de {countries.length} países
          </p>
        )}
      </div>

      {/* Grid de Países */}
      <main className="main-content">
        {filteredCountries.length > 0 ? (
          <div className="countries-grid">
            {filteredCountries.map(country => (
              <div key={country.cca3} className="country-card">
                <div className="flag-container">
                  <img 
                    src={country.flags.png} 
                    alt={`Bandeira de ${country.name.common}`}
                    className="flag-image"
                  />
                </div>
                
                <div className="country-info">
                  <h3 className="country-name">{country.name.common}</h3>
                  
                  <div className="country-details">
                    <p>
                      <span className="icon">📍</span>
                      <strong>Capital:</strong> {country.capital?.[0] || 'N/A'}
                    </p>
                    <p>
                      <span className="icon">🌎</span>
                      <strong>Região:</strong> {country.region}
                    </p>
                    <p>
                      <span className="icon">👥</span>
                      <strong>População:</strong> {country.population.toLocaleString('pt-BR')}
                    </p>
                    <p>
                      <span className="icon">📏</span>
                      <strong>Área:</strong> {country.area.toLocaleString('pt-BR')} km²
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-icon">🔍</div>
            <h3>Nenhum país encontrado</h3>
            <p>
              {searchTerm && selectedRegion !== 'all'
                ? `Não há países na região "${regions.find(r => r.value === selectedRegion)?.label}" que correspondam a "${searchTerm}"`
                : searchTerm
                ? `Não há países que correspondam a "${searchTerm}"`
                : `Não há países na região "${regions.find(r => r.value === selectedRegion)?.label}"`
              }
            </p>
            <button onClick={clearAllFilters} className="reset-btn">
              🔄 Resetar Filtros
            </button>
          </div>
        )}
      </main>

      {/* Rodapé */}
      <footer className="footer">
        <p>
          Dados fornecidos pela <a href="https://servicodados.ibge.gov.br/api/docs/paises" target="_blank" rel="noopener noreferrer">API do IBGE</a>
        </p>
      </footer>
    </div>
  );
}

export default App;
```

---

## 5.5 Favoritos

Queremos permitir que o usuário marque países como favoritos diretamente nos cards. Para manter as coisas simples (conforme solicitado: sem `localStorage`), usaremos um estado local `favorites` e uma função `toggleFavorite`.

Exemplo rápido (adicionar dentro do componente `App`):

```jsx
// Estado de favoritos
const [favorites, setFavorites] = useState([]);

const toggleFavorite = (code) => {
  setFavorites(prev =>
    prev.includes(code) ? prev.filter(c => c !== code) : [...prev, code]
  );
};
```

No JSX de cada card, adicione um botão que chama `toggleFavorite`:

```jsx
<button
  className={`favorite-btn ${favorites.includes(country.cca3) ? 'favorited' : ''}`}
  onClick={() => toggleFavorite(country.cca3)}
  aria-pressed={favorites.includes(country.cca3)}
>
  {favorites.includes(country.cca3) ? '♥ Favorito' : '♡ Favoritar'}
</button>
```

E no cabeçalho podemos mostrar a contagem de favoritos:

```jsx
<div className="header-stats">
  <span>{countries.length} países</span>
  <span>{filteredCountries.length} visíveis</span>
  <span>{favorites.length} favoritos</span>
</div>
```

Observações:
- Não existe persistência: favoritos são mantidos somente em memória e serão perdidos ao recarregar a página.
- A classe `favorite-btn` e a variação `.favorited` já estão definidas em `App.css` (estilos fornecidos no repositório).
- Se quiser, podemos adicionar persistência após (usando `localStorage`) — me avise.

### 5.6 Integrando com CountryCard/CountryGrid

Se você tiver os componentes `CountryGrid` e `CountryCard`, a integração dos favoritos fica assim:

```jsx
import CountryGrid from './components/CountryGrid';

// ... estados e efeitos (countries, filteredCountries, favorites, toggleFavorite)

return (
  <>
    {/* ...header e filtros... */}
    <main>
      {filteredCountries.length > 0 ? (
        <CountryGrid 
          countries={filteredCountries}
          favorites={favorites}
          onToggleFavorite={toggleFavorite}
        />
      ) : (
        <div className="empty-state">Nenhum país encontrado</div>
      )}
    </main>
  </>
);
```

E o `CountryCard` deve receber as props `isFavorite` e `onToggleFavorite(cca3)` para acionar o toggle localmente.

## 6. Estilos CSS

```css
/* src/App.css */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.app {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

/* Header */
.header {
  text-align: center;
  color: white;
  margin-bottom: 30px;
  padding: 30px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
}

/* Controles */
.controls {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  justify-content: center;
}

.search-container {
  position: relative;
  flex: 1;
  min-width: 250px;
  max-width: 500px;
}

.search-input {
  width: 100%;
  padding: 12px 40px 12px 16px;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.search-input:focus {
  outline: none;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.clear-input-btn {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #999;
  padding: 5px 10px;
  transition: color 0.3s ease;
}

.clear-input-btn:hover {
  color: #333;
}

.filter-container {
  min-width: 200px;
}

.region-select {
  width: 100%;
  padding: 12px 16px;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.region-select:focus {
  outline: none;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.clear-all-btn {
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid white;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.clear-all-btn:hover {
  background: white;
  color: #667eea;
}

/* Filtros Ativos */
.active-filters {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
}

.filter-label {
  color: white;
  font-weight: 600;
}

.filter-tag {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: white;
  border-radius: 20px;
  font-size: 0.9rem;
}

.filter-tag button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  color: #999;
  padding: 0 4px;
  transition: color 0.3s ease;
}

.filter-tag button:hover {
  color: #e74c3c;
}

/* Informações dos Resultados */
.results-info {
  text-align: center;
  color: white;
  margin-bottom: 20px;
  font-size: 1.1rem;
}

/* Grid de Países */
.countries-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
  margin-bottom: 40px;
}

.country-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.country-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
}

.flag-container {
  height: 180px;
  overflow: hidden;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.flag-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.country-info {
  padding: 20px;
}

.country-name {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #2c3e50;
  text-align: center;
}

.country-details {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.country-details p {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #34495e;
  font-size: 0.95rem;
}

.icon {
  font-size: 1.2rem;
}

/* Estados Vazios e de Erro */
.empty-state, .loading-container, .error-container {
  text-align: center;
  padding: 60px 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  color: white;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.empty-state h3, .error-container h2 {
  font-size: 1.8rem;
  margin-bottom: 15px;
}

.empty-state p, .error-container p {
  font-size: 1.1rem;
  margin-bottom: 25px;
  opacity: 0.9;
}

.reset-btn {
  padding: 12px 30px;
  background: white;
  color: #667eea;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.reset-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

/* Loading */
.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Footer */
.footer {
  text-align: center;
  padding: 30px;
  color: white;
  margin-top: 40px;
}

.footer a {
  color: white;
  text-decoration: underline;
}

/* Responsividade */
@media (max-width: 768px) {
  .header h1 {
    font-size: 1.8rem;
  }
  
  .controls {
    flex-direction: column;
  }
  
  .search-container, .filter-container {
    max-width: 100%;
  }
  
  .countries-grid {
    grid-template-columns: 1fr;
  }
}
```

---

## 7. Testando os Filtros

### 7.1 Teste: Busca Simples

```
1. Digite "bra" → Veja Brasil, Brazil
2. Digite "united" → Veja United States, United Kingdom, United Arab Emirates
3. Limpe o campo → Todos os países voltam
```

### 7.2 Teste: Filtro por Região

```
1. Selecione "Europa" → Apenas países europeus
2. Selecione "Ásia" → Apenas países asiáticos
3. Selecione "Todas as Regiões" → Todos voltam
```

### 7.3 Teste: Filtros Combinados

```
1. Digite "port" + Selecione "Europa" → Portugal
2. Digite "ara" + Selecione "Ásia" → Arábia Saudita, Emirados Árabes
3. Digite "rep" + Selecione "África" → República Centro-Africana, República Democrática do Congo, etc.
```

---

## 8. Análise dos Array Methods

### 8.1 filter() - Nosso Herói

```jsx
// Sintaxe básica
const result = array.filter(item => condition);

// No nosso código
const filteredCountries = countries.filter(country => {
  const matchesSearch = country.name.common
    .toLowerCase()
    .includes(searchTerm.toLowerCase());
  
  const matchesRegion = selectedRegion === 'all' || 
    country.region === selectedRegion;
  
  return matchesSearch && matchesRegion;
});
```

**Como funciona:**
1. Percorre cada país do array `countries`
2. Testa se o país passa nas condições
3. Se `true`, inclui no resultado
4. Se `false`, ignora o país
5. Retorna novo array com países aprovados

### 8.2 includes() - Busca Parcial

```jsx
// Exemplo
'Brasil'.toLowerCase().includes('bra')  // true
'França'.toLowerCase().includes('bra')  // false

// No código
country.name.toLowerCase().includes(searchTerm.toLowerCase())
```

### 8.3 find() - Encontrar Região

```jsx
const regionLabel = regions.find(r => r.value === selectedRegion)?.label;

// Exemplo:
// selectedRegion = 'Europe'
// Retorna: { value: 'Europe', label: 'Europa' }
// Acessa: .label → 'Europa'
```

---

## 9. Comparação: Antes vs Depois

| Aspecto | Módulo 10 | Módulo 11 |
|---------|-----------|-----------|
| Busca | ❌ Não tinha | ✅ Busca por nome |
| Filtro Região | ❌ Não tinha | ✅ 6 regiões |
| Filtros Combinados | ❌ Não tinha | ✅ Busca + Região |
| Feedback Visual | ❌ Básico | ✅ Tags de filtros ativos |
| Estado Vazio | ❌ Simples | ✅ Mensagens específicas |

---

## 10. Exercícios Práticos

### Exercício 1: Buscar por Capital

Modifique o filtro para buscar também por capital:

```jsx
const matchesSearch = 
  country.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
  country.capital.toLowerCase().includes(searchTerm.toLowerCase());
```

**Teste:** Digite "brasília" e veja o Brasil aparecer.

### Exercício 2: Contador de Países por Região

```jsx
const countByRegion = {};
countries.forEach(country => {
  countByRegion[country.region] = (countByRegion[country.region] || 0) + 1;
});

// Exibir: "Europa (47 países)"
```

### Exercício 3: Filtro por Sub-região

Adicione um terceiro filtro para sub-regiões:

```jsx
const [selectedSubregion, setSelectedSubregion] = useState('all');

// Obter sub-regiões únicas
const subregions = ['all', ...new Set(countries.map(c => c.subregion))];

// Adicionar ao filtro
const matchesSubregion = selectedSubregion === 'all' || 
  country.subregion === selectedSubregion;
```

**Teste:** Filtre por "Americas" → depois por "South America" para ver apenas países da América do Sul.