import React, { useState } from 'react';

interface ProblemFormProps {
  onSubmit: (description: string) => Promise<void>;
  isLoading: boolean;
}

export const ProblemForm: React.FC<ProblemFormProps> = ({ onSubmit, isLoading }) => {
  const [description, setDescription] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (description.trim().length < 10) {
      setError('Por favor, descreva o problema com no mínimo 10 caracteres para que a IA possa analisar.');
      return;
    }

    setError(null);
    try {
      await onSubmit(description);
      setDescription('');
    } catch (err: any) {
      setError(err.message || 'Ocorreu um erro ao processar a solicitação.');
    }
  };

  return (
    <form className="card form-card" onSubmit={handleSubmit}>
      <h2>Descrever Novo Problema Técnico</h2>
      <p className="subtitle">
        Relate em linguagem natural o que está acontecendo. Nossa IA analisará o impacto, classificará e sugerirá uma solução inicial.
      </p>

      <div className="form-group">
        <label htmlFor="description">Descrição do Problema:</label>
        <textarea
          id="description"
          rows={5}
          placeholder="Ex: Meu computador está conectado ao Wi-Fi, mas não consigo acessar nenhum site. Outros dispositivos estão navegando normalmente..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          disabled={isLoading}
        />
        <div className="char-count">
          {description.length} caracteres (mínimo 10)
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      <button type="submit" className="btn-primary" disabled={isLoading || description.trim().length < 10}>
        {isLoading ? (
          <>
            <span className="spinner"></span> Analisando com Gemini IA...
          </>
        ) : (
          'Analisar e Registrar Problema'
        )}
      </button>
    </form>
  );
};
