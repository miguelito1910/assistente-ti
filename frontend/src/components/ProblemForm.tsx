import { useState, type FormEvent } from 'react';
import { ApiError } from '../services/api';

interface ProblemFormProps {
  onSubmit: (description: string) => Promise<void>;
  isLoading: boolean;
}

const MIN_DESCRIPTION_LENGTH = 10;

export function ProblemForm({ onSubmit, isLoading }: ProblemFormProps) {
  const [description, setDescription] = useState('');
  const [fieldError, setFieldError] = useState<string | null>(null);
  const [submitError, setSubmitError] = useState<{ message: string; isTransient: boolean } | null>(
    null,
  );

  const trimmedLength = description.trim().length;
  const errorId = 'problem-description-error';

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (trimmedLength < MIN_DESCRIPTION_LENGTH) {
      setFieldError('Descreva o problema com pelo menos 10 caracteres para iniciar a triagem.');
      setSubmitError(null);
      return;
    }

    setFieldError(null);
    setSubmitError(null);
    try {
      await onSubmit(description.trim());
      setDescription('');
    } catch (err: unknown) {
      if (err instanceof ApiError) {
        setSubmitError({
          message: err.message,
          isTransient: err.status === 503 || err.status === 429,
        });
      } else {
        const message =
          err instanceof Error ? err.message : 'Não foi possível concluir a análise do problema.';
        setSubmitError({ message, isTransient: false });
      }
    }
  };

  return (
    <form className="panel form-panel" onSubmit={handleSubmit} noValidate>
      <div className="panel-header">
        <div>
          <h2 className="panel-title">Registrar problema técnico</h2>
          <p className="panel-subtitle">
            Descreva o incidente em linguagem natural para classificação automática de categoria,
            prioridade e sugestão inicial.
          </p>
        </div>
      </div>

      <div className="field">
        <label className="field-label" htmlFor="problem-description">
          Descrição do incidente
        </label>
        <textarea
          id="problem-description"
          name="description"
          rows={5}
          className="field-textarea"
          placeholder="Ex.: Meu computador está conectado ao Wi-Fi, mas não carrega nenhum site. Outros aparelhos na rede navegam normalmente."
          value={description}
          onChange={(e) => {
            setDescription(e.target.value);
            if (fieldError) setFieldError(null);
            if (submitError) setSubmitError(null);
          }}
          disabled={isLoading}
          aria-invalid={fieldError ? 'true' : 'false'}
          aria-describedby={fieldError ? errorId : 'problem-description-hint'}
        />
        <div className="field-meta">
          <span id="problem-description-hint" className="field-hint">
            Mínimo de {MIN_DESCRIPTION_LENGTH} caracteres
          </span>
          <span className="field-counter">{description.length} / 5000</span>
        </div>
        {fieldError && (
          <p id={errorId} className="field-error" role="alert">
            {fieldError}
          </p>
        )}
      </div>

      <div className="form-actions">
        {submitError && (
          <div
            className={submitError.isTransient ? 'alert-warning' : 'alert-error'}
            role="alert"
          >
            {submitError.message}
          </div>
        )}

        <button type="submit" className="btn btn--primary" disabled={isLoading}>
          {isLoading ? (
            <>
              <span className="spinner" aria-hidden="true" />
              <span>Analisando problema</span>
            </>
          ) : (
            <span>Analisar problema</span>
          )}
        </button>
        <p className="form-status" role="status" aria-live="polite">
          {isLoading ? 'Consultando classificação e salvando registro no banco de dados.' : ''}
        </p>
      </div>
    </form>
  );
}
