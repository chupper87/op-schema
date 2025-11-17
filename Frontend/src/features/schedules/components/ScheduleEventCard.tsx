import { User, Clock, DotsSixVertical } from "phosphor-react";
import type { ScheduleEvent, Customer, Measure } from "../types/schedule.types";
import { useDraggable } from "@dnd-kit/core";

interface ScheduleEventCardProps {
  event: ScheduleEvent;
  customer: Customer;
  measure: Measure;
}

export default function ScheduleEventCard({
  event,
  customer,
  measure,
}: ScheduleEventCardProps) {
  const { attributes, listeners, setNodeRef, transform } = useDraggable({
    id: `event-${event.id}`,
    data: {
      type: "SCHEDULE_EVENT",
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
        transform: `translate3d(${transform.x}px, ${transform.y}px, 0)`,
      }
    : undefined;
  // Status colors
  const statusConfig = {
    scheduled: {
      bg: "bg-blue-500",
      border: "border-blue-600",
    },
    "in-progress": {
      bg: "bg-green-500",
      border: "border-green-600",
    },
    completed: {
      bg: "bg-gray-400",
      border: "border-gray-500",
    },
    cancelled: {
      bg: "bg-red-400",
      border: "border-red-500",
    },
  };

  const status = statusConfig[event.status];

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className={`
                rounded-lg p-2 border-l-4 ${status.border}
                bg-white shadow-sm hover:shadow-md
                cursor-pointer
                transition-all duration-150
            `}
    >
      {/* Drag Handle */}
      <div className="flex items-start gap-1.5">
        <DotsSixVertical
          size={12}
          className="text-gray-400 mt-0.5 flex-shrink-0"
        />

        <div className="flex-1 min-w-0">
          {/* Customer Name */}
          <div className="flex items-center gap-1 mb-1">
            <User
              size={12}
              className="text-indigo-900 flex-shrink-0"
              weight="bold"
            />
            <p className="text-xs font-bold text-indigo-900 truncate">
              {customer.name}
            </p>
          </div>

          {/* Measure Name */}
          <p className="text-xs text-gray-700 truncate mb-1">{measure.name}</p>

          {/* Time */}
          <div className="flex items-center gap-1">
            <Clock size={10} className="text-gray-500 flex-shrink-0" />
            <p className="text-xs text-gray-600">
              {event.startTime} - {event.endTime}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
