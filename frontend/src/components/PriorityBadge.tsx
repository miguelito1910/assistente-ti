import React from 'react';
import type { Priority } from '../types/problem';

interface PriorityBadgeProps {
  priority: Priority;
}

export const PriorityBadge: React.FC<PriorityBadgeProps> = ({ priority }) => {
  const getBadgeClass = () => {
    switch (priority) {
      case 'Alta':
        return 'badge-priority-alta';
      case 'Média':
        return 'badge-priority-media';
      case 'Baixa':
        return 'badge-priority-baixa';
      default:
        return '';
    }
  };

  return <span className={`badge ${getBadgeClass()}`}>{priority}</span>;
};
