import UnassignedVisitsPanel from './UnassignedVisitsPanel';
import ScheduleTimeline from './ScheduleTimeline';
import type {
  Employee,
  Customer,
  Measure,
  ScheduleEvent,
  UnassignedVisit,
} from '../types/schedule.types';

interface DayScheduleViewProps {
  currentDate: Date;
  employees: Employee[];
  scheduleEvents: ScheduleEvent[];
  unassignedVisits: UnassignedVisit[];
  customers: Customer[];
  measures: Measure[];
}

export default function DayScheduleView({
  currentDate,
  employees,
  scheduleEvents,
  unassignedVisits,
  customers,
  measures,
}: DayScheduleViewProps) {
  return (
    <div className="flex gap-4">
      {/* Left Panel: Unassigned Visits */}
      <UnassignedVisitsPanel visits={unassignedVisits} customers={customers} measures={measures} />

      {/* Center Panel: Timeline Grid */}
      <ScheduleTimeline
        date={currentDate}
        employees={employees}
        scheduleEvents={scheduleEvents}
        customers={customers}
        measures={measures}
      />
    </div>
  );
}
