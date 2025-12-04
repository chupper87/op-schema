import { TrashIcon } from '@heroicons/react/24/outline';

interface MeasureCardProps {
  id: number;
  name: string;
  defaultDuration: number;
  text: string | null;
  timeOfDay: string | null;
  timeFlexibility: string | null;
  isActive: boolean;
  onDelete?: (id: number) => void;
}

export default function MeasureCard({
  id,
  name,
  defaultDuration,
  text,
  timeOfDay,
  timeFlexibility,
  isActive,
  onDelete,
}: MeasureCardProps) {
  return (
    <div
      className={`relative rounded-xl p-4 shadow-md transition-shadow hover:shadow-lg ${
        isActive ? 'bg-white' : 'bg-gray-200 opacity-60'
      }`}
    >
      {/* Delete-knapp */}
      {onDelete && (
        <button
          onClick={(e) => {
            e.stopPropagation(); // Förhindra att card-click triggas
            onDelete(id);
          }}
          className="absolute top-2 right-2 rounded-lg p-1 text-gray-400 hover:bg-red-50 hover:text-red-600"
          title="Radera insats"
        >
          <TrashIcon className="h-5 w-5" />
        </button>
      )}

      <h3 className="text-lg font-bold text-indigo-900">{name}</h3>
      <p className="mt-1 text-sm font-medium text-indigo-700">{defaultDuration} minuter</p>

      {text && <p className="mt-2 text-sm text-gray-600">{text}</p>}

      <div className="mt-3 flex flex-wrap gap-2">
        {timeOfDay && (
          <span className="rounded-full bg-indigo-100 px-2 py-1 text-xs text-indigo-700">
            {timeOfDay}
          </span>
        )}
        {timeFlexibility && (
          <span className="rounded-full bg-gray-100 px-2 py-1 text-xs text-gray-600">
            {timeFlexibility}
          </span>
        )}
      </div>
    </div>
  );
}
