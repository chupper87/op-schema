import { apiClient } from './client';

export interface Measure {
  id: number;
  name: string;
  defaultDuration: number;
  text: string | null;
  time_of_day: string | null;
  time_flexibility: string | null;
  created: string;
}

export interface CustomerMeasure {
  id: number;
  customer_id: number;
  measure_id: number;
  measure_name: string;
  customer_duration: number | null;
  frequency: string;
  days_of_week: string[] | null;
  occurrences_per_week: number | null;
  customer_notes: string | null;
  customer_time_of_day: string | null;
  customer_time_flexibility: string | null;
  schedule_info: string | null;
  created: string;
}

export interface CustomerMeasureCreateData {
  measure_id: number;
  customer_duration?: number | null;
  frequency: string;
  days_of_week?: string[] | null;
  occurrences_per_week?: number | null;
  customer_notes?: string | null;
  customer_time_of_day?: string | null;
  customer_time_flexibility?: string | null;
  schedule_info?: string | null;
}

export const fetchCustomerMeasures = async (customerId: number): Promise<CustomerMeasure[]> => {
  const response = await apiClient.get(`/customers/${customerId}/measures`);
  return response.data;
};

export const createCustomerMeasure = async (
  customerId: number,
  data: CustomerMeasureCreateData
): Promise<CustomerMeasure> => {
  const response = await apiClient.post(`/customers/${customerId}/measures`, data);
  return response.data;
};

export const deleteCustomerMeasure = async (
  customerId: number,
  customerMeasureId: number
): Promise<void> => {
  await apiClient.delete(`/customers/${customerId}/measures/${customerMeasureId}`);
};

export const fetchMeasures = async (isActive: boolean = true): Promise<Measure[]> => {
  const params = new URLSearchParams();
  if (isActive !== undefined) {
    params.append('is_active', isActive.toString());
  }

  const response = await apiClient.get(`/measures/?${params.toString()}`);

  return response.data;
};
