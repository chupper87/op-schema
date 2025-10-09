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

export default function EmployeeCard({ id, name, phone, employmentType, employmentDegree, weeklyHours, isSummerWorker, role, isActive }: EmployeeCardProps) {
    return (
        <div key={id} className={`rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow cursor-pointer ${
            isActive ? 'bg-white' : 'bg-gray-200 opacity-60'
        }`}>
            <h3 className="text-lg font-bold text-indigo-900">
                {name}
                {isSummerWorker && (
                    <span className="text-emerald-500 text-xs ml-2">- Sommararbetare</span>
                )}
            </h3>
            <p className="text-gray-600 text-sm mt-1">{role}</p>
            <p className="text-gray-600 text-sm mt-1">{employmentType === "Hourly" ? "Timanställd" : "Månadsanställd"}</p>
            <p className="text-gray-600 text-sm mt-1">{phone}</p>
            <p className="text-gray-600 text-sm mt-1">Anställningsgrad: {employmentDegree}%</p>
            <p className="text-gray-600 text-sm mt-1">Veckoarbetstid: {weeklyHours}h</p>
        </div>
    );
}