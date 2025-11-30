import { TrashIcon } from '@heroicons/react/24/outline';
import { type CustomerMeasure } from '../../api/measureApi';

interface MeasureListProps {
  measures: CustomerMeasure[];
  onRemove: (id: number) => void;
}

/**
 * Formaterar frekvens för display.
 */
function formatFrequency(frequency: string, occurrences: number | null): string {
  switch (frequency) {
    case 'DAILY':
      return 'dagligen';
    case 'MONTHLY':
      return `${occurrences ?? 1} ggr/månad`;
    case 'WEEKLY':
    default:
      return `${occurrences ?? 0} ggr/vecka`;
  }
}

/**
 * Beräknar timmar per månad baserat på frekvens.
 */
function calculateHoursPerMonth(duration: number, frequency: string, occurrences: number): number {
  switch (frequency) {
    case 'DAILY':
      // Dagligen = 7 ggr/vecka × 4.3 veckor = 30.1 ggr/månad
      return (duration * 7 * 4.3) / 60;
    case 'MONTHLY':
      // Månadsvis = occurrences gånger per månad
      return (duration * occurrences) / 60;
    case 'WEEKLY':
    default:
      // Veckovis = occurrences × 4.3 veckor
      return (duration * occurrences * 4.3) / 60;
  }
}

export default function MeasureList({ measures, onRemove }: MeasureListProps) {
  if (measures.length === 0) {
    return (
      <div className="rounded-xl border-2 border-dashed border-gray-200 p-8 text-center">
        <p className="text-gray-500">Inga insatser tillagda än.</p>
        <p className="text-sm text-gray-400">Klicka på "Lägg till insats" för att börja planera.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {measures.map((measure) => {
        const duration = measure.customer_duration ?? 0;
        const occurrences = measure.occurrences_per_week ?? 0;
        const hoursPerMonth = calculateHoursPerMonth(duration, measure.frequency, occurrences);

        return (
          <div
            key={measure.id}
            className="flex items-center justify-between rounded-xl bg-white p-4 shadow-sm ring-1 ring-gray-100 transition-shadow hover:shadow-md"
          >
            <div>
              <h4 className="font-bold text-indigo-900">{measure.measure_name}</h4>
              <p className="text-sm text-gray-600">
                {duration} minuter, {formatFrequency(measure.frequency, occurrences)}
              </p>
            </div>

            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="font-bold text-indigo-900">{hoursPerMonth.toFixed(2)} h/mån</p>
              </div>

              <button
                onClick={() => onRemove(measure.id)}
                className="cursor-pointer rounded-lg p-2 text-gray-400 hover:bg-red-50 hover:text-red-600"
                title="Ta bort insats"
              >
                <TrashIcon className="h-5 w-5" />
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
}
