import TimeBudget from './TimeBudget';

interface CustomerMeasuresProps {
  customerId: number;
  approvedHours: number;
}

export default function CustomerMeasures({
  // customerId: _customerId,
  approvedHours,
}: CustomerMeasuresProps) {
  const plannedHours = 0;
  return (
    <div className="space-y-8">
      <TimeBudget approvedHours={approvedHours} plannedHours={plannedHours} />

      <div className="flex justify-end">
        <button className="rounded-lg bg-indigo-900 px-4 py-2 text-white hover:bg-indigo-800">
          + Lägg till insats
        </button>
      </div>

      <div className="text-center text-gray-500">Inga insatser tillagda än.</div>
    </div>
  );
}
