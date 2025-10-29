import { useMemo } from "react";
import EmployeeRow from "./EmployeeRow";
import type {
    Employee,
    ScheduleEvent,
    Customer,
    Measure,
    TimeSlot,
} from "../types/schedule.types";

interface ScheduleTimelineProps {
    date: Date;
    employees: Employee[];
    scheduleEvents: ScheduleEvent[];
    customers: Customer[];
    measures: Measure[];
}

export default function ScheduleTimeline({
    date,
    employees,
    scheduleEvents,
    customers,
    measures,
}: ScheduleTimelineProps) {
    // Generate time slots (06:00 - 22:00, 30-minute intervals)
    const timeSlots = useMemo(() => {
        const slots: TimeSlot[] = [];
        for (let hour = 6; hour <= 22; hour++) {
            for (let minute = 0; minute < 60; minute += 30) {
                slots.push({
                    hour,
                    minute,
                    display: `${hour.toString().padStart(2, "0")}:${minute
                        .toString()
                        .padStart(2, "0")}`,
                });
            }
        }
        return slots;
    }, []);

    return (
        <div className="flex-1 bg-white rounded-xl shadow-md overflow-hidden flex flex-col">
            {/* Timeline Header */}
            <div className="flex border-b border-gray-200 sticky top-0 bg-white z-10">
                {/* Employee Name Column - Sticky */}
                <div className="w-40 flex-shrink-0 border-r border-gray-200 p-3 bg-indigo-50">
                    <h3 className="text-sm font-bold text-indigo-900">Personal</h3>
                </div>

                {/* Time Slots - Scrollable */}
                <div className="flex-1 overflow-x-auto">
                    <div className="flex" style={{ minWidth: "max-content" }}>
                        {timeSlots.map((slot) => (
                            <div
                                key={`${slot.hour}-${slot.minute}`}
                                className={`
                                    w-24 flex-shrink-0 p-2 text-center border-r border-gray-100
                                    ${slot.minute === 0 ? "border-l border-gray-300" : ""}
                                `}
                            >
                                {slot.minute === 0 && (
                                    <span className="text-xs font-semibold text-gray-700">
                                        {slot.display}
                                    </span>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Employee Rows - Scrollable */}
            <div className="flex-1 overflow-auto">
                <div className="flex flex-col">
                    {employees.map((employee) => {
                        const employeeEvents = scheduleEvents.filter(
                            (event) => event.employeeId === employee.id
                        );

                        return (
                            <EmployeeRow
                                key={employee.id}
                                employee={employee}
                                events={employeeEvents}
                                timeSlots={timeSlots}
                                customers={customers}
                                measures={measures}
                            />
                        );
                    })}
                </div>
            </div>
        </div>
    );
}
