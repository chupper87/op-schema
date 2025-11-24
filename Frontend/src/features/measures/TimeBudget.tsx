interface TimeBudgetProps {
  approvedHours: number;
  plannedHours: number;
}

export default function TimeBudget({ approvedHours, plannedHours }: TimeBudgetProps) {
  // Räkna ut procenten, men maxa den visuellt på 100% så den inte spräcker layouten
  const percentage = Math.min((plannedHours / approvedHours) * 100, 100);

  // Bestäm färg baserat på hur mycket tid som är använd
  // Grön: < 90%, Gul: 90-100%, Röd: > 100%
  let colorClass = 'bg-green-500';
  if (plannedHours > approvedHours) {
    colorClass = 'bg-red-500';
  } else if (percentage > 90) {
    colorClass = 'bg-yellow-500';
  }

  return (
    <div className="rounded-xl bg-white p-6 shadow-sm ring-1 ring-gray-200">
      <div className="mb-4 flex items-end justify-between">
        <div>
          <h3 className="text-lg font-bold text-indigo-900">Tidsbudget</h3>
          <p className="text-sm text-gray-500">Planerat vs Beviljat</p>
        </div>
        <div className="text-right">
          <span
            className={`text-2xl font-bold ${plannedHours > approvedHours ? 'text-red-600' : 'text-indigo-900'}`}
          >
            {plannedHours}
          </span>
          <span className="text-gray-500"> / {approvedHours} h/mån</span>
        </div>
      </div>

      {/* Progress Bar Container */}
      <div className="h-4 w-full overflow-hidden rounded-full bg-gray-100">
        {/* Progress Bar Fill */}
        <div
          className={`h-full transition-all duration-500 ease-out ${colorClass}`}
          style={{ width: `${percentage}%` }}
        />
      </div>

      {/* Varningstext om man övertrasserat */}
      {plannedHours > approvedHours && (
        <p className="mt-2 text-sm font-medium text-red-600">
          Obs! Du har planerat in mer tid än vad som är beviljat.
        </p>
      )}
    </div>
  );
}
