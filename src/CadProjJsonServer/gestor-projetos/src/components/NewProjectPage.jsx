/**
 * Página de Novo Projeto (NewProjectPage)
 * Exibe o formulário de cadastro
 * @param {object} props
 * @param {function} props.onAddProject - Função para adicionar um novo projeto
 */

import { useState } from 'react';

function NewProjectPage({ onAddProject }) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [budget, setBudget] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Validação simples
    if (!name.trim() || !description.trim() || !budget) {
      setFormError('Todos os campos são obrigatórios.');
      return;
    }

    setSubmitting(true);
    setFormError('');

    const newProject = {
      name,
      description,
      budget: parseFloat(budget),
    };

    // Chama a função passada pelo App.jsx
    const success = await onAddProject(newProject);

    if (success) {
      // O App.jsx cuidará de mudar a página
      // Limpar o formulário (embora o componente vá "desmontar")
      setName('');
      setDescription('');
      setBudget('');
    } else {
      setFormError('Falha ao enviar o projeto. Tente novamente.');
    }
    setSubmitting(false);
  };

  return (
    <div className="bg-white p-6 sm:p-8 rounded-lg shadow-lg max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-6 border-b pb-4">
        Cadastrar Novo Projeto
      </h1>
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Exibe erro do formulário */}
        {formError && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg" role="alert">
            {formError}
          </div>
        )}

        {/* Campo: Nome do Projeto */}
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
            Nome do Projeto
          </label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Ex: Novo Website Corporativo"
          />
        </div>

        {/* Campo: Descrição */}
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Descrição
          </label>
          <textarea
            id="description"
            rows="4"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Descreva os objetivos do projeto..."
          ></textarea>
        </div>

        {/* Campo: Orçamento */}
        <div>
          <label htmlFor="budget" className="block text-sm font-medium text-gray-700 mb-1">
            Orçamento (R$)
          </label>
          <input
            type="number"
            id="budget"
            step="0.01"
            min="0"
            value={budget}
            onChange={(e) => setBudget(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Ex: 5000.00"
          />
        </div>

        {/* Botão de Envio */}
        <div>
          <button
            type="submit"
            disabled={submitting}
            className="w-full py-3 px-4 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {submitting ? 'Enviando...' : 'Cadastrar Projeto'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default NewProjectPage;