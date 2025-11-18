import { useState } from "react";
import { Funnel, ClockCounterClockwise } from "phosphor-react";
import UnassignedVisitCard from "./UnassignedVisitCard";
import type {
  UnassignedVisit,
  Customer,
  Measure,
} from "../types/schedule.types";
import { useDroppable } from "@dnd-kit/core";

interface UnassignedVisitsPanelProps {
  visits: UnassignedVisit[];
  customers: Customer[];
  measures: Measure[];
}

export default function UnassignedVisitsPanel({
  visits,
  customers,
  measures,
}: UnassignedVisitsPanelProps) {
  const [priorityFilter, setPriorityFilter] = useState<string>("all");

  // Filter visits by priority
  const filteredVisits = visits.filter((visit) => {
    if (priorityFilter === "all") return true;
    return visit.priority === priorityFilter;
  });

  // Sort by priority (urgent first)
  const sortedVisits = [...filteredVisits].sort((a, b) => {
    const priorityOrder: Record<string, number> = {
      urgent: 0,
      high: 1,
      medium: 2,
      low: 3,
    };
    return priorityOrder[a.priority] - priorityOrder[b.priority];
  });

  const { isOver, setNodeRef } = useDroppable({
    id: `unassigned-panel`,
    data: {
      type: "UNASSIGNED_PANEL",
    },
  });

  return (
    <div
      ref={setNodeRef}
      className={`w-80 flex-shrink-0 bg-white rounded-xl shadow-md flex flex-col overflow-hidden
            transition-colors
            ${isOver ? `ring-4 ring-indigo-500 bg-indigo-50` : ""}
            `}
    >
      {/* Panel Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center gap-2 mb-3">
          <ClockCounterClockwise
            size={20}
            className="text-indigo-900"
            weight="bold"
          />
          <h3 className="text-lg font-bold text-indigo-900">
            Otilldelade besök
          </h3>
        </div>

        {/* Priority Filter */}
        <div className="flex items-center gap-2">
          <Funnel size={16} className="text-gray-600" />
          <select
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
            className="flex-1 text-sm border border-gray-300 rounded-lg px-3 py-1.5 text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="all">Alla prioriteter</option>
            <option value="urgent">Akut</option>
            <option value="high">Hög</option>
            <option value="medium">Medium</option>
            <option value="low">Låg</option>
          </select>
        </div>

        {/* Visit Count */}
        <p className="text-xs text-gray-600 mt-2">
          {sortedVisits.length} besök att tilldela
        </p>
      </div>

      {/* Visits List - 2 Column Grid */}
      <div className="flex-1 overflow-y-auto p-2">
        {sortedVisits.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-500 text-sm">Inga otilldelade besök</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-2">
            {sortedVisits.map((visit) => {
              const customer = customers.find((c) => c.id === visit.customerId);
              const measure = measures.find((m) => m.id === visit.measureId);

              if (!customer || !measure) return null;

              return (
                <UnassignedVisitCard
                  key={visit.id}
                  visit={visit}
                  customer={customer}
                  measure={measure}
                />
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
