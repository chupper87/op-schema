import Header from "../components/Header";
import { Plus } from "phosphor-react";
import MeasureCard from "../features/measures/MeasureCard";
import { useState } from "react";



export default function MeasuresPage() {

    const [measures] = useState([
        { id: 1, name: "Dusch", default_duration: 15, text: "Morgonhjälp + dusch", time_of_day: "Morgon"},
        { id: 2, name: "Frukost", default_duration: 20, text: "Morgonhjälp + frukost", time_of_day: "Morgon"},
        { id: 3, name: "Tillsyn", default_duration: 10, text: "Hjälp med medicinering", time_of_day: "Morgon"},
        { id: 4, name: "Lunch", default_duration: 30, text: "Hjälp med lunch", time_of_day: "Mitt på dagen"},
        { id: 5, name: "Middag", default_duration: 30, text: "Hjälp med middag", time_of_day: "Kväll"},
        { id: 6, name: "Kvällshjälp", default_duration: 20, text: "Kvällshjälp + sänggående", time_of_day: "Kväll"},
    ])






    return (
        <div className="bg-indigo-100 min-h-screen flex flex-col">
            <Header />

            <div className="flex-1 p-8 md:p-8">
                <div className="max-w-7xl mx-auto">

                    {/* Header */}
                    <div className="flex justify-between items-center mb-6">
                        <h1 className="text-3xl font-bold text-indigo-900">Insatser</h1>
                        <div className="flex gap-3 items-center">
                            <button className="cursor-pointer flex items-center gap-2 bg-indigo-900 text-white px-4 py-2 hover:bg-indigo-800 transition-colors rounded-lg">
                                <Plus size={20} weight="bold"/>
                                Skapa insats
                            </button>
                        </div>
                    </div>
                    {/*Measures*/}

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                        {measures.map((measure) => (
                            <MeasureCard
                                key={measure.id}
                                id={measure.id}
                                name={measure.name}
                                defaultDuration={measure.default_duration}
                                text={measure.text}
                                timeOfDay={measure.time_of_day}
                                timeFlexibility={"Flexibel"}
                                isActive={true}
                            />
                        ))}

                    </div>
                </div>
            </div>

        </div>
    );
}
