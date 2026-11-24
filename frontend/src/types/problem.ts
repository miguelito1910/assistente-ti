// Definição dos tipos do sistema (devem espelhar os Schemas do Backend)

export type Category =
  | 'Hardware'
  | 'Software'
  | 'Rede'
  | 'Segurança'
  | 'Sistema Operacional'
  | 'Banco de Dados'
  | 'Outros';

export type Priority = 'Baixa' | 'Média' | 'Alta';

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
