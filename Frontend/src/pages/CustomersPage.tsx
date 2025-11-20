import { useState } from 'react';
import { Dialog, DialogPanel, DialogBackdrop } from '@headlessui/react';
import Header from '../components/Header';
import CustomerForm from '../features/customers/CustomerForm';
import { Plus } from 'phosphor-react';

export default function CustomersPage() {
  const [showForm, setShowForm] = useState(false);

  // TODO: Implement customer creation and update logic setCustomers add it again
  const [customers] = useState([
    {
      id: 1,
      name: 'Anna Andersson',
      personalNumber: '19850615-1234',
      address: 'Storgatan 1',
      phone: '070-1234567',
    },
    {
      id: 2,
      name: 'Bengt Berg',
      personalNumber: '19720320-5678',
      address: 'Lillgatan 5',
      phone: '070-9876543',
    },
  ]);

  return (
    <div className="flex min-h-screen flex-col bg-indigo-100">
      <Header />

      <div className="flex-1 p-6 md:p-8">
        <div className="mx-auto max-w-7xl">
          {/* Header med knapp */}
          <div className="mb-6 flex items-center justify-between">
            <h1 className="text-3xl font-bold text-indigo-900">Vårdtagare</h1>
            <button
              onClick={() => setShowForm(true)}
              className="flex cursor-pointer items-center gap-2 rounded-lg bg-indigo-900 px-4 py-2 text-white transition-colors hover:bg-indigo-800"
            >
              <Plus size={20} weight="bold" />
              Lägg till vårdtagare
            </button>
          </div>

          {/* Kundlista */}
          <div className="overflow-hidden rounded-xl bg-white shadow-md">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase">
                    Namn
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase">
                    Personnummer
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase">
                    Adress
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase">
                    Telefon
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium tracking-wider text-gray-500 uppercase">
                    Åtgärder
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 bg-white">
                {customers.map((customer) => (
                  <tr key={customer.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm font-medium whitespace-nowrap text-gray-900">
                      {customer.name}
                    </td>
                    <td className="px-6 py-4 text-sm whitespace-nowrap text-gray-500">
                      {customer.personalNumber}
                    </td>
                    <td className="px-6 py-4 text-sm whitespace-nowrap text-gray-500">
                      {customer.address}
                    </td>
                    <td className="px-6 py-4 text-sm whitespace-nowrap text-gray-500">
                      {customer.phone}
                    </td>
                    <td className="px-6 py-4 text-right text-sm font-medium whitespace-nowrap">
                      <button className="mr-4 text-indigo-600 hover:text-indigo-900">
                        Redigera
                      </button>
                      <button className="text-red-600 hover:text-red-900">Ta bort</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Tom lista meddelande */}
          {customers.length === 0 && (
            <div className="rounded-xl bg-white p-12 text-center shadow-md">
              <p className="text-gray-500">Inga vårdtagare ännu. Lägg till din första!</p>
            </div>
          )}
        </div>
      </div>

      {/* Drawer */}
      <Dialog open={showForm} onClose={() => {}} className="relative z-50">
        {/* Backdrop */}
        <DialogBackdrop className="fixed inset-0 bg-black/20 transition-opacity duration-300 ease-out data-[closed]:opacity-0" />

        {/* Drawer Panel */}
        <div className="fixed inset-0 overflow-hidden">
          <div className="absolute inset-0 overflow-hidden">
            <div className="pointer-events-none fixed inset-y-0 right-0 flex max-w-full pl-10">
              <DialogPanel className="pointer-events-auto w-screen max-w-md transform transition duration-300 ease-out data-[closed]:translate-x-full">
                <div className="flex h-full flex-col bg-white shadow-xl">
                  <CustomerForm />
                </div>
              </DialogPanel>
            </div>
          </div>
        </div>
      </Dialog>
    </div>
  );
}
