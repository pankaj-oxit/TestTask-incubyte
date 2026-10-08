import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import MenuItem from "@mui/material/MenuItem";
import Stack from "@mui/material/Stack";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import { useEffect, useState } from "react";

import { COUNTRY_CURRENCY_MAP, COUNTRY_OPTIONS } from "../constants/countries";
import type { EmployeeInput } from "../types/employee";
import { ApiError } from "../api/client";

const emptyForm = (): EmployeeInput => ({
  employee_code: "",
  first_name: "",
  last_name: "",
  email: "",
  job_title: "",
  department: "",
  country_code: "US",
  currency: "USD",
  annual_salary: 0,
  hire_date: new Date().toISOString().slice(0, 10),
});

type Props = {
  title: string;
  initialValues: EmployeeInput | null;
  onSubmit: (values: EmployeeInput) => Promise<void>;
  onCancel: () => void;
};

export function EmployeeForm({ title, initialValues, onSubmit, onCancel }: Props) {
  const [values, setValues] = useState<EmployeeInput>(initialValues ?? emptyForm());
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (initialValues) {
      setValues(initialValues);
    }
  }, [initialValues]);

  const setField = <K extends keyof EmployeeInput>(key: K, value: EmployeeInput[K]) => {
    setValues((prev) => ({ ...prev, [key]: value }));
  };

  const onCountryChange = (country_code: string) => {
    const currency = COUNTRY_CURRENCY_MAP[country_code] ?? values.currency;
    setValues((prev) => ({ ...prev, country_code, currency }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await onSubmit({ ...values, annual_salary: Number(values.annual_salary) });
    } catch (err) {
      const message = err instanceof ApiError ? err.message : err instanceof Error ? err.message : "Save failed";
      setError(message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} noValidate>
      <Typography variant="h5" gutterBottom>
        {title}
      </Typography>
      {error && (
        <Alert severity="error" role="alert" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: { xs: "1fr", md: "1fr 1fr" },
          gap: 2,
          width: "100%",
        }}
      >
        <TextField
          fullWidth
          label="Employee code"
          required
          value={values.employee_code}
          onChange={(e) => setField("employee_code", e.target.value)}
        />
        <TextField
          fullWidth
          label="Email"
          type="email"
          required
          value={values.email}
          onChange={(e) => setField("email", e.target.value)}
        />
        <TextField
          fullWidth
          label="First name"
          required
          value={values.first_name}
          onChange={(e) => setField("first_name", e.target.value)}
        />
        <TextField
          fullWidth
          label="Last name"
          required
          value={values.last_name}
          onChange={(e) => setField("last_name", e.target.value)}
        />
        <TextField
          fullWidth
          label="Job title"
          required
          value={values.job_title}
          onChange={(e) => setField("job_title", e.target.value)}
        />
        <TextField
          fullWidth
          label="Department"
          required
          value={values.department}
          onChange={(e) => setField("department", e.target.value)}
        />
        <TextField
          fullWidth
          select
          label="Country"
          required
          value={values.country_code}
          onChange={(e) => onCountryChange(e.target.value)}
        >
          {COUNTRY_OPTIONS.map((c) => (
            <MenuItem key={c} value={c}>
              {c}
            </MenuItem>
          ))}
        </TextField>
        <TextField fullWidth label="Currency" value={values.currency} InputProps={{ readOnly: true }} />
        <TextField
          fullWidth
          label="Annual salary (local)"
          type="number"
          required
          inputProps={{ min: 1 }}
          value={values.annual_salary || ""}
          onChange={(e) => setField("annual_salary", Number(e.target.value))}
        />
        <TextField
          fullWidth
          label="Hire date"
          type="date"
          required
          InputLabelProps={{ shrink: true }}
          value={values.hire_date}
          onChange={(e) => setField("hire_date", e.target.value)}
        />
        <Stack direction="row" spacing={2} sx={{ gridColumn: { xs: "1", md: "1 / -1" }, pt: 1 }}>
          <Button type="submit" variant="contained" disabled={submitting}>
            Save
          </Button>
          <Button type="button" variant="outlined" onClick={onCancel}>
            Cancel
          </Button>
        </Stack>
      </Box>
    </Box>
  );
}
