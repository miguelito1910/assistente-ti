import { useCallback, useEffect, useMemo, useState } from 'react';
import type { Category, Priority, Problem } from './types/problem';
import { createProblem, getProblemById, getProblems } from './services/api';
import { ProblemForm } from './components/ProblemForm';
import { ProblemDetail } from './components/ProblemDetail';
import { ProblemHistoryList } from './components/ProblemHistoryList';
import './index.css';

export function App() {
  const [problems, setProblems] = useState<Problem[]>([]);
  const [isLoadingHistory, setIsLoadingHistory] = useState(true);
  const [historyError, setHistoryError] = useState<string | null>(null);

  const [isCreating, setIsCreating] = useState(false);
  const [latestCreated, setLatestCreated] = useState<Problem | null>(null);

  const [selectedProblem, setSelectedProblem] = useState<Problem | null>(null);
  const [isLoadingDetail, setIsLoadingDetail] = useState(false);
  const [detailError, setDetailError] = useState<string | null>(null);

  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState<Category | 'Todas'>('Todas');
  const [priorityFilter, setPriorityFilter] = useState<Priority | 'Todas'>('Todas');

  const fetchHistory = useCallback(async () => {
    setIsLoadingHistory(true);
    setHistoryError(null);
    try {
      const data = await getProblems();
      setProblems(data);
    } catch (err: unknown) {
      const message =
        err instanceof Error ? err.message : 'Não foi possível carregar o histórico de chamados.';
      setHistoryError(message);
    } finally {
      setIsLoadingHistory(false);
    }
  }, []);

  useEffect(() => {
    let isCancelled = false;

    getProblems()
      .then((data) => {
        if (!isCancelled) {
          setProblems(data);
          setHistoryError(null);
        }
      })
      .catch((err: unknown) => {
        if (!isCancelled) {
          const message =
            err instanceof Error
              ? err.message
              : 'Não foi possível carregar o histórico de chamados.';
          setHistoryError(message);
        }
      })
      .finally(() => {
        if (!isCancelled) {
          setIsLoadingHistory(false);
        }
      });

    return () => {
      isCancelled = true;
    };
  }, []);

  const handleCreateProblem = async (description: string) => {
    setIsCreating(true);
    setDetailError(null);
    try {
      const created = await createProblem({ description });
      setLatestCreated(created);
      setSelectedProblem(null);
      setProblems((prev) => [created, ...prev]);
    } finally {
      setIsCreating(false);
    }
  };

  const handleSelectProblem = async (id: number) => {
    setIsLoadingDetail(true);
    setDetailError(null);
    try {
      const problem = await getProblemById(id);
      setSelectedProblem(problem);
    } catch (err: unknown) {
      const message =
        err instanceof Error ? err.message : 'Não foi possível carregar os detalhes do chamado.';
      setDetailError(message);
    } finally {
      setIsLoadingDetail(false);
    }
  };

  const handleBackToNew = () => {
    setSelectedProblem(null);
    setDetailError(null);
  };

  const handleClearFilters = () => {
    setSearchQuery('');
    setCategoryFilter('Todas');
    setPriorityFilter('Todas');
  };

  const filteredProblems = useMemo(() => {
    const query = searchQuery.trim().toLowerCase();
    return problems.filter((problem) => {
      if (categoryFilter !== 'Todas' && problem.category !== categoryFilter) {
        return false;
      }
      if (priorityFilter !== 'Todas' && problem.priority !== priorityFilter) {
        return false;
      }
      if (query !== '') {
        const matchesSummary = problem.summary.toLowerCase().includes(query);
        const matchesDescription = problem.description.toLowerCase().includes(query);
        const matchesId = String(problem.id) === query.replace('#', '');
        return matchesSummary || matchesDescription || matchesId;
      }
      return true;
    });
  }, [problems, searchQuery, categoryFilter, priorityFilter]);

  return (
    <div className="app-shell">
      <a className="skip-link" href="#workspace-main">
        Pular para o conteúdo
      </a>

      <header className="topbar">
        <div className="wrap topbar-inner">
          <div className="brand">
            <span className="brand-mark" aria-hidden="true" />
            <h1 className="brand-name">Assistente de TI</h1>
          </div>

          <div className="topbar-actions">
            <span className="topbar-count">
              {problems.length} {problems.length === 1 ? 'chamado' : 'chamados'}
            </span>
            {selectedProblem && (
              <button type="button" className="btn btn--primary btn--sm" onClick={handleBackToNew}>
                Novo registro
              </button>
            )}
          </div>
        </div>
      </header>

      <main id="workspace-main" className="workspace">
        <div className="wrap workspace-grid">
          <div className="workspace-primary">
            {detailError && (
              <div className="alert-error" role="alert">
                {detailError}
              </div>
            )}

            {selectedProblem ? (
              <ProblemDetail
                problem={selectedProblem}
                headingLabel="Detalhes do registro"
                isLoading={isLoadingDetail}
                onBackToNew={handleBackToNew}
              />
            ) : (
              <div className="workspace-stack">
                <ProblemForm onSubmit={handleCreateProblem} isLoading={isCreating} />
                {latestCreated && (
                  <ProblemDetail
                    problem={latestCreated}
                    headingLabel="Resultado da triagem"
                  />
                )}
              </div>
            )}
          </div>

          <aside className="workspace-secondary">
            <ProblemHistoryList
              problems={filteredProblems}
              selectedId={selectedProblem?.id ?? null}
              isLoading={isLoadingHistory}
              error={historyError}
              searchQuery={searchQuery}
              categoryFilter={categoryFilter}
              priorityFilter={priorityFilter}
              onSearchChange={setSearchQuery}
              onCategoryChange={setCategoryFilter}
              onPriorityChange={setPriorityFilter}
              onClearFilters={handleClearFilters}
              onSelectProblem={handleSelectProblem}
              onRefresh={fetchHistory}
            />
          </aside>
        </div>
      </main>
    </div>
  );
}

export default App;
