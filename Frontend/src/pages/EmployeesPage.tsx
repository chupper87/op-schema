import Header from "../components/Header";

export default function EmployeesPage() {
    return (
        <div>
            <Header />
            <div className="p-8">
                <h1 className="text-3xl font-bold text-indigo-900">Medarbetare</h1>
                <p className="mt-4 text-gray-600">Här visas alla medarbetare.</p>
            </div>
        </div>
    );
}

