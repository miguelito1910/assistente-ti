import type { Priority } from '../types/problem';

interface PriorityBadgeProps {
  priority: Priority;
}

const PRIORITY_CLASS: Record<Priority, string> = {
  Alta: 'priority-indicator--alta',
  Média: 'priority-indicator--media',
  Baixa: 'priority-indicator--baixa',
};

export function PriorityBadge({ priority }: PriorityBadgeProps) {
  return (
    <span className={`priority-indicator ${PRIORITY_CLASS[priority]}`}>
      <span className="priority-dot" aria-hidden="true" />
      <span>{priority}</span>
    </span>
  );
}
