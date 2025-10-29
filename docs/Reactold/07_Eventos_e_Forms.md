---
id: 07_Eventos_e_Forms
title: 07 - Eventos e Formulários
---

# 07 - **Eventos e Formulários**

## Introdução

**Eventos** e **formulários** são fundamentais para criar interfaces interativas. Neste módulo, aprenderemos como capturar eventos do usuário, processar entradas de formulários e validar dados, combinando useState com manipulação de eventos.

### O que são Eventos no React?

- **Definição**: Ações do usuário que desencadeiam funções (cliques, digitação, envio)
- **SyntheticEvents**: React usa eventos sintéticos que funcionam igual em todos os navegadores
- **Event Handlers**: Funções que respondem aos eventos
- **Prevenção**: Como prevenir comportamentos padrão do navegador

### Principais Eventos no React

- **onClick**: Clique em elementos
- **onChange**: Mudança em inputs
- **onSubmit**: Envio de formulários
- **onFocus/onBlur**: Foco e desfoque
- **onMouseEnter/onMouseLeave**: Mouse sobre elementos

### Sintaxe Básica de Eventos

```jsx
function MeuComponente() {
  const handleClick = () => {
    console.log('Botão clicado!');
  };

  const handleInputChange = (event) => {
    console.log('Valor digitado:', event.target.value);
  };

  return (
    <div>
      <button onClick={handleClick}>Clique aqui</button>
      <input onChange={handleInputChange} placeholder="Digite algo" />
    </div>
  );
}
```

### Formulários Controlados vs Não Controlados

**Formulário Controlado**: React controla o valor do input via state

```jsx
import { useState } from 'react';

function FormularioControlado() {
  const [nome, setNome] = useState('');

  return (
    <input 
      value={nome}
      onChange={(e) => setNome(e.target.value)}
    />
  );
}
```

**Formulário Não Controlado**: DOM controla o valor (menos recomendado)

```jsx
import { useRef } from 'react';

function FormularioNaoControlado() {
  const inputRef = useRef();

  const handleSubmit = () => {
    console.log(inputRef.current.value);
  };

  return <input ref={inputRef} />;
}
```

## Evoluindo o Projeto: Adicionando Formulário de Países

Vamos expandir nosso projeto "Lista de Países" adicionando um formulário para cadastrar novos países.

### 1. Componente AddCountryForm

```jsx
// src/components/AddCountryForm.jsx
import { useState } from 'react';

function AddCountryForm({ onAddCountry }) {
  const [formData, setFormData] = useState({
    name: '',
    capital: '',
    population: '',
    language: '',
    flag: ''
  });

  const [errors, setErrors] = useState({});

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });

    // Limpar erro quando usuário começar a digitar
    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: ''
      });
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Nome é obrigatório';
    }

    if (!formData.capital.trim()) {
      newErrors.capital = 'Capital é obrigatória';
    }

    if (!formData.population.trim()) {
      newErrors.population = 'População é obrigatória';
    }

    if (!formData.language.trim()) {
      newErrors.language = 'Idioma é obrigatório';
    }

    if (!formData.flag.trim()) {
      newErrors.flag = 'Emoji da bandeira é obrigatório';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (validateForm()) {
      onAddCountry({
        id: Date.now(), // ID simples para demonstração
        flag: formData.flag,
        name: formData.name,
        capital: formData.capital,
        population: formData.population,
        language: formData.language
      });

      // Limpar formulário após envio
      setFormData({
        name: '',
        capital: '',
        population: '',
        language: '',
        flag: ''
      });

      alert('País adicionado com sucesso!');
    }
  };

  return (
    <form className="add-country-form" onSubmit={handleSubmit}>
      <h2>Adicionar Novo País</h2>
      
      <div className="form-group">
        <label htmlFor="flag">Bandeira (emoji):</label>
        <input
          type="text"
          id="flag"
          name="flag"
          value={formData.flag}
          onChange={handleInputChange}
          placeholder="🇧🇷"
          maxLength="2"
        />
        {errors.flag && <span className="error">{errors.flag}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="name">Nome do País:</label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleInputChange}
          placeholder="Brasil"
        />
        {errors.name && <span className="error">{errors.name}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="capital">Capital:</label>
        <input
          type="text"
          id="capital"
          name="capital"
          value={formData.capital}
          onChange={handleInputChange}
          placeholder="Brasília"
        />
        {errors.capital && <span className="error">{errors.capital}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="population">População:</label>
        <input
          type="text"
          id="population"
          name="population"
          value={formData.population}
          onChange={handleInputChange}
          placeholder="215 milhões"
        />
        {errors.population && <span className="error">{errors.population}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="language">Idioma:</label>
        <input
          type="text"
          id="language"
          name="language"
          value={formData.language}
          onChange={handleInputChange}
          placeholder="Português"
        />
        {errors.language && <span className="error">{errors.language}</span>}
      </div>

      <button type="submit" className="submit-btn">
        Adicionar País
      </button>
    </form>
  );
}

export default AddCountryForm;
```

### 2. App.jsx Atualizado com Formulário

