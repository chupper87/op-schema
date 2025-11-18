import { useMemo } from 'react';
import ScheduleEventCard from './ScheduleEventCard';
import type { Employee, ScheduleEvent, Customer, Measure, TimeSlot } from '../types/schedule.types';
import { useDroppable } from '@dnd-kit/core';

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
      className={`h-full w-24 flex-shrink-0 border-r border-gray-100 ${timeSlot.minute === 0 ? 'border-l border-gray-200' : ''} ${isOver ? 'bg-blue-100' : ''} `}
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
      const [startHour, startMinute] = event.startTime.split(':').map(Number);
      const [endHour, endMinute] = event.endTime.split(':').map(Number);

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
    <div className="flex border-b border-gray-100 transition-colors hover:bg-gray-50">
      {/* Employee Name - Sticky */}
      <div className="sticky left-0 z-10 w-40 flex-shrink-0 border-r border-gray-200 bg-white p-3">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-indigo-200">
            <span className="text-xs font-bold text-indigo-900">{employee.name.charAt(0)}</span>
          </div>
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-semibold text-indigo-900">{employee.name}</p>
            <p className="truncate text-xs text-gray-600">{employee.role}</p>
          </div>
        </div>
      </div>

      {/* Time Grid - Synchronized with header scroll */}
      <div className="relative overflow-y-hidden" style={{ minHeight: '90px' }}>
        <div className="flex" style={{ height: '100%' }}>
          {/* Time Slot Grid */}
          {timeSlots.map((slot) => (
            <TimeSlotDropZone
              key={`${employee.id}-${slot.display}`}
              employeeId={employee.id}
              timeSlot={slot}
            />
          ))}

          {/* Positioned Events (Absolute) */}
          <div className="pointer-events-none absolute inset-0">
            {positionedEvents.map(({ event, leftPosition, width }) => {
              const customer = customers.find((c) => c.id === event.customerId);
              const measure = measures.find((m) => m.id === event.measureId);

              if (!customer || !measure) return null;

              return (
                <div
                  key={event.id}
                  className="pointer-events-auto absolute top-1 max-h-[104px] min-w-[96px]"
                  style={{
                    left: `${leftPosition}px`,
                    width: `${width}px`,
                  }}
                >
                  <ScheduleEventCard event={event} customer={customer} measure={measure} />
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
