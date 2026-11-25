export const CATEGORIES = [
  'Hardware',
  'Software',
  'Rede',
  'Segurança',
  'Sistema Operacional',
  'Banco de Dados',
  'Outros',
] as const;

export type Category = (typeof CATEGORIES)[number];

export const PRIORITIES = ['Alta', 'Média', 'Baixa'] as const;

export type Priority = (typeof PRIORITIES)[number];

export interface ProblemCreateRequest {
  description: string;
}

export interface Problem {
  id: number;
  description: string;
  category: Category;
  priority: Priority;
  summary: string;
  initial_suggestion: string;
  created_at: string;
}
