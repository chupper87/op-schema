interface MeasureCardProps {
    id: number;
    name: string;
    defaultDuration: number;
    text: string;
    timeOfDay: string;
    timeFlexibility: string;
    isActive: boolean;
}

export default function MeasureCard({ name, defaultDuration, text, timeOfDay, timeFlexibility, isActive }: MeasureCardProps) {
    return (
        <div className={`rounded-xl p-4 shadow-md hover:shadow-lg transition-shadow cursor-pointer
            ${
            isActive ? 'bg-white' : 'bg-gray-200 opacity-60'
        }`}>
            <h3 className="text-lg font-bold text-indigo-900">{name}</h3>
            <p className="text-gray-600 text-sm mt-1">{defaultDuration}</p>
            <p className="text-gray-600 text-sm mt-1">{text}</p>
            <p className="text-gray-600 text-sm mt-1">{timeOfDay}</p>
            <p className="text-gray-600 text-sm mt-1">{timeFlexibility}</p>
        </div>
    );
}
