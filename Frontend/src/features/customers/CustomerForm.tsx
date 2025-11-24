import { useState, type FormEvent, useEffect } from 'react';

interface CustomerFormProps {
  initialData?: {
    first_name: string;
    last_name: string;
    key_number: number;
    address: string;
    care_level: 'high' | 'medium' | 'low';
    gender: 'male' | 'female' | 'unspecified';
    approved_hours: number;
  };
  onSubmit: (customer: {
    first_name: string;
    last_name: string;
    key_number: number;
    address: string;
    care_level: 'high' | 'medium' | 'low';
    gender: 'male' | 'female' | 'unspecified';
    approved_hours: number;
    is_active: boolean;
  }) => void;
  onCancel: () => void;
  submitLabel?: string;
}

export default function CustomerForm({
  onSubmit,
  onCancel,
  initialData,
  submitLabel = 'Lägg till',
}: CustomerFormProps) {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    key_number: '',
    address: '',
    care_level: 'medium' as 'high' | 'medium' | 'low',
    gender: 'unspecified' as 'male' | 'female' | 'unspecified',
    approved_hours: '',
  });

  useEffect(() => {
    if (initialData) {
      setFormData({
        first_name: initialData.first_name,
        last_name: initialData.last_name,
        key_number: initialData.key_number.toString(),
        address: initialData.address,
        care_level: initialData.care_level,
        gender: initialData.gender,
        approved_hours: initialData.approved_hours.toString(),
      });
    }
  }, [initialData]);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();

    // Convert key_number and approved_hours to numbers
    const customerData = {
      first_name: formData.first_name,
      last_name: formData.last_name,
      key_number: Number(formData.key_number),
      address: formData.address,
      care_level: formData.care_level,
      gender: formData.gender,
      approved_hours: Number(formData.approved_hours),
      is_active: true,
    };

    onSubmit(customerData);
    setFormData({
      first_name: '',
      last_name: '',
      key_number: '',
      address: '',
      care_level: 'medium',
      gender: 'unspecified',
      approved_hours: '',
    });
  };

  return (
    <div className="flex h-full flex-col">
      <form onSubmit={handleSubmit} className="flex flex-1 flex-col overflow-y-auto">
        <div className="flex-1 space-y-6 p-6">
          {/* First Name Field */}
          <div>
            <label htmlFor="first_name" className="mb-2 block text-sm font-medium text-gray-700">
              Förnamn *
            </label>
            <input
              type="text"
              id="first_name"
              required
              value={formData.first_name}
              onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
              className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              placeholder="Anna"
            />
          </div>

          {/* Last Name Field */}
          <div>
            <label htmlFor="last_name" className="mb-2 block text-sm font-medium text-gray-700">
              Efternamn *
            </label>
            <input
              type="text"
              id="last_name"
              required
              value={formData.last_name}
              onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
              className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              placeholder="Andersson"
            />
          </div>

          {/* Key Number Field */}
          <div>
            <label htmlFor="key_number" className="mb-2 block text-sm font-medium text-gray-700">
              Nyckelnummer *
            </label>
            <input
              type="number"
              id="key_number"
              required
              value={formData.key_number}
              onChange={(e) => setFormData({ ...formData, key_number: e.target.value })}
              className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              placeholder="123"
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
              value={formData.address}
              onChange={(e) => setFormData({ ...formData, address: e.target.value })}
              className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              placeholder="Storgatan 1"
            />
          </div>

          {/* Gender Field */}
          <div>
            <label htmlFor="gender" className="mb-2 block text-sm font-medium text-gray-700">
              Kön *
            </label>
            <select
              id="gender"
              required
              value={formData.gender}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  gender: e.target.value as 'male' | 'female' | 'unspecified',
                })
              }
              className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            >
              <option value="unspecified">Ospecificerat</option>
              <option value="male">Man</option>
              <option value="female">Kvinna</option>
            </select>
          </div>

          {/* Care Level Field */}
          <div>
            <label htmlFor="care_level" className="mb-2 block text-sm font-medium text-gray-700">
              Omsorgsnivå *
            </label>
            <select
              id="care_level"
              required
              value={formData.care_level}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  care_level: e.target.value as 'high' | 'medium' | 'low',
                })
              }
              className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            >
              <option value="low">Låg</option>
              <option value="medium">Medel</option>
              <option value="high">Hög</option>
            </select>
          </div>

          {/* Approved Hours Field */}
          <div>
            <label
              htmlFor="approved_hours"
              className="mb-2 block text-sm font-medium text-gray-700"
            >
              Beviljade timmar *
            </label>
            <input
              type="number"
              id="approved_hours"
              required
              step="0.5"
              min="0"
              value={formData.approved_hours}
              onChange={(e) => setFormData({ ...formData, approved_hours: e.target.value })}
              className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              placeholder="40"
            />
          </div>
        </div>

        {/* Footer Actions */}
        <div className="flex gap-3 border-t border-gray-200 px-6 py-4">
          <button
            type="button"
            onClick={onCancel}
            className="flex-1 cursor-pointer rounded-lg border border-gray-300 px-4 py-2 text-gray-700 transition-colors hover:bg-gray-50"
          >
            Avbryt
          </button>
          <button
            type="submit"
            className="flex-1 cursor-pointer rounded-lg bg-indigo-900 px-4 py-2 text-white transition-colors hover:bg-indigo-800"
          >
            {submitLabel}
          </button>
        </div>
      </form>
    </div>
  );
}
