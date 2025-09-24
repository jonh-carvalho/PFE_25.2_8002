---
id: prototipo_baixa_fidelidade_salt
title: Protótipo de Baixa Fidelidade - Salt PlantUML
---

# Protótipo de Baixa Fidelidade - Aplicativo Web E-commerce

## Introdução

<p align = "justify">
Este documento apresenta os protótipos de baixa fidelidade do aplicativo web de e-commerce, desenvolvidos utilizando Salt PlantUML. Os wireframes foram criados com base na análise de tarefas realizada e nas histórias de usuário levantadas, focando nas principais funcionalidades identificadas: gestão de pedidos, controle de estoque e atendimento ao cliente.
</p>

## Metodologia

<p align = "justify">
Os protótipos foram desenvolvidos utilizando a linguagem Salt PlantUML, que permite criar wireframes interativos de forma rápida e colaborativa. A abordagem seguiu os princípios de Design Thinking, priorizando as necessidades dos usuários identificadas na análise de tarefas.
</p>

## Protótipos de Baixa Fidelidade

### Tela de Login

```plantuml
@startsalt
{+ <b>Sistema E-commerce - Login
  .
  {* <b>Acesso ao Sistema
    .
    E-mail/CPF:     | "usuario@empresa.com"
    Senha:          | "********"
    .
    [  Entrar  ]
    .
    [ Esqueci minha senha ]
    .
    Primeiro acesso? [ Criar conta ]
  }
}
@endsalt
```

### Tela Principal - Dashboard Vendedor

```plantuml
@startsalt
{+ <b>Dashboard - Vendedor
  .
  Menu: [ Pedidos ] [ Estoque ] [ Clientes ] [ Relatórios ] [ Sair ]
  .
  {* <b>Área de Trabalho
    .
    // US01: Busca rápida de clientes //
    Buscar cliente: | "Nome ou CPF" 🔍 [Buscar]
    .
    {# <b>Pedidos do Dia
      | Cliente | Produto | Valor | Status |
      | João Silva | Produto A | R$ 150,00 | Finalizado |
      | Maria Santos | Produto B | R$ 89,90 | Pendente |
      | Pedro Costa | Produto C | R$ 220,00 | Preparando |
    }
    .
    [ + Novo Pedido ] [ Ver Todos ]
  }
}
@endsalt
```

### Tela de Registro de Pedido

```plantuml
@startsalt
{+ <b>Registrar Novo Pedido
  .
  {* <b>Dados do Cliente
    Cliente: | "João Silva - 123.456.789-00" [Buscar]
    .
    <b>Produtos Selecionados:
    .
    {#
      | Produto | Qtd | Valor Unit. | Subtotal |
      | Produto A | 2 | R$ 75,00 | R$ 150,00 |
      | - | [ + Adicionar Produto ] | - | - |
    }
    .
    // US02: Aplicar descontos personalizados //
    Desconto (%): | "5" [Aplicar]
    .
    <b>Total: R$ 142,50
    .
    [ Cancelar ] [  Finalizar Pedido  ]
  }
}
@endsalt
```

### Tela de Consulta de Estoque

```plantuml
@startsalt
{+ <b>Controle de Estoque
  .
  {* <b>Filtros
    Categoria: | Todos ▼ | Buscar: | "Nome do produto" 🔍
    .
    // US03: Ver estoque em tempo real //
    {# <b>Produtos em Estoque
      | Código | Produto | Categoria | Qtd | Status |
      | 001 | Produto A | Eletrônicos | 45 | Disponível |
      | 002 | Produto B | Roupas | 0 | **ESGOTADO** |
      | 003 | Produto C | Casa | 120 | Disponível |
      | 004 | Produto D | Livros | 3 | **CRÍTICO** |
    }
    .
    [ Atualizar Estoque ] [ Solicitar Reposição ]
    .
    // US06: Alertas de estoque crítico //
    ⚠️ <b>Alertas: 2 produtos com estoque crítico
  }
}
@endsalt
```

### Tela de Aprovação de Descontos - Gerente

```plantuml
@startsalt
{+ <b>Aprovação de Descontos - Gerente
  .
  {* <b>Solicitações Pendentes
    .
    // US04: Aprovar descontos acima de 10% //
    {# <b>Descontos para Aprovação
      | Vendedor | Cliente | Valor Original | Desconto | Novo Valor | Ação |
      | Ana Costa | João Silva | R$ 500,00 | 15% | R$ 425,00 | [Aprovar] [Rejeitar] |
      | Carlos Lima | Maria Santos | R$ 300,00 | 12% | R$ 264,00 | [Aprovar] [Rejeitar] |
    }
    .
    Observações: | "Justificativa para o desconto..."
    .
    [ Aprovar Selecionados ] [ Rejeitar Selecionados ]
  }
}
@endsalt
```

### Tela de Relatórios

```plantuml
@startsalt
{+ <b>Relatórios de Vendas
  .
  {* <b>Filtros do Relatório
    .
    // US05: Exportar relatórios por período //
    Período: | 01/09/2025 ▼ | até | 30/09/2025 ▼
    .
    Tipo de Relatório:
    (•) Vendas por período
    ( ) Produtos mais vendidos  
    ( ) Performance por vendedor
    ( ) Estoque crítico
    .
    Formato: (•) PDF ( ) Excel ( ) CSV
    .
    [  Gerar Relatório  ]
    .
    <b>Relatórios Recentes:
    {#
      | Data | Tipo | Período | Download |
      | 23/09 | Vendas | Set/2025 | [📄 PDF] |
      | 20/09 | Estoque | - | [📊 Excel] |
    }
  }
}
@endsalt
```

