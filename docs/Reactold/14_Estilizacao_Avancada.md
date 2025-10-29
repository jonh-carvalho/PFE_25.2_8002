# 14 - **Estilização Avançada em React**

Agora que dominamos os fundamentos do React, chegou o momento de elevar nossa **Lista de Países** a um nível profissional! Neste módulo, exploraremos técnicas avançadas de estilização que tornarão nosso projeto visualmente impressionante e tecnicamente robusto.

---

## **Objetivos do Módulo**
- Dominar CSS-in-JS e CSS Modules em projetos reais
- Implementar sistema de temas dinâmicos (claro/escuro)
- Criar componentes estilizados reutilizáveis
- Otimizar performance de estilos em aplicações React
- Desenvolver um sistema de design consistente

---

## **🎨 Quando Usar Cada Abordagem de Estilização**

### **📊 Matriz de Decisão**

| **Cenário** | **CSS Tradicional** | **CSS Modules** | **Styled Components** |
|-------------|---------------------|-----------------|----------------------|
| **Projeto Simples** | ✅ Ideal | ⚡ Opcional | ❌ Excessivo |
| **Projeto Médio** | ⚠️ Limitado | ✅ Recomendado | ⚡ Considerar |
| **Projeto Complexo** | ❌ Inadequado | ⚡ Considerar | ✅ Ideal |
| **Temas Dinâmicos** | ❌ Difícil | ⚠️ Limitado | ✅ Perfeito |
| **Estilos Condicionais** | ⚠️ Verboso | ⚡ Médio | ✅ Elegante |
| **Performance Crítica** | ✅ Ótima | ✅ Boa | ⚠️ Considerar |

### **🔧 CSS Tradicional com Classes**
```css
/* ✅ Use quando: Projeto simples, performance crítica */
.country-card {
  padding: 20px;
  border-radius: 8px;
  transition: transform 0.2s;
}

.country-card--favorite {
  border: 2px solid #e74c3c;
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.2);
}
```

### **🧩 CSS Modules**
```css
/* styles.module.css */
/* ✅ Use quando: Quer escopo local sem JavaScript */
.card {
  padding: 20px;
  border-radius: 8px;
  background: white;
}

.cardFavorite {
  composes: card;
  border: 2px solid #e74c3c;
}
```

### **⚡ CSS-in-JS (Styled Components)**
```jsx
/* ✅ Use quando: Estilos dinâmicos e temas complexos */
const CountryCard = styled.div`
  padding: 20px;
  border-radius: 8px;
  background: ${props => props.theme.cardBackground};
  border: 2px solid ${props => 
    props.isFavorite ? props.theme.favoriteColor : 'transparent'
  };
  
  transform: translateY(${props => props.isHovered ? '-4px' : '0'});
  transition: all 0.3s ease;
`;
```

---

## **🌟 Implementando Sistema de Temas com Styled Components**

### **1. Configuração Base**

```bash
# Instalar dependências
npm install styled-components
npm install --save-dev @types/styled-components
```

### **2. Criando o Sistema de Temas**

```jsx
// src/theme/themes.js
export const lightTheme = {
  name: 'light',
  colors: {
    primary: '#667eea',
    secondary: '#764ba2',
    background: '#ffffff',
    surface: '#f8f9fa',
    text: '#2c3e50',
    textSecondary: '#7f8c8d',
    border: '#e1e8ed',
    favorite: '#e74c3c',
    success: '#27ae60',
    warning: '#f39c12',
    error: '#e74c3c'
  },
  shadows: {
    small: '0 2px 4px rgba(0,0,0,0.1)',
    medium: '0 4px 6px rgba(0,0,0,0.07)',
    large: '0 10px 15px rgba(0,0,0,0.1)'
  },
  borderRadius: {
    small: '4px',
    medium: '8px',
    large: '12px',
    xlarge: '16px'
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    xxl: '48px'
  }
};

export const darkTheme = {
  ...lightTheme,
  name: 'dark',
  colors: {
    ...lightTheme.colors,
    primary: '#4c6ef5',
    secondary: '#9775fa',
    background: '#1a1a1a',
    surface: '#2d2d2d',
    text: '#ffffff',
    textSecondary: '#a0a0a0',
    border: '#404040',
    favorite: '#ff6b6b'
  }
};
```

