import {
  CATEGORIES,
  PRIORITIES,
  type Category,
  type Priority,
  type Problem,
} from '../types/problem';
import { PriorityBadge } from './PriorityBadge';

interface ProblemHistoryListProps {
  problems: Problem[];
  selectedId: number | null;
  isLoading: boolean;
  error: string | null;
  searchQuery: string;
  categoryFilter: Category | 'Todas';
  priorityFilter: Priority | 'Todas';
  onSearchChange: (value: string) => void;
  onCategoryChange: (value: Category | 'Todas') => void;
  onPriorityChange: (value: Priority | 'Todas') => void;
  onClearFilters: () => void;
  onSelectProblem: (id: number) => void;
  onRefresh: () => void;
}

export function ProblemHistoryList({
  problems,
  selectedId,
  isLoading,
  error,
  searchQuery,
  categoryFilter,
  priorityFilter,
  onSearchChange,
  onCategoryChange,
  onPriorityChange,
  onClearFilters,
  onSelectProblem,
  onRefresh,
}: ProblemHistoryListProps) {
  const hasActiveFilters =
    searchQuery.trim() !== '' || categoryFilter !== 'Todas' || priorityFilter !== 'Todas';

  return (
    <section className="panel history-panel" aria-label="Histórico de chamados">
      <div className="history-header">
        <div>
          <h2 className="panel-title">Histórico de chamados</h2>
          <p className="history-count">
            {problems.length} {problems.length === 1 ? 'registro exibido' : 'registros exibidos'}
          </p>
        </div>
        <button
          type="button"
          className="btn btn--secondary btn--sm"
          onClick={onRefresh}
          disabled={isLoading}
        >
          {isLoading ? 'Atualizando' : 'Atualizar lista'}
        </button>
      </div>

      <div className="history-filters">
        <div className="filter-field filter-field--search">
          <label className="field-label" htmlFor="history-search">
            Buscar
          </label>
          <input
            id="history-search"
            type="search"
            className="field-input"
            placeholder="Buscar por resumo ou relato"
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
          />
        </div>

        <div className="filter-row">
          <div className="filter-field">
            <label className="field-label" htmlFor="filter-category">
              Categoria
            </label>
            <select
              id="filter-category"
              className="field-select"
              value={categoryFilter}
              onChange={(e) => onCategoryChange(e.target.value as Category | 'Todas')}
            >
              <option value="Todas">Todas</option>
              {CATEGORIES.map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>
          </div>

          <div className="filter-field">
            <label className="field-label" htmlFor="filter-priority">
              Prioridade
            </label>
            <select
              id="filter-priority"
              className="field-select"
              value={priorityFilter}
              onChange={(e) => onPriorityChange(e.target.value as Priority | 'Todas')}
            >
              <option value="Todas">Todas</option>
              {PRIORITIES.map((priority) => (
                <option key={priority} value={priority}>
                  {priority}
                </option>
              ))}
            </select>
          </div>
        </div>

        {hasActiveFilters && (
          <button type="button" className="btn-link" onClick={onClearFilters}>
            Limpar filtros
          </button>
        )}
      </div>

      {error && (
        <div className="alert-error" role="alert">
          {error}
        </div>
      )}

      {isLoading && problems.length === 0 ? (
        <div className="history-empty">
          <p>Carregando histórico de registros...</p>
        </div>
      ) : problems.length === 0 ? (
        <div className="history-empty">
          <p>
            {hasActiveFilters
              ? 'Nenhum chamado corresponde aos filtros aplicados.'
              : 'Nenhum problema registrado até o momento.'}
          </p>
        </div>
      ) : (
        <ul className="history-list">
          {problems.map((problem) => {
            const isSelected = problem.id === selectedId;
            const formattedDate = new Date(problem.created_at).toLocaleString('pt-BR', {
              day: '2-digit',
              month: '2-digit',
              hour: '2-digit',
              minute: '2-digit',
            });

            return (
              <li key={problem.id}>
                <button
                  type="button"
                  className={`history-item ${isSelected ? 'is-selected' : ''}`}
                  onClick={() => onSelectProblem(problem.id)}
                  aria-current={isSelected ? 'true' : undefined}
                >
                  <div className="history-item-top">
                    <span className="history-item-id">#{problem.id}</span>
                    <PriorityBadge priority={problem.priority} />
                  </div>
                  <p className="history-item-summary">{problem.summary}</p>
                  <div className="history-item-bottom">
                    <span className="tag-neutral">{problem.category}</span>
                    <span className="history-item-date">{formattedDate}</span>
                  </div>
                </button>
              </li>
            );
          })}
        </ul>
      )}
    </section>
  );
}
