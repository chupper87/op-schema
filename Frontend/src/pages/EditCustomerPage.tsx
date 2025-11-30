import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  fetchCustomerById,
  updateCustomer,
  deleteCustomer,
  type CustomerCreateData,
} from '../api/customerApi';
import CustomerForm from '../features/customers/CustomerForm';
import CustomerMeasures from '../features/measures/CustomerMeasures';
import Header from '../components/Header';
import { ArrowLeft, Trash } from 'phosphor-react';

export default function EditCustomerPage() {
  const { id } = useParams<{ id: string }>();
  const [activeTab, setActiveTab] = useState<'details' | 'planning'>('details');
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const customerId = Number(id);

  const {
    data: customer,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ['customer', customerId],
    queryFn: () => fetchCustomerById(customerId),
    enabled: !!customerId,
  });

  const updateMutation = useMutation({
    mutationFn: (data: Partial<CustomerCreateData>) => updateCustomer(customerId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['customers'] });
      queryClient.invalidateQueries({ queryKey: ['customer', customerId] });
      navigate('/customers');
    },
  });

  const deleteMutation = useMutation({
    mutationFn: () => deleteCustomer(customerId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['customers'] });
      navigate('/customers');
    },
  });

  const handleUpdate = (data: CustomerCreateData) => {
    updateMutation.mutate(data);
  };

  const handleDelete = () => {
    if (window.confirm('Är du säker på att du vill ta bort kunden? Detta går inte att ångra.')) {
      deleteMutation.mutate();
    }
  };

  if (isLoading) {
    return (
      <div className="flex min-h-screen flex-col bg-indigo-100">
        <Header />
        <div className="flex-1 p-6 md:p-8">
          <div className="mx-auto max-w-3xl rounded-xl bg-white p-12 text-center shadow-md">
            <p className="text-gray-500">Laddar...</p>
          </div>
        </div>
      </div>
    );
  }

  if (isError || !customer) {
    return (
      <div className="flex min-h-screen flex-col bg-indigo-100">
        <Header />
        <div className="flex-1 p-6 md:p-8">
          <div className="mx-auto max-w-3xl rounded-xl bg-white p-12 text-center shadow-md">
            <p className="text-red-500">Kunde inte hämta kunden.</p>
            <button
              onClick={() => navigate('/customers')}
              className="mt-4 text-indigo-600 hover:text-indigo-900"
            >
              Gå tillbaka
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col bg-indigo-100">
      <Header />

      <div className="flex-1 p-6 md:p-8">
        <div className="mx-auto max-w-3xl">
          <button
            onClick={() => navigate('/customers')}
            className="mb-6 flex items-center gap-2 font-bold text-indigo-900 hover:text-indigo-700"
          >
            <ArrowLeft size={20} />
            Tillbaka
          </button>

          <div className="overflow-hidden rounded-xl bg-white shadow-md">
            <div className="border-b border-gray-200 px-6 py-4">
              <h1 className="text-2xl font-bold text-indigo-900">
                {customer.first_name} {customer.last_name}
              </h1>
            </div>

            {/* Tab Navigation */}
            <div className="flex border-b border-gray-200">
              <button
                onClick={() => setActiveTab('details')}
                className={`flex-1 cursor-pointer px-6 py-3 text-sm font-medium transition-colors ${
                  activeTab === 'details'
                    ? 'border-b-2 border-indigo-900 text-indigo-900'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Grunduppgifter
              </button>
              <button
                onClick={() => setActiveTab('planning')}
                className={`flex-1 cursor-pointer px-6 py-3 text-sm font-medium transition-colors ${
                  activeTab === 'planning'
                    ? 'border-b-2 border-indigo-900 text-indigo-900'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Planering
              </button>
            </div>

            <div className="p-6">
              {activeTab === 'details' ? (
                <CustomerForm
                  initialData={customer}
                  onSubmit={handleUpdate}
                  onCancel={() => navigate('/customers')}
                  submitLabel="Spara ändringar"
                />
              ) : (
                <CustomerMeasures customerId={customerId} approvedHours={customer.approved_hours} />
              )}
            </div>

            <div className="bg-gray-50 px-6 py-4">
              <div className="rounded-lg border border-red-200 bg-red-50 p-4">
                <button
                  onClick={handleDelete}
                  className="mt-4 flex cursor-pointer items-center gap-2 rounded-lg bg-red-600 px-4 py-2 text-white transition-colors hover:bg-red-700"
                >
                  <Trash size={20} />
                  Radera kund
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
