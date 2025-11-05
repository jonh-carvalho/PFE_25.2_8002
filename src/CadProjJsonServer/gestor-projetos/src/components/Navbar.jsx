// --- Configuração da API ---
// URL base para o seu json-server
const API_URL = 'http://localhost:5000/projects';

/**
 * Componente da Barra de Navegação
 * @param {object} props
 * @param {function} props.setPage - Função para alterar a página atual
 * @param {string} props.currentPage - Nome da página atual
 */
function Navbar({ setPage, currentPage }) {
  // Função auxiliar para criar itens de navegação
  const NavItem = ({ pageName, children }) => {
    const isActive = currentPage === pageName;
    return (
      <button
        onClick={() => setPage(pageName)}
        className={`px-3 py-2 rounded-md text-sm font-medium transition-colors duration-150 ${
          isActive
            ? 'bg-blue-600 text-white'
            : 'text-gray-700 hover:bg-gray-200 hover:text-gray-900'
        }`}
      >
        {children}
      </button>
    );
  };

  return (
    <nav className="bg-white shadow-sm sticky top-0 z-10">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex-shrink-0 flex items-center">
            {/* Logo ou Título do Site */}
            <span className="text-2xl font-bold text-blue-600">
              Gestor de Projetos
            </span>
          </div>
          {/* Links de Navegação */}
          <div className="hidden sm:ml-6 sm:flex sm:space-x-4">
            <NavItem pageName="home">Início</NavItem>
            <NavItem pageName="new">Novo Projeto</NavItem>
            <NavItem pageName="contact">Contato</NavItem>
            <NavItem pageName="about">Sobre</NavItem>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;