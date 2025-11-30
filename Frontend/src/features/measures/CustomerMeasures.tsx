import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  fetchCustomerMeasures,
  deleteCustomerMeasure,
  createCustomerMeasure,
  type CustomerMeasure,
  type CustomerMeasureCreateData,
} from '../../api/measureApi';
import MeasureList from './MeasureList';
import TimeBudget from './TimeBudget';
import AddMeasureModal from './AddMeasureModal';

interface CustomerMeasuresProps {
  customerId: number;
  approvedHours: number;
}

export default function CustomerMeasures({ customerId, approvedHours }: CustomerMeasuresProps) {
  // State för modal
  const [isModalOpen, setIsModalOpen] = useState(false);

  const queryClient = useQueryClient();

  // Hämta kundens measures
  const {
    data: measures = [],
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ['customerMeasures', customerId],
    queryFn: () => fetchCustomerMeasures(customerId),
  });

  // Mutation för att ta bort measure
  const deleteMutation = useMutation({
    mutationFn: (customerMeasureId: number) => deleteCustomerMeasure(customerId, customerMeasureId),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ['customerMeasures', customerId],
      });
    },
  });

  // Mutation för att lägga till measure
  const createMutation = useMutation({
    mutationFn: (data: CustomerMeasureCreateData) => createCustomerMeasure(customerId, data),
    onSuccess: () => {
      // Uppdatera listan efter lyckad skapelse
      queryClient.invalidateQueries({
        queryKey: ['customerMeasures', customerId],
      });
    },
  });

  /**
   * Beräknar timmar per månad baserat på frekvens.
   */
  const calculateHoursPerMonth = (
    duration: number,
    frequency: string,
    occurrences: number
  ): number => {
    switch (frequency) {
      case 'DAILY':
        return (duration * 7 * 4.3) / 60;
      case 'MONTHLY':
        return (duration * occurrences) / 60;
      case 'WEEKLY':
      default:
        return (duration * occurrences * 4.3) / 60;
    }
  };

  // Beräkna total planerad tid
  const plannedHours = measures.reduce((total: number, measure: CustomerMeasure) => {
    const duration = measure.customer_duration ?? 0;
    const occurrences = measure.occurrences_per_week ?? 0;
    const hoursPerMonth = calculateHoursPerMonth(duration, measure.frequency, occurrences);
    return total + hoursPerMonth;
  }, 0);

  // Handler för att ta bort measure
  const handleRemove = (customerMeasureId: number) => {
    deleteMutation.mutate(customerMeasureId);
  };

  // Handler för att lägga till measure (anropas från modal)
  const handleAddMeasure = (data: CustomerMeasureCreateData) => {
    createMutation.mutate(data);
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

      {/* Knapp för att öppna modal */}
      <div className="flex justify-end">
        <button
          onClick={() => setIsModalOpen(true)}
          className="cursor-pointer rounded-lg bg-indigo-900 px-4 py-2 text-white hover:bg-indigo-800"
        >
          + Lägg till insats
        </button>
      </div>

      {/* Lista över insatser, eller tom state */}
      <MeasureList measures={measures} onRemove={handleRemove} />

      {/* Modal för att lägga till ny insats */}
      <AddMeasureModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleAddMeasure}
      />
    </div>
  );
}
