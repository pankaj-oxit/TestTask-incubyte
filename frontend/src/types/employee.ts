export type Employee = {
  id: number;
  employee_code: string;
  first_name: string;
  last_name: string;
  email: string;
  job_title: string;
  department: string;
  country_code: string;
  currency: string;
  annual_salary: number;
  hire_date: string;
  created_at: string;
  updated_at: string;
};

export type EmployeeInput = Omit<Employee, "id" | "created_at" | "updated_at">;

export type EmployeeListResponse = {
  items: Employee[];
  total: number;
  page: number;
  page_size: number;
};

export type MetaFilters = {
  countries: string[];
  departments: string[];
  job_titles: string[];
};

export type ListEmployeesParams = {
  page?: number;
  page_size?: number;
  search?: string;
  country?: string;
  job_title?: string;
  department?: string;
  sort_by?: string;
  order?: "asc" | "desc";
};
