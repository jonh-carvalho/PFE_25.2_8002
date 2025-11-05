/**
 * Componente Principal (App)
 * Gerencia o estado da aplicação, a navegação e os dados da API
 */
import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar.jsx';
import HomePage from './components/HomePage.jsx';
import NewProjectPage from './components/NewProjectPage.jsx';
import ContactPage from './components/ContactPage.jsx';
import AboutPage from './components/AboutPage.jsx';

// --- Configuração da API ---
// URL base para o seu json-server
const API_URL = 'http://localhost:3000/projects';

export default function App() {
  // Estado para controlar a página atual
  const [page, setPage] = useState('home'); // 'home', 'new', 'contact', 'about'

  // Estados para os dados da API
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null); // Armazena erros da API

  // --- Lógica da API ---

  // 1. Buscar (GET) projetos quando o componente é montado
  useEffect(() => {
    const fetchProjects = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await fetch(API_URL);
        if (!response.ok) {
          throw new Error(`Erro HTTP: ${response.status}`);
        }
        const data = await response.json();
        setProjects(data);
      } catch (e) {
        console.error("Falha ao buscar projetos:", e);
        setError("Falha ao carregar projetos. O servidor API está acessível?");
      } finally {
        setLoading(false);
      }
    };

    fetchProjects();
  }, []); // O array vazio [] significa que este efeito roda apenas uma vez

  // 2. Adicionar (POST) um novo projeto
  const handleAddProject = async (projectData) => {
    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(projectData),
      });

      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }
      
      const newProject = await response.json();

      // Atualiza o estado local com o novo projeto
      setProjects(prevProjects => [...prevProjects, newProject]);
      
      // "Redireciona" para a página inicial
      setPage('home'); 
      return true; // Sinaliza sucesso
    } catch (e) {
      console.error("Falha ao adicionar projeto:", e);
      setError("Falha ao salvar o projeto. Tente novamente."); // Pode definir um erro específico para o formulário
      return false; // Sinaliza falha
    }
  };

  // --- Renderização da Página ---

  // Função "roteadora" que renderiza o componente da página correta
  const renderPage = () => {
    switch (page) {
      case 'home':
        return <HomePage projects={projects} loading={loading} error={error} />;
      case 'new':
        return <NewProjectPage onAddProject={handleAddProject} />;
      case 'contact':
        return <ContactPage />;
      case 'about':
        return <AboutPage />;
      default:
        return <HomePage projects={projects} loading={loading} error={error} />;
    }
  };

  return (
    // Adiciona um fundo cinza a toda a aplicação
    <div className="min-h-screen bg-gray-100 font-sans">
      {/* Adiciona animação de fade-in */}
      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .page-container {
          animation: fadeIn 0.3s ease-out;
        }
      `}</style>
      
      {/* Barra de Navegação Fixa */}
      <Navbar setPage={setPage} currentPage={page} />

      {/* Conteúdo Principal da Página */}
      <main className="max-w-6xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="page-container">
          {renderPage()}
        </div>
      </main>
    </div>
  );
}





/**
 * Componente Principal (App)
 * Gerencia o estado da aplicação, a navegação e os dados da API
 */