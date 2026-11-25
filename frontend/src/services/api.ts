import type { Problem, ProblemCreateRequest } from '../types/problem';

const API_BASE_URL = 'http://localhost:8000';

export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

export async function createProblem(data: ProblemCreateRequest): Promise<Problem> {
  const response = await fetch(`${API_BASE_URL}/problems`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const message =
      typeof errorData.detail === 'string'
        ? errorData.detail
        : `Erro ${response.status}: Falha ao analisar o problema.`;
    throw new ApiError(response.status, message);
  }

  return response.json();
}

export async function getProblems(): Promise<Problem[]> {
  const response = await fetch(`${API_BASE_URL}/problems`);

  if (!response.ok) {
    throw new ApiError(response.status, `Erro ${response.status}: Falha ao buscar histórico de problemas.`);
  }

  return response.json();
}

export async function getProblemById(id: number): Promise<Problem> {
  const response = await fetch(`${API_BASE_URL}/problems/${id}`);

  if (!response.ok) {
    throw new ApiError(response.status, `Erro ${response.status}: Problema não encontrado.`);
  }

  return response.json();
}