### Tela de Rastreamento - Cliente

```plantuml
@startsalt
{+ <b>Rastreamento de Pedido - Cliente
  .
  {* <b>Meu Pedido #12345
    .
    // US07: Rastrear pedido em tempo real //
    <b>Status do Pedido:
    .
    ✅ Pedido Confirmado (23/09 - 14:30)
    ✅ Pagamento Aprovado (23/09 - 14:35)
    🔄 **Em Preparação** (23/09 - 15:00)
    ⏳ Em Transporte (Previsão: 24/09)
    ⏳ Entregue
    .
    <b>Detalhes:
    Produto: Produto A (Qtd: 2)
    Valor: R$ 150,00
    Entrega prevista: 25/09/2025
    .
    // US08: Solicitar trocas via chat //
    [ 💬 Abrir Chat ] [ 🔄 Solicitar Troca ]
  }
}
@endsalt
```

### Tela de Chat de Suporte - Cliente

```plantuml
@startsalt
{+ <b>Suporte ao Cliente - Chat
  .
  {* <b>Conversa com Suporte
    .
    {# <b>Histórico da Conversa
      <b>Você:</b> Gostaria de trocar o produto do pedido #12345
      .
      <b>Atendente Ana:</b> Olá! Vou verificar seu pedido. 
      Qual o motivo da troca?
      .
      <b>Você:</b> O produto chegou com defeito
      .
      <b>Atendente Ana:</b> Entendo. Vou gerar uma 
      autorização de troca para você.
    }
    .
    Digite sua mensagem: | "Obrigado pelo atendimento!"
    .
    [ Enviar ] [ Anexar Foto ] [ Finalizar Chat ]
  }
}
@endsalt
```

### Fluxo de Navegação

```plantuml
@startsalt
{+ <b>Fluxo Principal de Navegação
  .
  {* <b>Mapa de Telas
    .
    [Login] -> [Dashboard]
    .
    [Dashboard] -> [Novo Pedido]
    [Dashboard] -> [Consultar Estoque] 
    [Dashboard] -> [Relatórios]
    .
    [Novo Pedido] -> [Buscar Cliente]
    [Novo Pedido] -> [Aplicar Desconto] -> [Aprovação Gerente]
    .
    [Cliente] -> [Rastrear Pedido]
    [Cliente] -> [Chat Suporte]
  }
}
@endsalt
```

## Mapeamento com Histórias de Usuário

| Tela | História de Usuário | Funcionalidade Principal |
|------|-------------------|-------------------------|
| Dashboard | US01 | Busca rápida de clientes |
| Registro de Pedido | US02 | Aplicar descontos personalizados |
| Consulta Estoque | US03, US06 | Estoque em tempo real e alertas |
| Aprovação Descontos | US04 | Aprovação de descontos pelo gerente |
| Relatórios | US05 | Exportar relatórios por período |
| Rastreamento | US07 | Rastrear pedido em tempo real |
| Chat Suporte | US08 | Solicitar trocas via chat |

## Considerações de Usabilidade

### Pontos Fortes Identificados:
- **Busca intuitiva**: Campo de busca prominent na tela principal
- **Feedback visual**: Status claros para estoque (ESGOTADO, CRÍTICO)
- **Fluxo simplificado**: Processo de pedido em etapas claras
- **Notificações**: Alertas visuais para ações importantes

### Melhorias Propostas:
- **Responsividade**: Adaptar layouts para dispositivos móveis
- **Acessibilidade**: Adicionar indicadores para usuários com deficiências
- **Performance**: Otimizar carregamento de listas grandes
- **Validação**: Feedback imediato em formulários

## Próximos Passos

1. **Validação com usuários**: Testar os wireframes com as personas identificadas
2. **Refinamento**: Ajustar com base no feedback coletado
3. **Prototipagem interativa**: Evoluir para protótipos de alta fidelidade
4. **Desenvolvimento**: Usar como base para implementação

## Conclusão

<p align = "justify">
Os protótipos de baixa fidelidade apresentados cobrem todas as funcionalidades críticas identificadas na análise de tarefas, priorizando a usabilidade e eficiência dos fluxos principais. A utilização do Salt PlantUML permitiu uma prototipagem rápida e colaborativa, facilitando discussões com a equipe e stakeholders.
</p>

## Referências

> PlantUML Salt. Disponível em: https://plantuml.com/salt

> Material Design Guidelines. Disponível em: https://material.io/design

> Nielsen, J. Usability Engineering. Academic Press, 1993.

## Autor(es)

| Data     | Versão | Descrição                            | Autor(es)                |
| -------- | ------- | -------------------------------------- | ------------------------ |
| 24/09/25 | 1.0     | Criação do documento                 | Equipe de UX/UI          |
| 24/09/25 | 1.1     | Adição dos wireframes Salt PlantUML  | Equipe de UX/UI          |
| 24/09/25 | 1.2     | Mapeamento com histórias de usuário  | Equipe de UX/UI          |
