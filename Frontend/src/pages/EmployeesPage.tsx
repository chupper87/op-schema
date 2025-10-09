import { useState } from "react";
import Header from "../components/Header";
import { Plus } from "phosphor-react";
import EmployeeCard from "../features/employees/EmployeeCard";

export default function EmployeesPage() {
    // Mockdata
    const [employees] = useState([
        { id: 1, name: "Lisa Larsson", email: "lisa@example.com", role: "Undersköterska", phone: "070-11 11 111", gender: "Kvinna", birthDate: "1990-01-01", employmentType: "Monthly", employmentDegree: 100, weeklyHours: 40, isSummerWorker: false, startDate: "2020-01-01", endDate: "2024-12-31", isActive: true },
        { id: 2, name: "Erik Eriksson", email: "erik@example.com", role: "Undersköterska", phone: "070-22 22 222", gender: "Man", birthDate: "1985-05-15", employmentType: "Monthly", employmentDegree: 100, weeklyHours: 38.25, isSummerWorker: false, startDate: "2020-01-01", endDate: "2024-12-31", isActive: true },
        { id: 3, name: "Maria Månsson", email: "maria@example.com", role: "Vårdbiträde", phone: "070-33 33 333", gender: "Kvinna", birthDate: "1992-07-20", employmentType: "Hourly", employmentDegree: 100, weeklyHours: 40, isSummerWorker: true, startDate: "2020-01-01", endDate: "2024-12-31", isActive: true },
    ]);

    return (
        <div className="bg-indigo-100 flex flex-col min-h-screen">
            <Header />
            
            <div className="flex-1 p-6 md:p-8">
                <div className="max-w-7xl mx-auto">
                    {/* Header med knapp */}
                    <div className="flex justify-between items-center mb-6">
                        <h1 className="text-3xl font-bold text-indigo-900">Medarbetare</h1>
                        <button 
                            className="cursor-pointer flex items-center gap-2 bg-indigo-900 text-white px-4 py-2 rounded-lg hover:bg-indigo-800 transition-colors"
                        >
                            <Plus size={20} weight="bold" />
                            Lägg till medarbetare
                        </button>
                    </div>

                    {/* Medarbetarkort */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                        {employees.map((employee) => (
                            <EmployeeCard 
                                key={employee.id} 
                                id={employee.id} 
                                name={employee.name} 
                                phone={employee.phone} 
                                employmentType={employee.employmentType}
                                employmentDegree={employee.employmentDegree} 
                                weeklyHours={employee.weeklyHours} 
                                isSummerWorker={employee.isSummerWorker} 
                                role={employee.role} 
                            />
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

