import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { XMarkIcon } from '@heroicons/react/24/outline';
import {
  fetchMeasures,
  createMeasure,
  type CustomerMeasureCreateData,
  type MeasureCreateData,
} from '../../api/measureApi';

/**
 * Props för AddMeasureModal komponenten
 */
interface AddMeasureModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: CustomerMeasureCreateData) => void;
}

// Typ för vilket läge modalen är i
type ModalMode = 'select' | 'create';

export default function AddMeasureModal({ isOpen, onClose, onSubmit }: AddMeasureModalProps) {
  // State för modal-läge (välj från katalog vs skapa ny)
  const [mode, setMode] = useState<ModalMode>('select');

  // State för "Välj från katalog"
  const [selectedMeasureId, setSelectedMeasureId] = useState<number | null>(null);
  const [frequency, setFrequency] = useState<string>('WEEKLY');
  const [occurrencesPerWeek, setOccurrencesPerWeek] = useState<number>(1);
  const [customDuration, setCustomDuration] = useState<number | null>(null);

  // State för "Skapa ny"
  const [newMeasureName, setNewMeasureName] = useState<string>('');
  const [newMeasureDuration, setNewMeasureDuration] = useState<number>(30);

  const queryClient = useQueryClient();

  // Hämta alla aktiva measures från katalogen
  const { data: measures = [], isLoading: measuresLoading } = useQuery({
    queryKey: ['measures'],
    queryFn: () => fetchMeasures(true),
    enabled: isOpen,
  });

  // Mutation för att skapa ny measure
  const createMeasureMutation = useMutation({
    mutationFn: (data: MeasureCreateData) => createMeasure(data),
    onSuccess: (newMeasure) => {
      // Uppdatera measures-listan
      queryClient.invalidateQueries({ queryKey: ['measures'] });

      // Välj den nya measure automatiskt och byt till select-läge
      setSelectedMeasureId(newMeasure.id);
      setCustomDuration(newMeasure.default_duration);
      setMode('select');

      // Rensa create-formuläret
      setNewMeasureName('');
      setNewMeasureDuration(30);
    },
  });

  // Hitta den valda measure för att visa info
  const selectedMeasure = measures.find((m) => m.id === selectedMeasureId);

  /**
   * Återställer formuläret till default-värden.
   */
  const resetForm = () => {
    setMode('select');
    setSelectedMeasureId(null);
    setFrequency('WEEKLY');
    setOccurrencesPerWeek(1);
    setCustomDuration(null);
    setNewMeasureName('');
    setNewMeasureDuration(30);
  };

  /**
   * Hanterar stängning av modal.
   */
  const handleClose = () => {
    resetForm();
    onClose();
  };

  /**
   * Hanterar skapande av ny measure.
   */
  const handleCreateMeasure = () => {
    if (!newMeasureName.trim()) return;

    createMeasureMutation.mutate({
      name: newMeasureName.trim(),
      default_duration: newMeasureDuration,
      text: null,
    });
  };

  /**
   * Hanterar submit av formuläret.
   */
  const handleSubmit = () => {
    if (!selectedMeasureId) return;

    const data: CustomerMeasureCreateData = {
      measure_id: selectedMeasureId,
      frequency: frequency,
      occurrences_per_week: occurrencesPerWeek,
      customer_duration: customDuration,
    };

    onSubmit(data);
    handleClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="w-full max-w-md rounded-xl bg-white shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between border-b p-4">
          <h2 className="text-lg font-bold text-indigo-900">Lägg till insats</h2>
          <button
            onClick={handleClose}
            className="rounded-lg p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-600"
          >
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b">
          <button
            onClick={() => setMode('select')}
            className={`flex-1 py-3 text-sm font-medium transition-colors ${
              mode === 'select'
                ? 'border-b-2 border-indigo-600 text-indigo-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Välj från katalog
          </button>
          <button
            onClick={() => setMode('create')}
            className={`flex-1 py-3 text-sm font-medium transition-colors ${
              mode === 'create'
                ? 'border-b-2 border-indigo-600 text-indigo-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Skapa ny insats
          </button>
        </div>

        {/* Body */}
        <div className="space-y-4 p-4">
          {mode === 'select' ? (
            // ============ VÄLJ FRÅN KATALOG ============
            <>
              {/* Measure Dropdown */}
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">Välj insats</label>
                {measuresLoading ? (
                  <p className="text-sm text-gray-500">Laddar insatser...</p>
                ) : (
                  <select
                    value={selectedMeasureId ?? ''}
                    onChange={(e) => {
                      const id = e.target.value ? Number(e.target.value) : null;
                      setSelectedMeasureId(id);
                      setCustomDuration(null);
                    }}
                    className="w-full rounded-lg border border-gray-300 p-2 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 focus:outline-none"
                  >
                    <option value="">-- Välj insats --</option>
                    {measures.map((measure) => (
                      <option key={measure.id} value={measure.id}>
                        {measure.name} ({measure.default_duration} min)
                      </option>
                    ))}
                  </select>
                )}
              </div>

              {/* Visa vald insats info */}
              {selectedMeasure && (
                <div className="rounded-lg bg-indigo-50 p-3">
                  <p className="text-sm text-indigo-800">
                    <strong>{selectedMeasure.name}</strong>
                  </p>
                  <p className="text-xs text-indigo-600">
                    Standard tid: {selectedMeasure.default_duration} minuter
                  </p>
                </div>
              )}

              {/* Duration Input */}
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                  Tid (minuter)
                </label>
                <input
                  type="number"
                  min="1"
                  placeholder={selectedMeasure?.default_duration?.toString() ?? 'Välj insats först'}
                  value={customDuration ?? ''}
                  onChange={(e) => {
                    const val = e.target.value ? Number(e.target.value) : null;
                    setCustomDuration(val);
                  }}
                  className="w-full rounded-lg border border-gray-300 p-2 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 focus:outline-none"
                />
                <p className="mt-1 text-xs text-gray-500">
                  Lämna tomt för standardtid ({selectedMeasure?.default_duration ?? '?'} min)
                </p>
              </div>

              {/* Occurrences Input */}
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                  Antal gånger per vecka
                </label>
                <input
                  type="number"
                  min="1"
                  max="14"
                  value={occurrencesPerWeek}
                  onChange={(e) => setOccurrencesPerWeek(Number(e.target.value))}
                  className="w-full rounded-lg border border-gray-300 p-2 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 focus:outline-none"
                />
              </div>

              {/* Frequency Dropdown */}
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">Frekvens</label>
                <select
                  value={frequency}
                  onChange={(e) => setFrequency(e.target.value)}
                  className="w-full rounded-lg border border-gray-300 p-2 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 focus:outline-none"
                >
                  <option value="DAILY">Dagligen</option>
                  <option value="WEEKLY">Varje vecka</option>
                  <option value="MONTHLY">Varje månad</option>
                </select>
              </div>
            </>
          ) : (
            // ============ SKAPA NY INSATS ============
            <>
              <div className="rounded-lg bg-yellow-50 p-3">
                <p className="text-xs text-yellow-800">
                  💡 Skapa en ny insatstyp som sparas i katalogen och kan användas för andra kunder
                  också.
                </p>
              </div>

              {/* Namn Input */}
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                  Namn på insats
                </label>
                <input
                  type="text"
                  placeholder="t.ex. Extra städ, Fönsterputs..."
                  value={newMeasureName}
                  onChange={(e) => setNewMeasureName(e.target.value)}
                  className="w-full rounded-lg border border-gray-300 p-2 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 focus:outline-none"
                />
              </div>

              {/* Duration Input */}
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                  Standardtid (minuter)
                </label>
                <input
                  type="number"
                  min="1"
                  value={newMeasureDuration}
                  onChange={(e) => setNewMeasureDuration(Number(e.target.value))}
                  className="w-full rounded-lg border border-gray-300 p-2 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 focus:outline-none"
                />
              </div>

              {/* Create Button */}
              <button
                onClick={handleCreateMeasure}
                disabled={!newMeasureName.trim() || createMeasureMutation.isPending}
                className="w-full rounded-lg bg-green-600 py-2 text-white hover:bg-green-700 disabled:cursor-not-allowed disabled:bg-gray-300"
              >
                {createMeasureMutation.isPending ? 'Skapar...' : 'Skapa insats'}
              </button>

              {/* Error message */}
              {createMeasureMutation.isError && (
                <p className="text-sm text-red-600">
                  Kunde inte skapa insats. Kanske namnet redan finns?
                </p>
              )}
            </>
          )}
        </div>

        {/* Footer - bara för select mode */}
        {mode === 'select' && (
          <div className="flex justify-end gap-2 border-t p-4">
            <button
              onClick={handleClose}
              className="rounded-lg px-4 py-2 text-gray-600 hover:bg-gray-100"
            >
              Avbryt
            </button>
            <button
              onClick={handleSubmit}
              disabled={!selectedMeasureId}
              className="rounded-lg bg-indigo-900 px-4 py-2 text-white hover:bg-indigo-800 disabled:cursor-not-allowed disabled:bg-gray-300"
            >
              Lägg till
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
