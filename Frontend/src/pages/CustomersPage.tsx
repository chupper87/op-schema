import { useState } from "react";
import Header from "../components/Header";
import { Plus } from "phosphor-react";

export default function CustomersPage() {
    const [showForm, setShowForm] = useState(false);
    
    // Mockdata för att börja med
    const [customers, setCustomers] = useState([
        { id: 1, name: "Anna Andersson", personalNumber: "19850615-1234", address: "Storgatan 1", phone: "070-1234567" },
        { id: 2, name: "Bengt Berg", personalNumber: "19720320-5678", address: "Lillgatan 5", phone: "070-9876543" },
    ]);

    return (
        <div className="bg-indigo-100 flex flex-col min-h-screen">
            <Header />
            
            <div className="flex-1 p-6 md:p-8">
                <div className="max-w-7xl mx-auto">
                    {/* Header med knapp */}
                    <div className="flex justify-between items-center mb-6">
                        <h1 className="text-3xl font-bold text-indigo-900">Vårdtagare</h1>
                        <button 
                            onClick={() => setShowForm(true)}
                            className=" cursor-pointer flex items-center gap-2 bg-indigo-900 text-white px-4 py-2 rounded-lg hover:bg-indigo-800 transition-colors"
                        >
                            <Plus size={20} weight="bold" />
                            Lägg till vårdtagare
                        </button>
                    </div>

                    {/* Kundlista */}
                    <div className="bg-white rounded-xl shadow-md overflow-hidden">
                        <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Namn
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Personnummer
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Adress
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Telefon
                                    </th>
                                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Åtgärder
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                                {customers.map((customer) => (
                                    <tr key={customer.id} className="hover:bg-gray-50">
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                            {customer.name}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                            {customer.personalNumber}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                            {customer.address}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                            {customer.phone}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                            <button className="text-indigo-600 hover:text-indigo-900 mr-4">
                                                Redigera
                                            </button>
                                            <button className="text-red-600 hover:text-red-900">
                                                Ta bort
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    {/* Tom lista meddelande */}
                    {customers.length === 0 && (
                        <div className="bg-white rounded-xl shadow-md p-12 text-center">
                            <p className="text-gray-500">Inga vårdtagare ännu. Lägg till din första!</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

