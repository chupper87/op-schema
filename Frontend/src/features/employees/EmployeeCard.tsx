interface EmployeeCardProps {
  id: number;
  name: string;
  phone: string;
  employmentType: string;
  employmentDegree: number;
  weeklyHours: number;
  isSummerWorker: boolean;
  role: string;
  isActive: boolean;
}

export default function EmployeeCard({
  id,
  name,
  phone,
  employmentType,
  employmentDegree,
  weeklyHours,
  isSummerWorker,
  role,
  isActive,
}: EmployeeCardProps) {
  return (
    <div
      key={id}
      className={`cursor-pointer rounded-xl p-6 shadow-md transition-shadow hover:shadow-lg ${
        isActive ? 'bg-white' : 'bg-gray-200 opacity-60'
      }`}
    >
      <h3 className="text-lg font-bold text-indigo-900">
        {name}
        {isSummerWorker && <span className="ml-2 text-xs text-emerald-500"> Sommararbetare</span>}
      </h3>
      <p className="mt-1 text-sm text-gray-600">{role}</p>
      <p className="mt-1 text-sm text-gray-600">
        {employmentType === 'Hourly' ? 'Timanställd' : 'Månadsanställd'}
      </p>
      <p className="mt-1 text-sm text-gray-600">{phone}</p>
      <p className="mt-1 text-sm text-gray-600">Anställningsgrad: {employmentDegree}%</p>
      <p className="mt-1 text-sm text-gray-600">Veckoarbetstid: {weeklyHours}h</p>
    </div>
  );
}
