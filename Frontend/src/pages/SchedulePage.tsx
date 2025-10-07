import Header from "../components/Header";

export default function SchedulePage() {
    return (
        <div>
            <Header />
            <div className="p-8">
                <h1 className="text-3xl font-bold text-indigo-900">Planering</h1>
                <p className="mt-4 text-gray-600">Här visas schemaläggning och planering.</p>
            </div>
        </div>
    );
}

