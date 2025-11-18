// Core schedule types
export type ScheduleView = 'day' | 'week' | 'month';

export interface ScheduleViewState {
  view: ScheduleView;
  currentDate: Date;
  selectedEmployeeId: number | null;
}

export interface ScheduleEvent {
  id: string;
  employeeId: number;
  customerId: number;
  measureId: number;
  date: string; // ISO date format "YYYY-MM-DD"
  startTime: string; // "HH:mm" format
  endTime: string; // "HH:mm" format
  status: 'scheduled' | 'in-progress' | 'completed' | 'cancelled';
  notes?: string;
  createdAt: string;
  updatedAt: string;
}

export interface UnassignedVisit {
  id: string;
  customerId: number;
  measureId: number;
  preferredDate?: string;
  preferredTimeSlot?: 'morning' | 'afternoon' | 'evening';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  notes?: string;
}

export interface TimeSlot {
  hour: number;
  minute: number;
  display: string; // "08:00"
}

export interface Employee {
  id: number;
  name: string;
  email: string;
  role: string;
  phone: string;
  employmentType: 'Monthly' | 'Hourly';
  employmentDegree: number;
  weeklyHours: number;
  isActive: boolean;
}

export interface Customer {
  id: number;
  name: string;
  personalNumber: string;
  address: string;
  phone: string;
}

export interface Measure {
  id: number;
  name: string;
  defaultDuration: number; // in minutes
  description: string;
  timeOfDay: 'Morgon' | 'Mitt på dagen' | 'Kväll';
}
