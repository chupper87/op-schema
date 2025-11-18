import type { ScheduleEvent } from '../types/schedule.types';

// Convert time to minutes: 08.30 -> 510
export function timeToMinutes(time: string): number {
  const [hours, minutes] = time.split(':').map(Number);
  return hours * 60 + minutes;
}

// Convert minutes to time: 510 -> 08:30
export function minutesToTime(minutes: number): string {
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  return `${hours.toString().padStart(2, '0')}:${remainingMinutes.toString().padStart(2, '0')}`;
}

// Find events that overlap with a specific time slot
export function findOverlappingEvents(
  allEvents: ScheduleEvent[],
  newStartTime: string,
  newEndTime: string,
  employeeId: number,
  excludeEventId?: string
): ScheduleEvent[] {
  const newStart = timeToMinutes(newStartTime);
  const newEnd = timeToMinutes(newEndTime);

  return allEvents.filter((event) => {
    // Skip the event we are dragging
    if (event.id === excludeEventId) return false;

    // Skip events from other employees
    if (event.employeeId !== employeeId) return false;

    const eventStart = timeToMinutes(event.startTime);
    const eventEnd = timeToMinutes(event.endTime);

    // Check if the new event overlaps with the existing event
    return newStart < eventEnd && newEnd > eventStart;
  });
}

// Shift overlapping events forward in time
export function shiftOverlappingEvents(
  overlappingEvents: ScheduleEvent[],
  allEvents: ScheduleEvent[],
  newEventEndTime: string
): ScheduleEvent[] {
  if (overlappingEvents.length === 0) return [];

  // Sort overlapping events by start time
  const sorted = [...overlappingEvents].sort(
    (a, b) => timeToMinutes(a.startTime) - timeToMinutes(b.startTime)
  );

  const updatedEvents: ScheduleEvent[] = [];
  let nextAvailableTime = timeToMinutes(newEventEndTime);

  for (const event of sorted) {
    // Calculate event duration
    const duration = timeToMinutes(event.endTime) - timeToMinutes(event.startTime);

    // Set new start time to next available time
    const newStart = nextAvailableTime;
    const newEnd = newStart + duration;

    // Update event
    const updatedEvent: ScheduleEvent = {
      ...event,
      startTime: minutesToTime(newStart),
      endTime: minutesToTime(newEnd),
      updatedAt: new Date().toISOString(),
    };

    updatedEvents.push(updatedEvent);

    // Next event can start when this ends
    nextAvailableTime = newEnd;
  }

  return updatedEvents;
}
