import { useState, useEffect } from 'react';
import type { Problem } from './types/problem';
import { createProblem, getProblems } from './services/api';
import { ProblemForm } from './components/ProblemForm';
import { ProblemCard } from './components/ProblemCard';
import './index.css';

export function App() {
  const [activeTab, setActiveTab] = useState<'create' | 'history'>('create');
  const [problems, setProblems] = useState<Problem[]>([]);
  const [latestProblem, setLatestProblem] = useState<Problem | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isFetchingHistory, setIsFetchingHistory] = useState(false);
  const [historyError, setHistoryError] = useState<string | null>(null);

  // Carrega o histórico de chamados ao mudar para a aba de histórico
  useEffect(() => {
    if (activeTab === 'history') {
      fetchHistory();
    }
  }, [activeTab]);

  const fetchHistory = async () => {
    setIsFetchingHistory(true);
    setHistoryError(null);
    try {
      const data = await getProblems();
      setProblems(data);
    } catch (err: any) {
      setHistoryError(err.message || 'Erro ao carregar o histórico.');
    } finally {
      setIsFetchingHistory(false);
    }
  };

  const handleCreateProblem = async (description: string) => {
    setIsLoading(true);
    try {
      const newProblem = await createProblem({ description });
      setLatestProblem(newProblem);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Barra de Navegação */}
      <header className="navbar">
        <div className="nav-brand">
          <span style={{ fontSize: '1.5rem' }}>🛠️</span>
          <h1>Assistente Inteligente de TI</h1>
        </div>

        <nav className="nav-tabs">
          <button
            className={`tab-btn ${activeTab === 'create' ? 'active' : ''}`}
            onClick={() => setActiveTab('create')}
          >
            Novo Chamado
          </button>
          <button
            className={`tab-btn ${activeTab === 'history' ? 'active' : ''}`}
            onClick={() => setActiveTab('history')}
          >
            Histórico de Problemas
          </button>
        </nav>
      </header>

      {/* Conteúdo Principal */}
      <main className="main-content">
        {activeTab === 'create' && (
          <div>
            <ProblemForm onSubmit={handleCreateProblem} isLoading={isLoading} />

            {/* Exibição imediata do resultado após análise da IA */}
            {latestProblem && (
              <section className="result-section">
                <h2>✨ Resultado da Análise da IA:</h2>
                <ProblemCard problem={latestProblem} />
              </section>
            )}
          </div>
        )}

        {activeTab === 'history' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
              <h2>Histórico de Atendimentos</h2>
              <button
                className="tab-btn"
                onClick={fetchHistory}
                disabled={isFetchingHistory}
                style={{ border: '1px solid var(--border-color)' }}
              >
                🔄 Atualizar
              </button>
            </div>

            {historyError && <div className="error-message">{historyError}</div>}

            {isFetchingHistory ? (
              <div className="empty-state">
                <div className="spinner" style={{ margin: '0 auto 1rem auto' }}></div>
                <p>Carregando histórico do banco de dados...</p>
              </div>
            ) : problems.length === 0 ? (
              <div className="card empty-state">
                <p>Nenhum problema registrado até o momento.</p>
              </div>
            ) : (
              problems.map((prob) => (
                <ProblemCard key={prob.id} problem={prob} />
              ))
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
