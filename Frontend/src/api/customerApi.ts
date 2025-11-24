import { apiClient } from './client';

export interface Customer {
  id: number;
  first_name: string;
  last_name: string;
  key_number: number;
  address: string;
  care_level: 'high' | 'medium' | 'low';
  gender: 'male' | 'female' | 'unspecified';
  approved_hours: number;
  is_active: boolean;
  created: string;
  updated: string;
}

export interface CustomerCreateData {
  first_name: string;
  last_name: string;
  key_number: number;
  address: string;
  care_level: 'high' | 'medium' | 'low';
  gender: 'male' | 'female' | 'unspecified';
  approved_hours: number;
  is_active: boolean;
}

export const fetchCustomers = async (): Promise<Customer[]> => {
  const response = await apiClient.get('/customers/');
  return response.data;
};

export const fetchCustomerById = async (customerId: number): Promise<Customer> => {
  const response = await apiClient.get(`/customers/${customerId}`);
  return response.data;
};

export const createCustomer = async (data: CustomerCreateData): Promise<Customer> => {
  const response = await apiClient.post('/customers/', data);
  return response.data;
};

export const updateCustomer = async (
  customerId: number,
  data: Partial<CustomerCreateData>
): Promise<Customer> => {
  const response = await apiClient.patch(`/customers/${customerId}`, data);
  return response.data;
};

export const deleteCustomer = async (customerId: number): Promise<void> => {
  await apiClient.delete(`/customers/${customerId}`);
};
