import Header from '../components/Header';
import WelcomeMessage from '../features/dashboard/components/WelcomeMessage';

export default function HomePage() {
  return (
    <div className="flex min-h-screen flex-col bg-indigo-100">
      <Header />

      <div className="flex-1 p-6 md:p-8">
        <div className="mx-auto max-w-7xl">
          <WelcomeMessage userName="Daniel" />

          {/* Stats Cards - Responsive grid */}
          <div className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 lg:grid-cols-3">
            <div className="rounded-xl bg-white p-6 shadow-md transition-shadow hover:shadow-lg">
              <h3 className="mb-2 text-sm font-semibold text-gray-500">Vårdtagare</h3>
              <p className="text-3xl font-bold text-indigo-900">45</p>
              <p className="mt-2 text-sm text-green-600">+3 denna vecka</p>
            </div>

            <div className="rounded-xl bg-white p-6 shadow-md transition-shadow hover:shadow-lg">
              <h3 className="mb-2 text-sm font-semibold text-gray-500">Schemalagt idag</h3>
              <p className="text-3xl font-bold text-indigo-900">12</p>
              <p className="mt-2 text-sm text-blue-600">3 kvar att utföra</p>
            </div>

            <div className="rounded-xl bg-white p-6 shadow-md transition-shadow hover:shadow-lg">
              <h3 className="mb-2 text-sm font-semibold text-gray-500">Kommande besök</h3>
              <p className="text-3xl font-bold text-indigo-900">8</p>
              <p className="mt-2 text-sm text-orange-600">Nästa 24 timmar</p>
            </div>
          </div>

          {/* Bigger sections */}
          <div className="mt-6 grid grid-cols-1 gap-4 md:gap-6 lg:grid-cols-2">
            <div className="min-h-[300px] rounded-xl bg-white p-6 shadow-md">
              <h2 className="mb-4 text-xl font-bold text-indigo-900">Dagens Schema</h2>
              <p className="text-gray-600">Här visas dagens schemalagda aktiviteter...</p>
            </div>

            <div className="min-h-[300px] rounded-xl bg-white p-6 shadow-md">
              <h2 className="mb-4 text-xl font-bold text-indigo-900">Senaste Aktivitet</h2>
              <p className="text-gray-600">Här visas senaste uppdateringar och händelser...</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
