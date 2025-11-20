import { X } from 'phosphor-react';
import { useState, type FormEvent } from 'react';

interface CustomerFormProps {
  onSubmit: (customer: {
    name: string;
    personalNumber: string;
    address: string;
    phone: string;
  }) => void;
  onCancel: () => void;
}

export default function CustomerForm({ onSubmit, onCancel }: CustomerFormProps) {
  const [formData, setFormData] = useState({
    name: '',
    personalNumber: '',
    address: '',
    phone: '',
  });

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
    setFormData({ name: '', personalNumber: '', address: '', phone: '' });
  };

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-gray-200 px-6 py-4">
        <h2 className="text-xl font-bold text-indigo-900">Lägg till vårdtagare</h2>
        <button
          onClick={onCancel}
          className="rounded-lg p-2 text-gray-400 transition-colors hover:bg-gray-100 hover:text-gray-600"
          aria-label="Stäng"
        >
          <X size={24} weight="bold" />
        </button>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="flex flex-1 flex-col overflow-y-auto">
        <div className="flex-1 space-y-6 p-6">
          {/* Name Field */}
          <div>
            <label htmlFor="name" className="mb-2 block text-sm font-medium text-gray-700">
              Namn *
            </label>
            <input
              type="text"
              id="name"
              required
              className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              placeholder="Anna Andersson"
            />
          </div>

          {/* Personal Number Field */}
          <div>
            <label
              htmlFor="personalNumber"
              className="mb-2 block text-sm font-medium text-gray-700"
            >
              Personnummer *
            </label>
            <input
              type="text"
              id="personalNumber"
              required
              className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              placeholder="ÅÅÅÅMMDD-XXXX"
            />
          </div>

          {/* Address Field */}
          <div>
            <label htmlFor="address" className="mb-2 block text-sm font-medium text-gray-700">
              Adress *
            </label>
            <input
              type="text"
              id="address"
              required
              className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              placeholder="Storgatan 1"
            />
          </div>

          {/* Phone Field */}
          <div>
            <label htmlFor="phone" className="mb-2 block text-sm font-medium text-gray-700">
              Telefon *
            </label>
            <input
              type="tel"
              id="phone"
              required
              className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              placeholder="070-1234567"
            />
          </div>
        </div>

        {/* Footer Actions */}
        <div className="flex gap-3 border-t border-gray-200 px-6 py-4">
          <button
            type="button"
            className="flex-1 rounded-lg border border-gray-300 px-4 py-2 text-gray-700 transition-colors hover:bg-gray-50"
          >
            Avbryt
          </button>
          <button
            type="submit"
            className="flex-1 rounded-lg bg-indigo-900 px-4 py-2 text-white transition-colors hover:bg-indigo-800"
          >
            Lägg till
          </button>
        </div>
      </form>
    </div>
  );
}
