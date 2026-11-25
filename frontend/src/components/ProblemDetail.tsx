import type { Problem } from '../types/problem';
import { PriorityBadge } from './PriorityBadge';

interface ProblemDetailProps {
  problem: Problem;
  headingLabel: string;
  isLoading?: boolean;
  onBackToNew?: () => void;
}

export function ProblemDetail({
  problem,
  headingLabel,
  isLoading = false,
  onBackToNew,
}: ProblemDetailProps) {
  const formattedDate = new Date(problem.created_at).toLocaleString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    <article className="panel detail-panel" aria-busy={isLoading}>
      <div className="detail-top">
        <div className="detail-meta-left">
          <span className="detail-eyebrow">{headingLabel}</span>
          <span className="detail-id">Chamado #{problem.id}</span>
        </div>
        {onBackToNew && (
          <button type="button" className="btn btn--secondary btn--sm" onClick={onBackToNew}>
            Voltar ao formulário
          </button>
        )}
      </div>

      <h2 className="detail-summary">{problem.summary}</h2>

      <dl className="detail-attributes">
        <div className="detail-attr">
          <dt>Categoria</dt>
          <dd>
            <span className="tag-neutral">{problem.category}</span>
          </dd>
        </div>
        <div className="detail-attr">
          <dt>Prioridade</dt>
          <dd>
            <PriorityBadge priority={problem.priority} />
          </dd>
        </div>
        <div className="detail-attr">
          <dt>Registrado em</dt>
          <dd className="detail-date">{formattedDate}</dd>
        </div>
      </dl>

      <div className="detail-block">
        <h3 className="detail-block-title">Sugestão inicial de solução</h3>
        <p className="detail-suggestion-text">{problem.initial_suggestion}</p>
        <p className="detail-disclaimer">
          Orientação preliminar gerada por IA. Não substitui o diagnóstico técnico definitivo.
        </p>
      </div>

      <div className="detail-block detail-block--muted">
        <h3 className="detail-block-title">Relato original do usuário</h3>
        <p className="detail-description-text">{problem.description}</p>
      </div>
    </article>
  );
}
