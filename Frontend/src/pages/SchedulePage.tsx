import { useState } from 'react';
import {
  DndContext,
  PointerSensor,
  useSensor,
  useSensors,
  closestCenter,
  type DragEndEvent,
  DragOverlay,
} from '@dnd-kit/core';
import Header from '../components/Header';
import { Plus } from 'phosphor-react';

import ScheduleHeader from '../features/schedules/components/ScheduleHeader';
import DayScheduleView from '../features/schedules/components/DayScheduleView';
import type {
  ScheduleView,
  Employee,
  Customer,
  Measure,
  ScheduleEvent,
  UnassignedVisit,
} from '../features/schedules/types/schedule.types';
import {
  findOverlappingEvents,
  shiftOverlappingEvents,
} from '../features/schedules/utils/dragDropHelper';
import ScheduleEventCard from '../features/schedules/components/ScheduleEventCard';
import UnassignedVisitCard from '../features/schedules/components/UnassignedVisitCard';

export default function SchedulePage() {
  const [view, setView] = useState<ScheduleView>('day');
  const [currentDate, setCurrentDate] = useState(new Date());
  const [activeId, setActiveId] = useState<string | null>(null);

  // Mock employees
  const [employees] = useState<Employee[]>([
    {
      id: 1,
      name: 'Lisa Larsson',
      email: 'lisa@example.com',
      role: 'Undersköterska',
      phone: '070-11 11 111',
      employmentType: 'Monthly',
      employmentDegree: 100,
      weeklyHours: 40,
      isActive: true,
    },
    {
      id: 2,
      name: 'Erik Eriksson',
      email: 'erik@example.com',
      role: 'Undersköterska',
      phone: '070-22 22 222',
      employmentType: 'Monthly',
      employmentDegree: 100,
      weeklyHours: 38.25,
      isActive: true,
    },
    {
      id: 3,
      name: 'Maria Månsson',
      email: 'maria@example.com',
      role: 'Vårdbiträde',
      phone: '070-33 33 333',
      employmentType: 'Hourly',
      employmentDegree: 100,
      weeklyHours: 40,
      isActive: true,
    },
  ]);

  // Mock customers
  const [customers] = useState<Customer[]>([
    {
      id: 1,
      name: 'Anna Andersson',
      personalNumber: '19850615-1234',
      address: 'Storgatan 1',
      phone: '070-1234567',
    },
    {
      id: 2,
      name: 'Bengt Berg',
      personalNumber: '19720320-5678',
      address: 'Lillgatan 5',
      phone: '070-9876543',
    },
    {
      id: 3,
      name: 'Carina Carlsson',
      personalNumber: '19901010-9999',
      address: 'Parkvägen 12',
      phone: '070-5555555',
    },
  ]);

  // Mock measures
  const [measures] = useState<Measure[]>([
    {
      id: 1,
      name: 'Dusch',
      defaultDuration: 30,
      description: 'Morgonhjälp + dusch',
      timeOfDay: 'Morgon',
    },
    {
      id: 2,
      name: 'Frukost',
      defaultDuration: 30,
      description: 'Morgonhjälp + frukost',
      timeOfDay: 'Morgon',
    },
    {
      id: 3,
      name: 'Lunch',
      defaultDuration: 45,
      description: 'Hjälp med lunch',
      timeOfDay: 'Mitt på dagen',
    },
    {
      id: 4,
      name: 'Middag',
      defaultDuration: 45,
      description: 'Hjälp med middag',
      timeOfDay: 'Kväll',
    },
  ]);

  // Mock schedule events
  const [scheduleEvents, setScheduleEvents] = useState<ScheduleEvent[]>([
    {
      id: 'event-1',
      employeeId: 1,
      customerId: 1,
      measureId: 1,
      date: new Date().toISOString().split('T')[0],
      startTime: '08:00',
      endTime: '08:30',
      status: 'scheduled',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    },
    {
      id: 'event-2',
      employeeId: 1,
      customerId: 2,
      measureId: 3,
      date: new Date().toISOString().split('T')[0],
      startTime: '12:00',
      endTime: '12:45',
      status: 'scheduled',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    },
    {
      id: 'event-3',
      employeeId: 2,
      customerId: 3,
      measureId: 2,
      date: new Date().toISOString().split('T')[0],
      startTime: '09:00',
      endTime: '09:30',
      status: 'in-progress',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    },
  ]);

  // Mock unassigned visits
  const [unassignedVisits, setUnassignedVisits] = useState<UnassignedVisit[]>([
    {
      id: 'unassigned-1',
      customerId: 1,
      measureId: 4,
      preferredTimeSlot: 'evening',
      priority: 'high',
      notes: 'Önskar kvällstid',
    },
    {
      id: 'unassigned-2',
      customerId: 3,
      measureId: 1,
      preferredTimeSlot: 'morning',
      priority: 'urgent',
      notes: 'Akut behov',
    },
  ]);

  const sensors = useSensors(useSensor(PointerSensor, { activationConstraint: { distance: 4 } }));

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    if (!over) return;

    console.log('Drog från:', active.data.current);
    console.log('Släpptes på:', over.data.current);

    const draggedData = active.data.current;
    const dropData = over.data.current;

    if (!draggedData || !dropData) return;

    // Check if dropping back to unassigned panel
    if (dropData.type === 'UNASSIGNED_PANEL' && draggedData.type === 'SCHEDULE_EVENT') {
      console.log('Flyttar tillbaka till unassigned');

      const unassignedVisit: UnassignedVisit = {
        id: `unassigned-${Date.now()}`,
        customerId: draggedData.customerId,
        measureId: draggedData.measureId,
        priority: 'medium',
        notes: 'Flyttad tillbaka från schema',
      };

      // Add to unassigned visits
      setUnassignedVisits((prev) => [...prev, unassignedVisit]);

      // Remove from schedule events
      setScheduleEvents((prev) => prev.filter((e) => e.id !== draggedData.eventId));

      return;
    }

    // Only proceed if we have a timeSlot (dropping on timeline)
    if (!dropData.timeSlot) {
      console.log('Ingen timeSlot - avbryter');
      return;
    }

    let duration: number;
    if (draggedData.type === 'UNASSIGNED_VISIT') {
      duration = draggedData.duration;
    } else {
      const [startHour, startMinute] = draggedData.startTime.split(':').map(Number);
      const [endHour, endMinute] = draggedData.endTime.split(':').map(Number);
      duration = endHour * 60 + endMinute - (startHour * 60 + startMinute);
    }

    const newStartTime = dropData.timeSlot;
    const [startHour, startMinute] = newStartTime.split(':').map(Number);
    const endTotalMinutes = startHour * 60 + startMinute + duration;
    const endHour = Math.floor(endTotalMinutes / 60);
    const endMinute = endTotalMinutes % 60;
    const newEndTime = `${String(endHour).padStart(2, '0')}:${String(endMinute).padStart(2, '0')}`;

    console.log('Duration:', duration, 'minuter');
    console.log('Ny tid:', newStartTime, '-', newEndTime);

    // Find overlapping events

    const overlappingEvents = findOverlappingEvents(
      scheduleEvents,
      newStartTime,
      newEndTime,
      dropData.employeeId,
      draggedData.type === 'SCHEDULE_EVENT' ? draggedData.eventId : undefined
    );

    console.log('Överlappande events:', overlappingEvents.length);

    // Shift overlapping events forward in time
    const shiftedEvents = shiftOverlappingEvents(overlappingEvents, scheduleEvents, newEndTime);

    console.log('Skjutna events:', shiftedEvents.length);

    // Handle different scenarios
    if (draggedData.type === 'UNASSIGNED_VISIT') {
      console.log('Skapar nytt event från unassigned visit');

      const newEvent: ScheduleEvent = {
        id: `event-${Date.now()}`,
        employeeId: dropData.employeeId,
        customerId: draggedData.customerId,
        measureId: draggedData.measureId,
        date: currentDate.toISOString().split('T')[0],
        startTime: newStartTime,
        endTime: newEndTime,
        status: 'scheduled',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      console.log('Nytt event skapat:', newEvent);

      setScheduleEvents((prev) => {
        // Ta bort gamla versioner av skjutna events
        const eventsToRemove = shiftedEvents.map((e) => e.id);
        const filteredEvents = prev.filter((e) => !eventsToRemove.includes(e.id));

        // Lägg till nytt event + alla skjutna events
        return [...filteredEvents, newEvent, ...shiftedEvents];
      });

      setUnassignedVisits((prev) => prev.filter((visit) => visit.id !== draggedData.visitId));
    } else {
      console.log('Flyttar befintligt event');

      // Update existing event
      setScheduleEvents((prev) => {
        // Ta bort gamla versioner av skjutna events
        const eventsToRemove = shiftedEvents.map((e) => e.id);
        const filteredEvents = prev.filter((e) => !eventsToRemove.includes(e.id));

        // Uppdatera det event vi drog + lägg till skjutna events
        const updatedEvents = filteredEvents.map((event) => {
          if (event.id === draggedData.eventId) {
            return {
              ...event,
              employeeId: dropData.employeeId,
              startTime: newStartTime,
              endTime: newEndTime,
              updatedAt: new Date().toISOString(),
            };
          }
          return event;
        });

        return [...updatedEvents, ...shiftedEvents];
      });
    }

    setActiveId(null);
  };

  const handleDragStart = (event: DragEndEvent) => {
    setActiveId(event.active.id as string);
  };

  const handleDragCancel = () => {
    setActiveId(null);
  };

  const getActiveCard = () => {
    if (!activeId) return null;

    // Kolla om det är ett unassigned visit
    if (activeId.startsWith('unassigned-visit-')) {
      const visit = unassignedVisits.find((v) => `unassigned-visit-${v.id}` === activeId);
      if (!visit) return null;

      const customer = customers.find((c) => c.id === visit.customerId);
      const measure = measures.find((m) => m.id === visit.measureId);

      if (!customer || !measure) return null;

      return { type: 'visit', visit, customer, measure };
    }

    // Annars är det ett schedule event
    if (activeId.startsWith('event-')) {
      const event = scheduleEvents.find((e) => `event-${e.id}` === activeId);
      if (!event) return null;

      const customer = customers.find((c) => c.id === event.customerId);
      const measure = measures.find((m) => m.id === event.measureId);

      if (!customer || !measure) return null;

      return { type: 'event', event, customer, measure };
    }

    return null;
  };

  return (
    <div className="flex min-h-screen flex-col bg-indigo-100">
      <Header />

      <div className="flex-1 p-6 md:p-8">
        <div className="mx-auto max-w-7xl">
          {/* Page Header */}
          <div className="mb-6 flex items-center justify-between">
            <h1 className="text-3xl font-bold text-indigo-900">Planering</h1>
            <button className="flex cursor-pointer items-center gap-2 rounded-lg bg-indigo-900 px-4 py-2 text-white transition-colors hover:bg-indigo-800">
              <Plus size={20} weight="bold" />
              Skapa besök
            </button>
          </div>

          {/* Schedule Controls */}
          <ScheduleHeader
            view={view}
            currentDate={currentDate}
            onViewChange={setView}
            onDateChange={setCurrentDate}
          />

          {/* Day Schedule View */}
          <div className="mt-4 h-[calc(100vh-280px)] min-h-[600px]">
            <DndContext
              sensors={sensors}
              onDragStart={handleDragStart}
              onDragCancel={handleDragCancel}
              onDragEnd={handleDragEnd}
              collisionDetection={closestCenter}
            >
              <DayScheduleView
                currentDate={currentDate}
                employees={employees}
                scheduleEvents={scheduleEvents}
                unassignedVisits={unassignedVisits}
                customers={customers}
                measures={measures}
              />

              <DragOverlay>
                {(() => {
                  const activeCard = getActiveCard();
                  if (!activeCard) return null;

                  if (activeCard.type === 'visit') {
                    if (!activeCard.visit) return null;
                    return (
                      <UnassignedVisitCard
                        visit={activeCard.visit}
                        customer={activeCard.customer}
                        measure={activeCard.measure}
                      />
                    );
                  }

                  if (activeCard.type === 'event') {
                    if (!activeCard.event) return null;
                    return (
                      <ScheduleEventCard
                        event={activeCard.event}
                        customer={activeCard.customer}
                        measure={activeCard.measure}
                      />
                    );
                  }

                  return null;
                })()}
              </DragOverlay>
            </DndContext>
          </div>
        </div>
      </div>
    </div>
  );
}
