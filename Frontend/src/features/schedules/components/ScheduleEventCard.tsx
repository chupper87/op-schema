import { User, Clock, DotsSixVertical } from 'phosphor-react';
import type { ScheduleEvent, Customer, Measure } from '../types/schedule.types';
import { useDraggable } from '@dnd-kit/core';

interface ScheduleEventCardProps {
  event: ScheduleEvent;
  customer: Customer;
  measure: Measure;
}

export default function ScheduleEventCard({ event, customer, measure }: ScheduleEventCardProps) {
  const { attributes, listeners, setNodeRef, transform } = useDraggable({
    id: `event-${event.id}`,
    data: {
      type: 'SCHEDULE_EVENT',
      eventId: event.id,
      employeeId: event.employeeId,
      customerId: event.customerId,
      measureId: event.measureId,
      startTime: event.startTime,
      endTime: event.endTime,
    },
  });

  const style = transform
    ? {
        opacity: 0.5,
      }
    : undefined;
  // Status colors
  const statusConfig = {
    scheduled: {
      bg: 'bg-blue-500',
      border: 'border-blue-600',
    },
    'in-progress': {
      bg: 'bg-green-500',
      border: 'border-green-600',
    },
    completed: {
      bg: 'bg-gray-400',
      border: 'border-gray-500',
    },
    cancelled: {
      bg: 'bg-red-400',
      border: 'border-red-500',
    },
  };

  const status = statusConfig[event.status];

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className={`rounded-lg border-l-4 p-2 ${status.border} cursor-pointer bg-white shadow-sm transition-all duration-150 hover:shadow-md`}
    >
      {/* Drag Handle */}
      <div className="flex items-start gap-1.5">
        <DotsSixVertical size={12} className="mt-0.5 flex-shrink-0 text-gray-400" />

        <div className="min-w-0 flex-1">
          {/* Customer Name */}
          <div className="mb-1 flex items-center gap-1">
            <User size={12} className="flex-shrink-0 text-indigo-900" weight="bold" />
            <p className="truncate text-xs font-bold text-indigo-900">{customer.name}</p>
          </div>

          {/* Measure Name */}
          <p className="mb-1 truncate text-xs text-gray-700">{measure.name}</p>

          {/* Time */}
          <div className="flex items-center gap-1">
            <Clock size={10} className="flex-shrink-0 text-gray-500" />
            <p className="text-xs text-gray-600">
              {event.startTime} - {event.endTime}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
