/**
 * Página Sobre (AboutPage)
 * Conteúdo estático
 */
function AboutPage() {
  return (
    <div className="bg-white p-6 sm:p-8 rounded-lg shadow-lg">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Sobre o Gestor de Projetos</h1>
      <div className="space-y-4 text-lg text-gray-700">
        <p>
          Esta é uma aplicação simples de cadastro de projetos desenvolvida para demonstrar
          o uso de React com Vite e a integração com uma API mock (json-server).
        </p>
        <p>
          O objetivo é mostrar como gerenciar o estado, consumir dados de uma API (GET/POST)
          e simular a navegação entre páginas sem o uso de uma biblioteca de roteamento
          como o `react-router-dom`.
        </p>
        <p><strong>Tecnologias utilizadas:</strong></p>
        <ul className="list-disc list-inside space-y-2">
          <li>React (com Hooks: useState, useEffect)</li>
          <li>Vite (como builder)</li>
          <li>Tailwind CSS (para estilização)</li>
          <li>json-server (para simular a API REST)</li>
        </ul>
      </div>
    </div>
  );
}

export default AboutPage;
