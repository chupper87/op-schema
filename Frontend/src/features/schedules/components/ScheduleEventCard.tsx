import { User, Clock, DotsSixVertical } from 'phosphor-react';
import type { ScheduleEvent, Customer, Measure } from '../types/schedule.types';
import { useDraggable } from '@dnd-kit/core';

interface ScheduleEventCardProps {
  event: ScheduleEvent;
  customer: Customer;
  measure: Measure;
}

/**
 * Truncates a full name to "FirstName FirstLetterOfLastName" format
 * Examples:
 * - "Anna Andersson Middag" → "Anna A"
 * - "John Doe" → "John D"
 * - "Maria" → "Maria"
 * - "Lars Peter Svensson" → "Lars S"
 */
function truncateCustomerName(fullName: string): string {
  if (!fullName || typeof fullName !== 'string') {
    return '';
  }

  const nameParts = fullName.trim().split(/\s+/); // Split by whitespace

  if (nameParts.length === 0) {
    return '';
  }

  if (nameParts.length === 1) {
    // Single name - return as is
    return nameParts[0];
  }

  // Multiple names - return first name + first letter of last name
  const firstName = nameParts[0];
  const lastName = nameParts[nameParts.length - 1]; // Get the last part as surname
  const lastInitial = lastName.charAt(0).toUpperCase();

  return `${firstName} ${lastInitial}`;
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

  // Truncate customer name for compact display
  const displayName = truncateCustomerName(customer.name);

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className={`overflow-hidden rounded-lg border-l-4 p-2 ${status.border} cursor-pointer bg-white shadow-sm transition-all duration-150 hover:shadow-md`}
    >
      {/* Drag Handle */}
      <div className="flex items-start gap-0.5">
        <DotsSixVertical size={10} className="flex-shrink-0 text-gray-400" />

        <div className="min-w-0 flex-1">
          {/* Customer Name - Truncated */}
          <div className="mb-2 flex items-center gap-0.5 leading-tight">
            <User size={12} className="flex-shrink-0 text-indigo-900" weight="bold" />
            <p className="truncate text-xs leading-tight font-bold text-indigo-900">
              {displayName}
            </p>
          </div>

          {/* Measure Name */}
          <p className="mb-2 truncate text-xs leading-tight text-gray-700">{measure.name}</p>

          {/* Time - Compact single line */}
          <div className="flex items-center gap-0.5 leading-tight">
            <Clock size={9} className="flex-shrink-0 text-gray-500" />
            <p className="text-[11px] leading-tight whitespace-nowrap text-gray-600">
              {event.startTime} - {event.endTime}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
