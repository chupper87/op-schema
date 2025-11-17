import { useMemo } from "react";
import ScheduleEventCard from "./ScheduleEventCard";
import type {
    Employee,
    ScheduleEvent,
    Customer,
    Measure,
    TimeSlot,
} from "../types/schedule.types";
import { useDroppable } from "@dnd-kit/core";

interface EmployeeRowProps {
    employee: Employee;
    events: ScheduleEvent[];
    timeSlots: TimeSlot[];
    customers: Customer[];
    measures: Measure[];
}

interface TimeSlotDropZoneProps {
    employeeId: number;
    timeSlot: TimeSlot;
}

function TimeSlotDropZone({ employeeId, timeSlot }: TimeSlotDropZoneProps) {
    const { isOver, setNodeRef } = useDroppable({
        id: `drop-${employeeId}-${timeSlot.display}`,
        data: {
            employeeId,
            timeSlot: timeSlot.display,
        },
    });

    return (
        <div
            ref={setNodeRef}
            className={`
                w-24 flex-shrink-0 border-r border-gray-100 h-full
                ${timeSlot.minute === 0 ? "border-l border-gray-200" : ""}
                ${isOver ? "bg-blue-100" : ""}
            `}
        />
    );
}

export default function EmployeeRow({
    employee,
    events,
    timeSlots,
    customers,
    measures,
}: EmployeeRowProps) {
    // Calculate event positions and widths
    const positionedEvents = useMemo(() => {
        return events.map((event) => {
            const [startHour, startMinute] = event.startTime.split(":").map(Number);
            const [endHour, endMinute] = event.endTime.split(":").map(Number);

            const startTotalMinutes = startHour * 60 + startMinute;
            const endTotalMinutes = endHour * 60 + endMinute;
            const durationMinutes = endTotalMinutes - startTotalMinutes;

            // Calculate position (06:00 = 0)
            const baseMinutes = 6 * 60;
            const offsetMinutes = startTotalMinutes - baseMinutes;
            const leftPosition = (offsetMinutes / 30) * 96; // 96px = w-24

            // Calculate width
            const width = (durationMinutes / 30) * 96;

            return {
                event,
                leftPosition,
                width,
            };
        });
    }, [events]);

    return (
        <div className="flex border-b border-gray-100 hover:bg-gray-50 transition-colors">
            {/* Employee Name - Sticky */}
            <div className="w-40 flex-shrink-0 border-r border-gray-200 p-3 bg-white sticky left-0 z-5">
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-full bg-indigo-200 flex items-center justify-center flex-shrink-0">
                        <span className="text-xs font-bold text-indigo-900">
                            {employee.name.charAt(0)}
                        </span>
                    </div>
                    <div className="flex-1 min-w-0">
                        <p className="text-sm font-semibold text-indigo-900 truncate">
                            {employee.name}
                        </p>
                        <p className="text-xs text-gray-600 truncate">{employee.role}</p>
                    </div>
                </div>
            </div>

            {/* Time Grid - Scrollable */}
            <div className="flex-1 overflow-x-auto relative" style={{ minHeight: "80px" }}>
                <div className="flex" style={{ minWidth: "max-content", height: "100%" }}>
                    {/* Time Slot Grid */}
                    {timeSlots.map((slot) => (
                        <TimeSlotDropZone
                        key={`${employee.id}-${slot.display}`}
                        employeeId={employee.id}
                        timeSlot={slot}
                    />
                    ))}

                    {/* Positioned Events (Absolute) */}
                    <div className="absolute inset-0 pointer-events-none">
                        {positionedEvents.map(({ event, leftPosition, width }) => {
                            const customer = customers.find((c) => c.id === event.customerId);
                            const measure = measures.find((m) => m.id === event.measureId);

                            if (!customer || !measure) return null;

                            return (
                                <div
                                    key={event.id}
                                    className="absolute top-1 pointer-events-auto"
                                    style={{
                                        left: `${leftPosition}px`,
                                        width: `${width}px`,
                                    }}
                                >
                                    <ScheduleEventCard
                                        event={event}
                                        customer={customer}
                                        measure={measure}
                                    />
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>
        </div>
    );
}