### **3. Provider de Tema**

```jsx
// src/theme/ThemeProvider.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { ThemeProvider as StyledThemeProvider } from 'styled-components';
import { lightTheme, darkTheme } from './themes';

const ThemeContext = createContext();

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme deve ser usado dentro de ThemeProvider');
  }
  return context;
};

export const ThemeProvider = ({ children }) => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Carregar preferência do localStorage
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme) {
      setIsDarkMode(savedTheme === 'dark');
    } else {
      setIsDarkMode(prefersDark);
    }
  }, []);

  // Salvar preferência
  useEffect(() => {
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', isDarkMode ? 'dark' : 'light');
  }, [isDarkMode]);

  const toggleTheme = () => setIsDarkMode(prev => !prev);
  const currentTheme = isDarkMode ? darkTheme : lightTheme;

  const value = {
    theme: currentTheme,
    isDarkMode,
    toggleTheme
  };

  return (
    <ThemeContext.Provider value={value}>
      <StyledThemeProvider theme={currentTheme}>
        {children}
      </StyledThemeProvider>
    </ThemeContext.Provider>
  );
};
```

### **4. Estilos Globais**

```jsx
// src/theme/GlobalStyles.js
import { createGlobalStyle } from 'styled-components';

export const GlobalStyles = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
    background-color: ${props => props.theme.colors.background};
    color: ${props => props.theme.colors.text};
    transition: background-color 0.3s ease, color 0.3s ease;
    line-height: 1.6;
  }

  button {
    font-family: inherit;
    cursor: pointer;
    border: none;
    outline: none;
    transition: all 0.2s ease;
  }

  input, select {
    font-family: inherit;
    outline: none;
    transition: all 0.2s ease;
  }

  a {
    color: ${props => props.theme.colors.primary};
    text-decoration: none;
    transition: color 0.2s ease;

    &:hover {
      color: ${props => props.theme.colors.secondary};
    }
  }

  ::-webkit-scrollbar {
    width: 8px;
  }

  ::-webkit-scrollbar-track {
    background: ${props => props.theme.colors.surface};
  }

  ::-webkit-scrollbar-thumb {
    background: ${props => props.theme.colors.border};
    border-radius: 4px;
  }

  ::-webkit-scrollbar-thumb:hover {
    background: ${props => props.theme.colors.textSecondary};
  }
`;
```

---

## **🎭 Componentes Estilizados para Lista de Países**

### **1. Container Principal**

```jsx
// src/components/styled/Containers.js
import styled from 'styled-components';

export const AppContainer = styled.div`
  max-width: 1400px;
  margin: 0 auto;
  padding: ${props => props.theme.spacing.lg};
  min-height: 100vh;
  
  @media (max-width: 768px) {
    padding: ${props => props.theme.spacing.md};
  }
`;

export const Header = styled.header`
  text-align: center;
  margin-bottom: ${props => props.theme.spacing.xxl};
  padding: ${props => props.theme.spacing.xl};
  background: linear-gradient(
    135deg, 
    ${props => props.theme.colors.primary} 0%, 
    ${props => props.theme.colors.secondary} 100%
  );
  border-radius: ${props => props.theme.borderRadius.xlarge};
  box-shadow: ${props => props.theme.shadows.large};
  color: white;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.1);
    transform: skewY(-2deg);
    transform-origin: top left;
  }

  > * {
    position: relative;
    z-index: 1;
  }
`;

export const Title = styled.h1`
  font-size: clamp(2rem, 5vw, 3.5rem);
  margin-bottom: ${props => props.theme.spacing.md};
  font-weight: 700;
  letter-spacing: -0.02em;
`;

export const Subtitle = styled.p`
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: ${props => props.theme.spacing.lg};
`;
```

### **2. Cartão de País Avançado**

```jsx
// src/components/styled/CountryCard.js
import styled, { css } from 'styled-components';

