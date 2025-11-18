import { User, ClockClockwise, Warning, ArrowsOutCardinal, Clock } from 'phosphor-react';
import type { UnassignedVisit, Customer, Measure } from '../types/schedule.types';
import { useDraggable } from '@dnd-kit/core';

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
      type: 'UNASSIGNED_VISIT',
      visitId: visit.id,
      customerId: visit.customerId,
      measureId: visit.measureId,
      duration: measure.defaultDuration,
    },
  });
  const style = transform
    ? {
        opacity: 0.5,
      }
    : undefined;

  // Priority colors
  const priorityConfig = {
    urgent: {
      bg: 'bg-red-50',
      border: 'border-red-500',
      text: 'text-red-700',
      icon: 'bg-red-500',
      label: 'Akut',
    },
    high: {
      bg: 'bg-orange-50',
      border: 'border-orange-500',
      text: 'text-orange-700',
      icon: 'bg-orange-500',
      label: 'Hög',
    },
    medium: {
      bg: 'bg-yellow-50',
      border: 'border-yellow-500',
      text: 'text-yellow-700',
      icon: 'bg-yellow-500',
      label: 'Medium',
    },
    low: {
      bg: 'bg-green-50',
      border: 'border-green-400',
      text: 'text-green-700',
      icon: 'bg-green-400',
      label: 'Låg',
    },
  };

  const priority = priorityConfig[visit.priority];

  // Time of day translation
  const timeOfDayMap = {
    morning: 'Morgon',
    afternoon: 'Dagtid',
    evening: 'Kväll',
    night: 'Natt',
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className={`cursor-grab rounded-md border-2 p-1.5 shadow-sm transition-all duration-200 hover:shadow-md active:cursor-grabbing ${priority.bg} ${priority.border} `}
    >
      {/* Priority Badge */}
      <div className="mb-1 flex items-center justify-between">
        <div className="flex items-center gap-1">
          <div className={`h-1.5 w-1.5 rounded-full ${priority.icon}`} />
          <span className={`text-[10px] font-semibold ${priority.text}`}>{priority.label}</span>
        </div>
        <ArrowsOutCardinal size={10} className="text-gray-400" weight="bold" />
      </div>

      {/* Customer Name */}
      <div className="mb-1 flex items-center gap-1">
        <User size={12} className="flex-shrink-0 text-indigo-900" weight="bold" />
        <h4 className="truncate text-[11px] leading-tight font-bold text-indigo-900">
          {customer.name}
        </h4>
      </div>

      {/* Measure Name */}
      <div className="mb-0.5 flex items-center gap-1">
        <ClockClockwise size={11} className="flex-shrink-0 text-gray-600" />
        <p className="truncate text-[10px] font-medium text-gray-700">{measure.name}</p>
      </div>

      {/* Duration */}
      <div className="mb-0.5 flex items-center gap-1">
        <Clock size={10} className="flex-shrink-0 text-gray-600" />
        <p className="text-[10px] text-gray-600">{measure.defaultDuration} min</p>
      </div>

      {/* Preferred Time */}
      {visit.preferredTimeSlot && (
        <div className="flex items-center gap-1">
          <Warning size={10} className="flex-shrink-0 text-amber-600" weight="fill" />
          <p className="text-[9px] text-gray-600">{timeOfDayMap[visit.preferredTimeSlot]}</p>
        </div>
      )}
    </div>
  );
}
