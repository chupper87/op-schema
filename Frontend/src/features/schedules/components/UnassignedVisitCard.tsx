import {
  User,
  ClockClockwise,
  Warning,
  ArrowsOutCardinal,
  Clock,
} from "phosphor-react";
import type {
  UnassignedVisit,
  Customer,
  Measure,
} from "../types/schedule.types";
import { useDraggable } from "@dnd-kit/core";

interface UnassignedVisitCardProps {
  visit: UnassignedVisit;
  customer: Customer;
  measure: Measure;
}

export default function UnassignedVisitCard({
  visit,
  customer,
  measure,
}: UnassignedVisitCardProps) {
  const { attributes, listeners, setNodeRef, transform } = useDraggable({
    id: `unassigned-visit-${visit.id}`,
    data: {
      type: "UNASSIGNED_VISIT",
      visitId: visit.id,
      customerId: visit.customerId,
      measureId: visit.measureId,
      duration: measure.defaultDuration,
    },
  });
  const style = transform
    ? {
        transform: `translate3d(${transform.x}px, ${transform.y}px, 0)`,
      }
    : undefined;

  // Priority colors
  const priorityConfig = {
    urgent: {
      bg: "bg-red-50",
      border: "border-red-500",
      text: "text-red-700",
      icon: "bg-red-500",
      label: "Akut",
    },
    high: {
      bg: "bg-orange-50",
      border: "border-orange-500",
      text: "text-orange-700",
      icon: "bg-orange-500",
      label: "Hög",
    },
    medium: {
      bg: "bg-yellow-50",
      border: "border-yellow-500",
      text: "text-yellow-700",
      icon: "bg-yellow-500",
      label: "Medium",
    },
    low: {
      bg: "bg-green-50",
      border: "border-green-400",
      text: "text-green-700",
      icon: "bg-green-400",
      label: "Låg",
    },
  };

  const priority = priorityConfig[visit.priority];

  // Time of day translation
  const timeOfDayMap = {
    morning: "Morgon",
    afternoon: "Dagtid",
    evening: "Kväll",
    night: "Natt",
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className={`
                rounded-md p-1.5 border-2 cursor-grab active:cursor-grabbing
                transition-all duration-200
                hover:shadow-md shadow-sm
                ${priority.bg} ${priority.border}
            `}
    >
      {/* Priority Badge */}
      <div className="flex items-center justify-between mb-1">
        <div className="flex items-center gap-1">
          <div className={`w-1.5 h-1.5 rounded-full ${priority.icon}`} />
          <span className={`text-[10px] font-semibold ${priority.text}`}>
            {priority.label}
          </span>
        </div>
        <ArrowsOutCardinal size={10} className="text-gray-400" weight="bold" />
      </div>

      {/* Customer Name */}
      <div className="flex items-center gap-1 mb-1">
        <User
          size={12}
          className="text-indigo-900 flex-shrink-0"
          weight="bold"
        />
        <h4 className="text-[11px] font-bold text-indigo-900 leading-tight truncate">
          {customer.name}
        </h4>
      </div>

      {/* Measure Name */}
      <div className="flex items-center gap-1 mb-0.5">
        <ClockClockwise size={11} className="text-gray-600 flex-shrink-0" />
        <p className="text-[10px] text-gray-700 font-medium truncate">
          {measure.name}
        </p>
      </div>

      {/* Duration */}
      <div className="flex items-center gap-1 mb-0.5">
        <Clock size={10} className="text-gray-600 flex-shrink-0" />
        <p className="text-[10px] text-gray-600">
          {measure.defaultDuration} min
        </p>
      </div>

      {/* Preferred Time */}
      {visit.preferredTimeSlot && (
        <div className="flex items-center gap-1">
          <Warning
            size={10}
            className="text-amber-600 flex-shrink-0"
            weight="fill"
          />
          <p className="text-[9px] text-gray-600">
            {timeOfDayMap[visit.preferredTimeSlot]}
          </p>
        </div>
      )}
    </div>
  );
}