export const CardContainer = styled.div`
  background: ${props => props.theme.colors.surface};
  border-radius: ${props => props.theme.borderRadius.large};
  box-shadow: ${props => props.theme.shadows.medium};
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  position: relative;

  &:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: ${props => props.theme.shadows.large};
  }

  ${props => props.isFavorite && css`
    border: 2px solid ${props.theme.colors.favorite};
    box-shadow: 0 8px 25px ${props.theme.colors.favorite}20;
  `}
`;

export const FlagSection = styled.div`
  height: 120px;
  background: linear-gradient(
    135deg, 
    ${props => props.theme.colors.primary}20,
    ${props => props.theme.colors.secondary}20
  );
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
    transform: translateX(-100%);
    transition: transform 0.6s;
  }

  ${CardContainer}:hover &::before {
    transform: translateX(100%);
  }
`;

export const FlagImage = styled.img`
  width: 80px;
  height: auto;
  border-radius: ${props => props.theme.borderRadius.medium};
  box-shadow: ${props => props.theme.shadows.medium};
  transition: transform 0.3s ease;

  ${CardContainer}:hover & {
    transform: scale(1.1);
  }
`;

export const FlagEmoji = styled.span`
  position: absolute;
  top: ${props => props.theme.spacing.md};
  right: ${props => props.theme.spacing.md};
  font-size: 2rem;
  filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
`;

export const CardContent = styled.div`
  padding: ${props => props.theme.spacing.lg};
`;

export const CountryName = styled.h2`
  font-size: 1.5rem;
  font-weight: 700;
  color: ${props => props.theme.colors.text};
  margin-bottom: ${props => props.theme.spacing.md};
  text-align: center;
`;

export const InfoGrid = styled.div`
  display: grid;
  gap: ${props => props.theme.spacing.sm};
  margin-bottom: ${props => props.theme.spacing.lg};
`;

export const InfoRow = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: ${props => props.theme.spacing.sm} 0;
  border-bottom: 1px solid ${props => props.theme.colors.border};

  &:last-child {
    border-bottom: none;
  }
`;

export const InfoLabel = styled.span`
  font-weight: 600;
  color: ${props => props.theme.colors.textSecondary};
  font-size: 0.9rem;
`;

export const InfoValue = styled.span`
  color: ${props => props.theme.colors.text};
  text-align: right;
  max-width: 60%;
  word-wrap: break-word;
  font-weight: 500;
`;
```

### **3. Botões e Controles**

```jsx
// src/components/styled/Buttons.js
import styled, { css } from 'styled-components';

const BaseButton = styled.button`
  padding: ${props => props.theme.spacing.sm} ${props => props.theme.spacing.md};
  border-radius: ${props => props.theme.borderRadius.medium};
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: ${props => props.theme.spacing.sm};
  position: relative;
  overflow: hidden;

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s;
  }

  &:hover:not(:disabled)::before {
    left: 100%;
  }
`;

export const PrimaryButton = styled(BaseButton)`
  background: linear-gradient(
    135deg, 
    ${props => props.theme.colors.primary}, 
    ${props => props.theme.colors.secondary}
  );
  color: white;
  border: none;

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: ${props => props.theme.shadows.medium};
  }
`;

export const FavoriteButton = styled(BaseButton)`
  ${props => props.isFavorite ? css`
    background: linear-gradient(135deg, ${props.theme.colors.favorite}, #c0392b);
    color: white;
  ` : css`
    background: ${props.theme.colors.surface};
    color: ${props.theme.colors.textSecondary};
    border: 2px solid ${props.theme.colors.border};
  `}

  &:hover:not(:disabled) {
    ${props => props.isFavorite ? css`
      background: linear-gradient(135deg, #c0392b, #a93226);
    ` : css`
      border-color: ${props.theme.colors.favorite};
      color: ${props.theme.colors.favorite};
    `}
  }
