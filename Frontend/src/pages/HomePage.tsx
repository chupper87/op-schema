import Header from "../components/Header";
import WelcomeMessage from "../features/dashboard/components/WelcomeMessage";

export default function HomePage() {
    return (
        <div className="bg-indigo-100 flex flex-col min-h-screen">
            <Header />

            <div className="flex-1 p-6 md:p-8">
                <div className="max-w-7xl mx-auto">
                    <WelcomeMessage userName="Daniel" />

                    {/* Stats Cards - Responsive grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 mt-6">
                        <div className="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow">
                            <h3 className="text-gray-500 text-sm font-semibold mb-2">Vårdtagare</h3>
                            <p className="text-3xl font-bold text-indigo-900">45</p>
                            <p className="text-green-600 text-sm mt-2">+3 denna vecka</p>
                        </div>

                        <div className="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow">
                            <h3 className="text-gray-500 text-sm font-semibold mb-2">Schemalagt idag</h3>
                            <p className="text-3xl font-bold text-indigo-900">12</p>
                            <p className="text-blue-600 text-sm mt-2">3 kvar att utföra</p>
                        </div>

                        <div className="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow">
                            <h3 className="text-gray-500 text-sm font-semibold mb-2">Kommande besök</h3>
                            <p className="text-3xl font-bold text-indigo-900">8</p>
                            <p className="text-orange-600 text-sm mt-2">Nästa 24 timmar</p>
                        </div>
                    </div>

                    {/* Bigger sections */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-6 mt-6">
                        <div className="bg-white rounded-xl p-6 shadow-md min-h-[300px]">
                            <h2 className="text-xl font-bold text-indigo-900 mb-4">Dagens Schema</h2>
                            <p className="text-gray-600">Här visas dagens schemalagda aktiviteter...</p>
                        </div>

                        <div className="bg-white rounded-xl p-6 shadow-md min-h-[300px]">
                            <h2 className="text-xl font-bold text-indigo-900 mb-4">Senaste Aktivitet</h2>
                            <p className="text-gray-600">Här visas senaste uppdateringar och händelser...</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
