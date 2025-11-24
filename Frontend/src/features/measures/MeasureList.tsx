import { TrashIcon } from '@heroicons/react/24/outline';
import { type CustomerMeasure } from '../../api/measureApi';

interface MeasureListProps {
  measures: CustomerMeasure[];
  onRemove: (id: number) => void;
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
      {measures.map((measure) => (
        <div
          key={measure.id}
          className="flex items-center justify-between rounded-xl bg-white p-4 shadow-sm ring-1 ring-gray-100 transition-shadow hover:shadow-md"
        >
          <div>
            <h4 className="font-bold text-indigo-900">{measure.measure_name}</h4>
            <p className="text-sm text-gray-600">
              {measure.customer_duration ?? 0} minuter, {measure.occurrences_per_week ?? 0}{' '}
              ggr/vecka
            </p>
          </div>

          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="font-bold text-indigo-900">
                {/* Räkna ut månadstotalen: (minuter * antal/vecka * 4.3 veckor) / 60 minuter */}
                {(
                  ((measure.customer_duration ?? 0) * (measure.occurrences_per_week ?? 0) * 4.3) /
                  60
                ).toFixed(2)}{' '}
                h/mån
              </p>
            </div>

            <button
              onClick={() => onRemove(measure.id)}
              className="rounded-lg p-2 text-gray-400 hover:bg-red-50 hover:text-red-600"
              title="Ta bort insats"
            >
              <TrashIcon className="h-5 w-5" />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