`;

export const ThemeToggleButton = styled(BaseButton)`
  background: ${props => props.theme.colors.surface};
  color: ${props => props.theme.colors.text};
  border: 2px solid ${props => props.theme.colors.border};
  border-radius: 50%;
  width: 48px;
  height: 48px;
  padding: 0;
  position: fixed;
  bottom: ${props => props.theme.spacing.lg};
  right: ${props => props.theme.spacing.lg};
  z-index: 1000;
  font-size: 1.2rem;

  &:hover {
    transform: scale(1.1) rotate(180deg);
    border-color: ${props => props.theme.colors.primary};
  }
`;
```

---

## **🔍 Filtros e Busca Estilizados**

```jsx
// src/components/styled/SearchComponents.js
import styled from 'styled-components';

export const SearchContainer = styled.div`
  background: ${props => props.theme.colors.surface};
  border-radius: ${props => props.theme.borderRadius.large};
  padding: ${props => props.theme.spacing.lg};
  margin-bottom: ${props => props.theme.spacing.xl};
  box-shadow: ${props => props.theme.shadows.medium};
`;

export const SearchInputWrapper = styled.div`
  position: relative;
  margin-bottom: ${props => props.theme.spacing.lg};
`;

export const SearchInput = styled.input`
  width: 100%;
  padding: ${props => props.theme.spacing.md} ${props => props.theme.spacing.md} ${props => props.theme.spacing.md} 48px;
  border: 2px solid ${props => props.theme.colors.border};
  border-radius: ${props => props.theme.borderRadius.xlarge};
  background: ${props => props.theme.colors.background};
  color: ${props => props.theme.colors.text};
  font-size: 1.1rem;
  transition: all 0.3s ease;

  &::placeholder {
    color: ${props => props.theme.colors.textSecondary};
  }

  &:focus {
    border-color: ${props => props.theme.colors.primary};
    box-shadow: 0 0 0 3px ${props => props.theme.colors.primary}20;
  }
`;

export const SearchIcon = styled.span`
  position: absolute;
  left: ${props => props.theme.spacing.md};
  top: 50%;
  transform: translateY(-50%);
  color: ${props => props.theme.colors.textSecondary};
  font-size: 1.2rem;
`;

export const FiltersRow = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: ${props => props.theme.spacing.md};
  align-items: center;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

export const FilterSelect = styled.select`
  padding: ${props => props.theme.spacing.sm} ${props => props.theme.spacing.md};
  border: 2px solid ${props => props.theme.colors.border};
  border-radius: ${props => props.theme.borderRadius.medium};
  background: ${props => props.theme.colors.background};
  color: ${props => props.theme.colors.text};
  font-size: 1rem;
  min-width: 150px;

  &:focus {
    border-color: ${props => props.theme.colors.primary};
    box-shadow: 0 0 0 3px ${props => props.theme.colors.primary}20;
  }
`;
```

---

## **🎯 App Principal com Temas**

