interface EmployeeCardProps {
    id: number;
    name: string;
    phone: string;
    employmentType: string;
    employmentDegree: number;
    weeklyHours: number;
    isSummerWorker: boolean;
    role: string;
}

export default function EmployeeCard({ id, name, phone, employmentType, employmentDegree, weeklyHours, isSummerWorker, role }: EmployeeCardProps) {
    return (
        <div key={id} className="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow cursor-pointer">
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