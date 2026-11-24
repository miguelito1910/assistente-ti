import React from 'react';
import type { Problem } from '../types/problem';
import { PriorityBadge } from './PriorityBadge';

interface ProblemCardProps {
  problem: Problem;
  onClick?: () => void;
}

export const ProblemCard: React.FC<ProblemCardProps> = ({ problem, onClick }) => {
  const formattedDate = new Date(problem.created_at).toLocaleString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    <div className="card problem-card" onClick={onClick}>
      <div className="card-header">
        <span className="problem-id">#{problem.id}</span>
        <div className="badges-group">
          <span className="badge badge-category">{problem.category}</span>
          <PriorityBadge priority={problem.priority} />
        </div>
      </div>

      <h3 className="problem-summary">{problem.summary}</h3>
      <p className="problem-description">{problem.description}</p>

      <div className="problem-suggestion">
        <strong>💡 Sugestão inicial:</strong>
        <p>{problem.initial_suggestion}</p>
      </div>

      <div className="card-footer">
        <span className="timestamp">Registrado em: {formattedDate}</span>
      </div>
    </div>
  );
};
