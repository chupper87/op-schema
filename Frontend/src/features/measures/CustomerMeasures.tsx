import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  fetchCustomerMeasures,
  deleteCustomerMeasure,
  type CustomerMeasure,
} from '../../api/measureApi';
import MeasureList from './MeasureList';
import TimeBudget from './TimeBudget';

interface CustomerMeasuresProps {
  customerId: number;
  approvedHours: number;
}

export default function CustomerMeasures({ customerId, approvedHours }: CustomerMeasuresProps) {
  const queryClient = useQueryClient();

  const {
    data: measures = [],
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ['customerMeasures', customerId],
    queryFn: () => fetchCustomerMeasures(customerId),
  });

  const deleteMutation = useMutation({
    mutationFn: (customerMeasureId: number) => deleteCustomerMeasure(customerId, customerMeasureId),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ['customerMeasures', customerId],
      });
    },
  });

  const plannedHours = measures.reduce((total: number, measure: CustomerMeasure) => {
    const duration = measure.customer_duration ?? 0;
    const occurrences = measure.occurrences_per_week ?? 0;

    const hoursPerMonth = (duration * occurrences * 4.3) / 60;

    return total + hoursPerMonth;
  }, 0);

  const handleRemove = (customerMeasureId: number) => {
    deleteMutation.mutate(customerMeasureId);
  };

  if (isLoading) {
    return (
      <div className="flex justify-center p-8">
        <p className="text-gray-500">Laddar insatser...</p>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="rounded-lg bg-red-50 p-4">
        <p className="text-red-600">
          Kunde inte ladda insatser: {error instanceof Error ? error.message : 'Okänt fel'}
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Time Budget visar planerad vs beviljad tid */}
      <TimeBudget approvedHours={approvedHours} plannedHours={Number(plannedHours.toFixed(2))} />

      {/* Knapp för att lägga till ny insats (framtida implementation) */}
      <div className="flex justify-end">
        <button className="rounded-lg bg-indigo-900 px-4 py-2 text-white hover:bg-indigo-800">
          + Lägg till insats
        </button>
      </div>

      {/* Lista över insatser, eller tom state */}
      <MeasureList measures={measures} onRemove={handleRemove} />
    </div>
  );
}