```jsx
// src/App.jsx - Versão com Styled Components
import React, { useState, useEffect } from 'react';
import { ThemeProvider } from './theme/ThemeProvider';
import { GlobalStyles } from './theme/GlobalStyles';
import { useTheme } from './theme/ThemeProvider';
import useCountries from './hooks/useCountries';
import useCountrySearch from './hooks/useCountrySearch';

// Componentes estilizados
import {
  AppContainer,
  Header,
  Title,
  Subtitle
} from './components/styled/Containers';

import {
  ThemeToggleButton
} from './components/styled/Buttons';

import {
  SearchContainer,
  SearchInputWrapper,
  SearchInput,
  SearchIcon,
  FiltersRow,
  FilterSelect
} from './components/styled/SearchComponents';

import StyledCountryCard from './components/StyledCountryCard';
import CountriesGrid from './components/CountriesGrid';
import Loading from './components/Loading';
import ErrorMessage from './components/ErrorMessage';

function AppContent() {
  const { theme, isDarkMode, toggleTheme } = useTheme();
  const { countries, isLoading, error, refetch } = useCountries();
  const [favorites, setFavorites] = useState([]);
  
  const {
    searchTerm,
    selectedRegion,
    setSearchTerm,
    setSelectedRegion,
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

  const toggleFavorite = (countryCode) => {
    setFavorites(prev => 
      prev.includes(countryCode)
        ? prev.filter(code => code !== countryCode)
        : [...prev, countryCode]
    );
  };

  if (isLoading) {
    return <Loading message="Carregando países do mundo..." />;
  }

  if (error) {
    return (
      <ErrorMessage 
        title="Erro ao Carregar Países"
        message={error}
        onRetry={refetch}
      />
    );
  }

  return (
    <AppContainer>
      <Header>
        <Title>🌍 Explorador de Países</Title>
        <Subtitle>
          Descubra informações sobre todos os {countries.length} países do mundo
        </Subtitle>
        
        <div style={{ 
          display: 'flex', 
          gap: theme.spacing.lg, 
          justifyContent: 'center',
          marginTop: theme.spacing.lg 
        }}>
          <span>📊 {filteredCountries.length} países exibidos</span>
          <span>❤️ {favorites.length} favoritos</span>
          <span>🎨 Tema {isDarkMode ? 'Escuro' : 'Claro'}</span>
        </div>
      </Header>

      <SearchContainer>
        <SearchInputWrapper>
          <SearchIcon>🔍</SearchIcon>
          <SearchInput
            type="text"
            placeholder="Buscar por país, capital, região ou idioma..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </SearchInputWrapper>

        <FiltersRow>
          <div>
            <label style={{ 
              display: 'block', 
              marginBottom: theme.spacing.sm,
              color: theme.colors.textSecondary,
              fontWeight: 600
            }}>
              🌍 Região:
            </label>
            <FilterSelect 
              value={selectedRegion} 
              onChange={(e) => setSelectedRegion(e.target.value)}
            >
              <option value="all">Todas as regiões</option>
              {searchStats.regions.map(region => (
                <option key={region} value={region}>{region}</option>
              ))}
            </FilterSelect>
          </div>

          {(searchTerm || selectedRegion !== 'all') && (
            <PrimaryButton onClick={clearAllFilters}>
              🗑️ Limpar Filtros
            </PrimaryButton>
          )}
        </FiltersRow>

        <div style={{ 
          textAlign: 'center', 
          marginTop: theme.spacing.md,
          color: theme.colors.textSecondary 
        }}>
          <span>
            População total: {new Intl.NumberFormat('pt-BR').format(searchStats.totalPopulation)}
          </span>
        </div>
      </SearchContainer>

      <CountriesGrid>
        {filteredCountries.map(country => (
          <StyledCountryCard
            key={country.cca3}
            country={country}
            isFavorite={favorites.includes(country.cca3)}
            onToggleFavorite={toggleFavorite}
          />
        ))}
      </CountriesGrid>

      <ThemeToggleButton 
        onClick={toggleTheme}
        title={`Mudar para tema ${isDarkMode ? 'claro' : 'escuro'}`}
      >
        {isDarkMode ? '☀️' : '🌙'}
      </ThemeToggleButton>
    </AppContainer>
  );
}

function App() {
  return (
    <ThemeProvider>
      <GlobalStyles />
      <AppContent />
    </ThemeProvider>
  );
}

export default App;
```

---

## **📱 Responsividade Avançada**

```jsx
// src/utils/breakpoints.js
export const breakpoints = {
  xs: '320px',
  sm: '576px',
  md: '768px',
  lg: '992px',
  xl: '1200px',
  xxl: '1400px'
};

export const media = {
  xs: `@media (min-width: ${breakpoints.xs})`,
  sm: `@media (min-width: ${breakpoints.sm})`,
  md: `@media (min-width: ${breakpoints.md})`,
  lg: `@media (min-width: ${breakpoints.lg})`,
  xl: `@media (min-width: ${breakpoints.xl})`,
  xxl: `@media (min-width: ${breakpoints.xxl})`
};

// Uso nos componentes
export const ResponsiveGrid = styled.div`
  display: grid;
  gap: ${props => props.theme.spacing.lg};
  
  grid-template-columns: 1fr;
  
  ${media.sm} {
    grid-template-columns: repeat(2, 1fr);
  }
  
  ${media.md} {
    grid-template-columns: repeat(3, 1fr);
  }
  
  ${media.xl} {
    grid-template-columns: repeat(4, 1fr);
  }