```jsx
// src/App.jsx
import { useState } from 'react';
import Header from './components/Header';
import CountryGrid from './components/CountryGrid';
import AddCountryForm from './components/AddCountryForm';
import './App.css';

function App() {
  const [countries, setCountries] = useState([
    { id: 1, flag: "🇧🇷", name: "Brasil", capital: "Brasília", population: "215 milhões", language: "Português" },
    { id: 2, flag: "🇦🇷", name: "Argentina", capital: "Buenos Aires", population: "45 milhões", language: "Espanhol" },
    { id: 3, flag: "🇨🇱", name: "Chile", capital: "Santiago", population: "19 milhões", language: "Espanhol" }
  ]);

  const [showForm, setShowForm] = useState(false);
  const [favoriteCount, setFavoriteCount] = useState(0);

  const addCountry = (newCountry) => {
    setCountries([...countries, newCountry]);
  };

  const toggleForm = () => {
    setShowForm(!showForm);
  };

  return (
    <div className="app">
      <Header 
        title="🌍 Lista de Países da América do Sul"
        subtitle="Explore e adicione países sul-americanos"
        favoriteCount={favoriteCount}
      />
      
      <div className="controls">
        <button 
          className="toggle-form-btn"
          onClick={toggleForm}
        >
          {showForm ? 'Ocultar Formulário' : 'Adicionar País'}
        </button>
      </div>

      {showForm && (
        <AddCountryForm onAddCountry={addCountry} />
      )}

      <CountryGrid 
        countries={countries}
        onFavoriteChange={setFavoriteCount}
      />
    </div>
  );
}

export default App;
```

### 3. CSS para Formulários

```css
/* App.css - Adições para formulários */

.add-country-form {
  background: white;
  border-radius: 15px;
  padding: 30px;
  margin: 30px 0;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  border: 2px solid #e1e8ed;
}

.add-country-form h2 {
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 5px rgba(52, 152, 219, 0.3);
}

.form-group input.error {
  border-color: #e74c3c;
}

.error {
  color: #e74c3c;
  font-size: 14px;
  margin-top: 5px;
  display: block;
}

.submit-btn {
  background: #27ae60;
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  width: 100%;
  transition: background 0.3s ease;
}

.submit-btn:hover {
  background: #219a52;
}

.toggle-form-btn {
  background: #9b59b6;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.toggle-form-btn:hover {
  background: #8e44ad;
  transform: translateY(-2px);
}
```

## Conceitos Importantes de Eventos e Formulários

### 1. **Prevenção de Comportamento Padrão**
```jsx
const handleSubmit = (e) => {
  e.preventDefault(); // Impede reload da página
  // Processar dados do formulário
};
```

### 2. **Captura de Dados do Evento**
```jsx
const handleChange = (e) => {
  const { name, value, type, checked } = e.target;
  
  // Para inputs normais
  if (type !== 'checkbox') {
    setFormData({ ...formData, [name]: value });
  } else {
    // Para checkboxes
    setFormData({ ...formData, [name]: checked });
  }
};
```

### 3. **Validação em Tempo Real**
```jsx
const validateField = (name, value) => {
  switch (name) {
    case 'email':
      return value.includes('@') ? '' : 'Email inválido';
    case 'password':
      return value.length >= 6 ? '' : 'Mínimo 6 caracteres';
    default:
      return '';
  }
};
```

### 4. **Diferentes Tipos de Inputs**
```jsx
function FormCompleto() {
  const [dados, setDados] = useState({
    texto: '',
    numero: 0,
    select: '',
    checkbox: false,
    radio: ''
  });

  return (
    <form>
      {/* Input texto */}
      <input 
        type="text" 
        value={dados.texto}
        onChange={(e) => setDados({...dados, texto: e.target.value})}
      />
      
      {/* Input número */}
      <input 
        type="number" 
        value={dados.numero}
        onChange={(e) => setDados({...dados, numero: e.target.value})}
      />
      
      {/* Select */}
      <select 
        value={dados.select}
        onChange={(e) => setDados({...dados, select: e.target.value})}
      >
        <option value="">Escolha...</option>
        <option value="opcao1">Opção 1</option>
      </select>
      
      {/* Checkbox */}
      <input 
        type="checkbox" 
        checked={dados.checkbox}
        onChange={(e) => setDados({...dados, checkbox: e.target.checked})}
      />
      
      {/* Radio */}
      <input 
        type="radio" 
        name="radio"
        value="valor1"
        checked={dados.radio === 'valor1'}
        onChange={(e) => setDados({...dados, radio: e.target.value})}
      />
    </form>
  );
}
```

### Exercícios Práticos

**1. Formulário de Login:**
- Criar campos email e senha
- Validar formato de email
- Mostrar/ocultar senha
- Mensagens de erro em tempo real

**2. Busca de Países:**
- Adicionar campo de busca no projeto
- Filtrar países conforme usuário digita
- Destacar termo buscado nos resultados

**3. Edição de Países:**
- Permitir editar países existentes
- Formulário pré-preenchido
- Confirmar alterações

### Próximos Passos

No próximo módulo aprenderemos sobre **Listas e Renderização Condicional**, onde expandiremos nossos conhecimentos sobre como renderizar múltiplos elementos e controlar a exibição baseada em condições!

### Resumo

- **Eventos**: Capturam ações do usuário (cliques, digitação, envio)
- **SyntheticEvents**: Eventos sintéticos do React funcionam igual em todos os navegadores
- **Formulários Controlados**: React controla o estado dos inputs via useState
- **Validação**: Verificar dados antes de processar
- **preventDefault()**: Evitar comportamentos padrão do navegador
- **Event Handlers**: Funções que respondem aos eventos
- **Projeto prático**: Formulário para adicionar países à lista
