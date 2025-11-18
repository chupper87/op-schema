interface MeasureCardProps {
  id: number;
  name: string;
  defaultDuration: number;
  text: string;
  timeOfDay: string;
  timeFlexibility: string;
  isActive: boolean;
}

export default function MeasureCard({
  name,
  defaultDuration,
  text,
  timeOfDay,
  timeFlexibility,
  isActive,
}: MeasureCardProps) {
  return (
    <div
      className={`cursor-pointer rounded-xl p-4 shadow-md transition-shadow hover:shadow-lg ${
        isActive ? 'bg-white' : 'bg-gray-200 opacity-60'
      }`}
    >
      <h3 className="text-lg font-bold text-indigo-900">{name}</h3>
      <p className="mt-1 text-sm text-gray-600">{defaultDuration}</p>
      <p className="mt-1 text-sm text-gray-600">{text}</p>
      <p className="mt-1 text-sm text-gray-600">{timeOfDay}</p>
      <p className="mt-1 text-sm text-gray-600">{timeFlexibility}</p>
    </div>
  );
}