`;
```

---

## **⚡ Otimização de Performance**

### **1. Componentes com Lazy Loading**

```jsx
// src/components/LazyCountryCard.jsx
import React, { lazy, Suspense } from 'react';
import styled from 'styled-components';

const StyledCountryCard = lazy(() => import('./StyledCountryCard'));

const CardSkeleton = styled.div`
  height: 300px;
  background: ${props => props.theme.colors.surface};
  border-radius: ${props => props.theme.borderRadius.large};
  animation: pulse 1.5s ease-in-out infinite alternate;

  @keyframes pulse {
    0% { opacity: 1; }
    100% { opacity: 0.4; }
  }
`;

function LazyCountryCard(props) {
  return (
    <Suspense fallback={<CardSkeleton />}>
      <StyledCountryCard {...props} />
    </Suspense>
  );
}

export default LazyCountryCard;
```

### **2. Memoização de Estilos**

```jsx
// src/hooks/useThemeStyles.js
import { useMemo } from 'react';
import { useTheme } from '../theme/ThemeProvider';

export const useThemeStyles = () => {
  const { theme } = useTheme();
  
  return useMemo(() => ({
    cardShadow: theme.shadows.medium,
    primaryGradient: `linear-gradient(135deg, ${theme.colors.primary}, ${theme.colors.secondary})`,
    borderRadius: theme.borderRadius.large,
    spacing: theme.spacing
  }), [theme]);
};
```

---

## **📝 Exercício Prático**

### 🎯 **Objetivo**
Implementar sistema completo de temas na Lista de Países

### 📋 **Requisitos**
- [ ] Configurar Styled Components e ThemeProvider
- [ ] Criar temas claro e escuro completos
- [ ] Implementar toggle de tema com persistência
- [ ] Estilizar todos os componentes com tema dinâmico
- [ ] Adicionar animações e transições suaves
- [ ] Garantir responsividade em todos os dispositivos
- [ ] Otimizar performance com lazy loading

### 🚀 **Bonus**
- [ ] Implementar tema automático baseado no sistema
- [ ] Criar tema de alto contraste para acessibilidade
- [ ] Adicionar suporte a múltiplas paletas de cores
- [ ] Implementar animações avançadas com Framer Motion

---

## **🎓 Comparação: Antes vs Depois**

### **❌ Antes (CSS Tradicional)**
```css
/* Muitos arquivos CSS */
/* Classes globais conflitantes */
/* Sem suporte a temas */
/* Difícil manutenção */
.country-card {
  /* Estilos estáticos */
}
```

### **✅ Depois (Styled Components + Temas)**
```jsx
const CountryCard = styled.div`
  /* Estilos dinâmicos */
  background: ${props => props.theme.colors.surface};
  color: ${props => props.theme.colors.text};
  border: 2px solid ${props => 
    props.isFavorite ? props.theme.colors.favorite : 'transparent'
  };
  /* Temas automáticos */
  /* Manutenção simplificada */
`;
```

---

## **🔮 Próximos Passos Avançados**

Depois de dominar este módulo, você estará preparado para:

1. **Framer Motion**: Animações complexas e interações
2. **React Spring**: Animações baseadas em física
3. **Sistemas de Design**: Design tokens e componentes reutilizáveis
4. **Micro-interactions**: Feedbacks visuais sofisticados
5. **PWA Styling**: Estilos para aplicações offline

---

## **📚 Resumo do Módulo**

- ✅ **CSS-in-JS Avançado**: Styled Components com temas dinâmicos
- ✅ **Sistema de Design**: Paletas, espaçamentos e componentes consistentes
- ✅ **Temas Completos**: Claro/escuro com persistência automática
- ✅ **Performance**: Lazy loading e memoização de estilos
- ✅ **Responsividade**: Breakpoints profissionais e grid system
- ✅ **UX Premium**: Animações, transições e micro-interactions

**Agora sua Lista de Países tem qualidade visual profissional!** 🎨✨