import Alert from "@mui/material/Alert";
import CircularProgress from "@mui/material/CircularProgress";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useNavigate, useParams } from "react-router-dom";

import { createEmployee, getEmployee, updateEmployee } from "../api/employees";
import { EmployeeForm } from "../components/EmployeeForm";
import type { EmployeeInput } from "../types/employee";

export default function EmployeeFormPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);
  const employeeId = id ? Number(id) : NaN;

  const employeeQuery = useQuery({
    queryKey: ["employee", employeeId],
    queryFn: () => getEmployee(employeeId),
    enabled: isEdit && !Number.isNaN(employeeId),
  });

  const saveMutation = useMutation({
    mutationFn: async (values: EmployeeInput) => {
      if (isEdit) {
        return updateEmployee(employeeId, values);
      }
      return createEmployee(values);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["employees"] });
      navigate("/employees");
    },
  });

  if (isEdit && employeeQuery.isLoading) {
    return <CircularProgress aria-label="Loading employee" />;
  }

  if (isEdit && employeeQuery.isError) {
    return <Alert severity="error">{(employeeQuery.error as Error).message}</Alert>;
  }

  const initial = employeeQuery.data
    ? {
        employee_code: employeeQuery.data.employee_code,
        first_name: employeeQuery.data.first_name,
        last_name: employeeQuery.data.last_name,
        email: employeeQuery.data.email,
        job_title: employeeQuery.data.job_title,
        department: employeeQuery.data.department,
        country_code: employeeQuery.data.country_code,
        currency: employeeQuery.data.currency,
        annual_salary: employeeQuery.data.annual_salary,
        hire_date: employeeQuery.data.hire_date,
      }
    : null;

  return (
    <EmployeeForm
      title={isEdit ? "Edit employee" : "Add employee"}
      initialValues={initial}
      onSubmit={async (values) => {
        await saveMutation.mutateAsync(values);
      }}
      onCancel={() => navigate("/employees")}
    />
  );
}
