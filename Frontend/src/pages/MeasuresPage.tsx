import Header from '../components/Header';
import { Plus } from 'phosphor-react';
import MeasureCard from '../features/measures/MeasureCard';
import { useQuery, useMutation } from '@tanstack/react-query';
import { useQueryClient } from '@tanstack/react-query';
import { deleteMeasure } from '../api/measureApi';
import { fetchMeasures } from '../api/measureApi';

export default function MeasuresPage() {
  const queryClient = useQueryClient();

  // Hämta alla measures från backend
  const {
    data: measures = [],
    isLoading,
    isError,
  } = useQuery({
    queryKey: ['measures'],
    queryFn: () => fetchMeasures(true), // true = bara aktiva
  });

  // Mutation för att radera measure
  const deleteMutation = useMutation({
    mutationFn: (measureId: number) => deleteMeasure(measureId),
    onSuccess: () => {
      // Uppdatera listan efter radering
      queryClient.invalidateQueries({ queryKey: ['measures'] });
    },
    onError: (error) => {
      // TODO: Visa toast/meddelande om fel
      console.error('Kunde inte radera:', error);
      alert('Kunde inte radera insatsen. Den kanske används av en kund?');
    },
  });

  // Handler för delete
  const handleDelete = (measureId: number) => {
    if (window.confirm('Är du säker på att du vill radera denna insats?')) {
      deleteMutation.mutate(measureId);
    }
  };

  if (isLoading) {
    return (
      <div className="flex min-h-screen flex-col bg-indigo-100">
        <Header />
        <div className="flex flex-1 items-center justify-center">
          <p className="text-gray-500">Laddar insatser...</p>
        </div>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="flex min-h-screen flex-col bg-indigo-100">
        <Header />
        <div className="flex flex-1 items-center justify-center">
          <p className="text-red-600">Kunde inte ladda insatser.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col bg-indigo-100">
      <Header />

      <div className="flex-1 p-8 md:p-8">
        <div className="mx-auto max-w-7xl">
          {/* Header */}
          <div className="mb-6 flex items-center justify-between">
            <h1 className="text-3xl font-bold text-indigo-900">Insatser</h1>
            <div className="flex items-center gap-3">
              <button className="flex cursor-pointer items-center gap-2 rounded-lg bg-indigo-900 px-4 py-2 text-white transition-colors hover:bg-indigo-800">
                <Plus size={20} weight="bold" />
                Skapa insats
              </button>
            </div>
          </div>
          {/*Measures*/}

          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {measures.map((measure) => (
              <MeasureCard
                key={measure.id}
                id={measure.id}
                name={measure.name}
                defaultDuration={measure.default_duration}
                text={measure.text}
                timeOfDay={measure.time_of_day}
                timeFlexibility={'Flexibel'}
                isActive={true}
                onDelete={handleDelete}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
