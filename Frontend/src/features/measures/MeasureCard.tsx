interface MeasureCardProps {
    id: number;
    name: string;
    default_duration: number;
    text: string;
    time_of_day: string;
    time_flexibility: string;
    is_active: boolean;
}

export default function MeasureCard({ id, name, default_duration, text, time_of_day, time_flexibility, is_active }: MeasureCardProps) {
    return (
        <div key={id} className={`rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow cursor-pointer ${
            is_active ? 'bg-white' : 'bg-gray-200 opacity-60'
        }`}>
            <h3 className="text-lg font-bold text-indigo-900">{name}</h3>
            <p className="text-gray-600 text-sm mt-1">{default_duration}</p>
            <p className="text-gray-600 text-sm mt-1">{text}</p>
            <p className="text-gray-600 text-sm mt-1">{time_of_day}</p>
            <p className="text-gray-600 text-sm mt-1">{time_flexibility}</p>
        </div>
    );
}