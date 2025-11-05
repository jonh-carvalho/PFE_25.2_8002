/**
 * Página Inicial (HomePage)
 * Exibe a lista de projetos
 * @param {object} props
 * @param {Array} props.projects - Lista de projetos
 * @param {boolean} props.loading - Estado de carregamento
 * @param {string|null} props.error - Mensagem de erro
 */
function HomePage({ projects, loading, error }) {
  return (
    <div className="bg-white p-6 sm:p-8 rounded-lg shadow-lg">
      <h1 className="text-3xl font-bold text-gray-800 mb-6 border-b pb-4">
        Projetos Cadastrados
      </h1>

      {/* Exibe mensagem de erro */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6" role="alert">
          <strong className="font-bold">Erro: </strong>
          <span className="block sm:inline">{error}</span>
          <p className="text-sm mt-1">Verifique se o `json-server` está rodando na porta 5000.</p>
        </div>
      )}

      {/* Exibe indicador de carregamento */}
      {loading && (
        <div className="text-center py-4">
          <p className="text-lg text-gray-600">Carregando projetos...</p>
        </div>
      )}

      {/* Exibe a lista de projetos */}
      {!loading && !error && (
        <div className="space-y-6">
          {projects.length === 0 ? (
            <p className="text-lg text-gray-600">Nenhum projeto cadastrado ainda.</p>
          ) : (
            projects.map((project) => (
              <div
                key={project.id}
                className="border border-gray-200 p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200"
              >
                <h2 className="text-2xl font-semibold text-blue-700 mb-2">{project.name}</h2>
                <p className="text-gray-700 mb-4 whitespace-pre-wrap">{project.description}</p>
                <div className="text-sm text-gray-600 font-medium">
                  <strong>Orçamento:</strong> R$ {
                    parseFloat(project.budget).toLocaleString('pt-BR', {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2
                    })
                  }
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default HomePage;