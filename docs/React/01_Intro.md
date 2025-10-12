---
id: introreact
title: 01 - Introdução ao React com HTML e CDN
---

# **React com HTML e CDN**

Apresentar os conceitos básicos do React e como integrá-lo em uma página HTML utilizando um link para a CDN, sem a necessidade de um ambiente de desenvolvimento local como o Node.js.

---

#### **1. Introdução ao React**

**Definição**: React é uma biblioteca JavaScript criada pelo Facebook para criar interfaces de usuário de forma declarativa e eficiente.

**Vantagens**:

  - Componentes reutilizáveis
  - Atualizações rápidas do DOM (Virtual DOM)
  - Facilita a criação de Single Page Applications (SPAs)

**Virtual DOM**:  
O Virtual DOM é uma representação leve da estrutura real do DOM mantida na memória pelo React. Quando o estado de um componente muda, o React atualiza primeiro o Virtual DOM, compara as diferenças com o DOM real (processo chamado de "reconciliation") e aplica apenas as alterações necessárias. Isso torna as atualizações de interface mais rápidas e eficientes, pois evita manipulações desnecessárias do DOM real.

---

#### **Comparação: React vs JavaScript Vanilla**

| Característica            | React                                      | JavaScript Vanilla                      |
|---------------------------|--------------------------------------------|-----------------------------------------|
| Manipulação do DOM        | Utiliza Virtual DOM para otimizar mudanças | Manipulação direta do DOM               |
| Organização do código     | Baseado em componentes reutilizáveis       | Estrutura livre, menos modularidade     |
| Atualização de interface  | Automática via estado e props              | Manual, exige mais código               |
| Aprendizado               | Requer aprender conceitos próprios         | Conhecimento básico de JS suficiente    |
| Escalabilidade            | Ideal para projetos grandes e SPAs         | Mais indicado para projetos simples     |

**Exemplo de atualização de conteúdo:**

*JavaScript Vanilla:*
```html
<div id="root"></div>
<script>
  document.getElementById('root').innerText = 'Hello, World!';
</script>
```

*React:*
```javascript
ReactDOM.render(
  React.createElement('h1', null, 'Hello, World!'),
  document.getElementById('root')
);
```

---

#### **2. Preparando o Ambiente**

* Não é necessário instalar nada localmente para este exemplo inicial, vamos usar uma página HTML e um link para a biblioteca via CDN.

---

#### **3. Estrutura Básica do Projeto**

**HTML Básico**

* Comece com a criação de uma página HTML simples contendo um elemento `<div>` que será usado como “ponto de montagem” para o React.

```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>React Introdução</title>
   </head>
   <body>
     <!-- Div onde o React renderizará o conteúdo -->
     <div id="root"></div>
   
     <!-- Scripts do React via CDN -->
     <script src="https://unpkg.com/react@17/umd/react.production.min.js" crossorigin></script>
     <script src="https://unpkg.com/react-dom@17/umd/react-dom.production.min.js" crossorigin></script>
     <!-- Nosso script JavaScript -->
     <script src="app.js"></script>
   </body>
   </html>
```

---

#### **4. Criando um Elemento React**

Crie o arquivo `app.js` com o seguinte código:

```javascript
   ReactDOM.render(
    React.createElement(
        'h1',
        null,
        'Hello, World!'
    ),
    document.getElementById('root'))
```
