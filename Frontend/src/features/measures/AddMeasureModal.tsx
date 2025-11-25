import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { XMarkIcon } from '@heroicons/react/24/outline';
import { fetchMeasures, type CustomerMeasureCreateData } from '../../api/measureApi';

/**
 * Props för AddMeasureModal komponenten
 */
interface AddMeasureModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: CustomerMeasureCreateData) => void;
}

export default function AddMeasureModal({ isOpen, onClose, onSubmit }: AddMeasureModalProps) {
  // State för formuläret
  const [selectedMeasureId, setSelectedMeasureId] = useState<number | null>(null);
  const [frequency, setFrequency] = useState<string>('WEEKLY');
  const [occurrencesPerWeek, setOccurrencesPerWeek] = useState<number>(1);
  const [customDuration, setCustomDuration] = useState<number | null>(null);

  // Hämta alla aktiva measures från katalogen
  const { data: measures = [], isLoading: measuresLoading } = useQuery({
    queryKey: ['measures'],
    queryFn: () => fetchMeasures(true),
    enabled: isOpen,
  });

  // Hitta den valda measure för att visa default duration
  const selectedMeasure = measures.find((m) => m.id === selectedMeasureId);

  /**
   * Återställer formuläret till default-värden.
   */
  const resetForm = () => {
    setSelectedMeasureId(null);
    setFrequency('WEEKLY');
    setOccurrencesPerWeek(1);
    setCustomDuration(null);
  };

  /**
   * Hanterar stängning av modal.
   */
  const handleClose = () => {
    resetForm();
    onClose();
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

  // Om modal inte är öppen, rendera ingenting
  if (!isOpen) return null;

  // JSX - Modal UI
  return (
    // Backdrop - mörk bakgrund som täcker hela skärmen
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      {/* Modal Container */}
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

        {/* Body */}
        <div className="space-y-4 p-4">
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
                  // Återställ custom duration när man byter measure
                  setCustomDuration(null);
                }}
                className="w-full rounded-lg border border-gray-300 p-2 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 focus:outline-none"
              >
                <option value="">-- Välj insats --</option>
                {measures.map((measure) => (
                  <option key={measure.id} value={measure.id}>
                    {measure.name} ({measure.defaultDuration} min)
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
                Standard tid: {selectedMeasure.defaultDuration} minuter
              </p>
            </div>
          )}

          {/* Duration Input */}
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">Tid (minuter)</label>
            <input
              type="number"
              min="1"
              placeholder={selectedMeasure?.defaultDuration?.toString() ?? 'Välj insats först'}
              value={customDuration ?? ''}
              onChange={(e) => {
                const val = e.target.value ? Number(e.target.value) : null;
                setCustomDuration(val);
              }}
              className="w-full rounded-lg border border-gray-300 p-2 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 focus:outline-none"
            />
            <p className="mt-1 text-xs text-gray-500">
              Lämna tomt för standardtid ({selectedMeasure?.defaultDuration ?? '?'} min)
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
        </div>

        {/* Footer */}
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
      </div>
    </div>
  );
}
