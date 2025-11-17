import { useState } from "react";
import {
  DndContext,
  PointerSensor,
  useSensor,
  useSensors,
  closestCenter,
  type DragEndEvent,
} from "@dnd-kit/core";
import Header from "../components/Header";
import { Plus } from "phosphor-react";

import ScheduleHeader from "../features/schedules/components/ScheduleHeader";
import DayScheduleView from "../features/schedules/components/DayScheduleView";
import type {
  ScheduleView,
  Employee,
  Customer,
  Measure,
  ScheduleEvent,
  UnassignedVisit,
} from "../features/schedules/types/schedule.types";

export default function SchedulePage() {
  const [view, setView] = useState<ScheduleView>("day");
  const [currentDate, setCurrentDate] = useState(new Date());

  // Mock employees
  const [employees] = useState<Employee[]>([
    {
      id: 1,
      name: "Lisa Larsson",
      email: "lisa@example.com",
      role: "Undersköterska",
      phone: "070-11 11 111",
      employmentType: "Monthly",
      employmentDegree: 100,
      weeklyHours: 40,
      isActive: true,
    },
    {
      id: 2,
      name: "Erik Eriksson",
      email: "erik@example.com",
      role: "Undersköterska",
      phone: "070-22 22 222",
      employmentType: "Monthly",
      employmentDegree: 100,
      weeklyHours: 38.25,
      isActive: true,
    },
    {
      id: 3,
      name: "Maria Månsson",
      email: "maria@example.com",
      role: "Vårdbiträde",
      phone: "070-33 33 333",
      employmentType: "Hourly",
      employmentDegree: 100,
      weeklyHours: 40,
      isActive: true,
    },
  ]);

  // Mock customers
  const [customers] = useState<Customer[]>([
    {
      id: 1,
      name: "Anna Andersson",
      personalNumber: "19850615-1234",
      address: "Storgatan 1",
      phone: "070-1234567",
    },
    {
      id: 2,
      name: "Bengt Berg",
      personalNumber: "19720320-5678",
      address: "Lillgatan 5",
      phone: "070-9876543",
    },
    {
      id: 3,
      name: "Carina Carlsson",
      personalNumber: "19901010-9999",
      address: "Parkvägen 12",
      phone: "070-5555555",
    },
  ]);

  // Mock measures
  const [measures] = useState<Measure[]>([
    {
      id: 1,
      name: "Dusch",
      defaultDuration: 30,
      description: "Morgonhjälp + dusch",
      timeOfDay: "Morgon",
    },
    {
      id: 2,
      name: "Frukost",
      defaultDuration: 30,
      description: "Morgonhjälp + frukost",
      timeOfDay: "Morgon",
    },
    {
      id: 3,
      name: "Lunch",
      defaultDuration: 45,
      description: "Hjälp med lunch",
      timeOfDay: "Mitt på dagen",
    },
    {
      id: 4,
      name: "Middag",
      defaultDuration: 45,
      description: "Hjälp med middag",
      timeOfDay: "Kväll",
    },
  ]);

  // Mock schedule events
  const [scheduleEvents, setScheduleEvents] = useState<ScheduleEvent[]>([
    {
      id: "event-1",
      employeeId: 1,
      customerId: 1,
      measureId: 1,
      date: new Date().toISOString().split("T")[0],
      startTime: "08:00",
      endTime: "08:30",
      status: "scheduled",
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    },
    {
      id: "event-2",
      employeeId: 1,
      customerId: 2,
      measureId: 3,
      date: new Date().toISOString().split("T")[0],
      startTime: "12:00",
      endTime: "12:45",
      status: "scheduled",
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    },
    {
      id: "event-3",
      employeeId: 2,
      customerId: 3,
      measureId: 2,
      date: new Date().toISOString().split("T")[0],
      startTime: "09:00",
      endTime: "09:30",
      status: "in-progress",
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    },
  ]);

  // Mock unassigned visits
  const [unassignedVisits, setUnassignedVisits] = useState<UnassignedVisit[]>([
    {
      id: "unassigned-1",
      customerId: 1,
      measureId: 4,
      preferredTimeSlot: "evening",
      priority: "high",
      notes: "Önskar kvällstid",
    },
    {
      id: "unassigned-2",
      customerId: 3,
      measureId: 1,
      preferredTimeSlot: "morning",
      priority: "urgent",
      notes: "Akut behov",
    },
  ]);

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 4 } })
  );

  const handleDragEnd = (event: DragEndEvent) => {
    console.log("Drag ended:", event);
  };

  return (
    <div className="bg-indigo-100 min-h-screen flex flex-col">
      <Header />

      <div className="flex-1 p-6 md:p-8">
        <div className="max-w-7xl mx-auto">
          {/* Page Header */}
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-indigo-900">Planering</h1>
            <button className="cursor-pointer flex items-center gap-2 bg-indigo-900 text-white px-4 py-2 rounded-lg hover:bg-indigo-800 transition-colors">
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
            </DndContext>
          </div>
        </div>
      </div>
    </div>
  );
}
