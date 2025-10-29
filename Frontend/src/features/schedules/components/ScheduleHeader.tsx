import { CaretLeft, CaretRight, CalendarBlank } from "phosphor-react";
import type { ScheduleView } from "../types/schedule.types";

interface ScheduleHeaderProps {
  view: ScheduleView;
  currentDate: Date;
  onViewChange: (view: ScheduleView) => void;
  onDateChange: (date: Date) => void;
}

export default function ScheduleHeader({
  view,
  currentDate,
  onViewChange,
  onDateChange,
}: ScheduleHeaderProps) {
  const formatDateDisplay = () => {
    const options: Intl.DateTimeFormatOptions = {
      year: "numeric",
      month: "long",
      ...(view === "day" && { day: "numeric" }),
    };
    return currentDate.toLocaleDateString("sv-SE", options);
  };

  const navigatePrevious = () => {
    const newDate = new Date(currentDate);
    if (view === "day") newDate.setDate(newDate.getDate() - 1);
    if (view === "week") newDate.setDate(newDate.getDate() - 7);
    if (view === "month") newDate.setMonth(newDate.getMonth() - 1);
    onDateChange(newDate);
  };

  const navigateNext = () => {
    const newDate = new Date(currentDate);
    if (view === "day") newDate.setDate(newDate.getDate() + 1);
    if (view === "week") newDate.setDate(newDate.getDate() + 7);
    if (view === "month") newDate.setMonth(newDate.getMonth() + 1);
    onDateChange(newDate);
  };

  const goToToday = () => {
    onDateChange(new Date());
  };

  return (
    <div className="bg-white rounded-xl p-4 shadow-md">
      <div className="flex flex-col md:flex-row justify-between items-center gap-4">
        {/* Date Navigation */}
        <div className="flex items-center gap-3">
          <button
            onClick={navigatePrevious}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            aria-label="F�reg�ende"
          >
            <CaretLeft size={24} className="text-indigo-900" weight="bold" />
          </button>

          <div className="flex items-center gap-2">
            <CalendarBlank size={24} className="text-indigo-900" />
            <h2 className="text-xl font-bold text-indigo-900 capitalize">
              {formatDateDisplay()}
            </h2>
          </div>

          <button
            onClick={navigateNext}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            aria-label="Nästa"
          >
            <CaretRight size={24} className="text-indigo-900" weight="bold" />
          </button>

          <button
            onClick={goToToday}
            className="ml-2 px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
          >
            Idag
          </button>
        </div>

        {/* View Switcher */}
        <div className="flex gap-2">
          {(["day", "week", "month"] as ScheduleView[]).map((viewOption) => (
            <button
              key={viewOption}
              onClick={() => onViewChange(viewOption)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                view === viewOption
                  ? "bg-indigo-900 text-white"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              {viewOption === "day" && "Dag"}
              {viewOption === "week" && "Vecka"}
              {viewOption === "month" && "Månad"}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
