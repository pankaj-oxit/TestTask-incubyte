import AddIcon from "@mui/icons-material/Add";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";
import IconButton from "@mui/material/IconButton";
import MenuItem from "@mui/material/MenuItem";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TablePagination from "@mui/material/TablePagination";
import TableRow from "@mui/material/TableRow";
import TableSortLabel from "@mui/material/TableSortLabel";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import DeleteOutlineIcon from "@mui/icons-material/DeleteOutline";
import EditIcon from "@mui/icons-material/Edit";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

import { deleteEmployee, fetchMetaFilters, listEmployees } from "../api/employees";
import { ConfirmDialog } from "../components/ConfirmDialog";
import { EmptyState } from "../components/EmptyState";
import { QueryErrorAlert } from "../components/QueryErrorAlert";
import { formatLocalSalary } from "../utils/formatSalary";

const SORT_COLUMNS = [
  { id: "last_name", label: "Name" },
  { id: "employee_code", label: "Code" },
  { id: "email", label: "Email" },
  { id: "job_title", label: "Job title" },
  { id: "department", label: "Department" },
  { id: "country_code", label: "Country" },
  { id: "annual_salary", label: "Salary" },
  { id: "hire_date", label: "Hire date" },
] as const;

export default function EmployeesPage() {
  const queryClient = useQueryClient();
  const [page, setPage] = useState(0);
  const [rowsPerPage] = useState(25);
  const [searchInput, setSearchInput] = useState("");
  const [search, setSearch] = useState("");
  const [country, setCountry] = useState("");
  const [jobTitle, setJobTitle] = useState("");
  const [department, setDepartment] = useState("");
  const [sortBy, setSortBy] = useState<string>("last_name");
  const [order, setOrder] = useState<"asc" | "desc">("asc");
  const [deleteId, setDeleteId] = useState<number | null>(null);

  useEffect(() => {
    const t = setTimeout(() => {
      setSearch(searchInput);
      setPage(0);
    }, 300);
    return () => clearTimeout(t);
  }, [searchInput]);

  const filtersQuery = useQuery({
    queryKey: ["meta-filters"],
    queryFn: fetchMetaFilters,
  });

  const listQuery = useQuery({
    queryKey: ["employees", page, rowsPerPage, search, country, jobTitle, department, sortBy, order],
    queryFn: () =>
      listEmployees({
        page: page + 1,
        page_size: rowsPerPage,
        search: search || undefined,
        country: country || undefined,
        job_title: jobTitle || undefined,
        department: department || undefined,
        sort_by: sortBy,
        order,
      }),
  });

  const deleteMutation = useMutation({
    mutationFn: deleteEmployee,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["employees"] });
      setDeleteId(null);
    },
  });

  const handleSort = (columnId: string) => {
    if (sortBy === columnId) {
      setOrder((o) => (o === "asc" ? "desc" : "asc"));
    } else {
      setSortBy(columnId);
      setOrder("asc");
    }
    setPage(0);
  };

  const rows = listQuery.data?.items ?? [];
  const total = listQuery.data?.total ?? 0;

  const filterOptions = useMemo(
    () => ({
      countries: filtersQuery.data?.countries ?? [],
      jobTitles: filtersQuery.data?.job_titles ?? [],
      departments: filtersQuery.data?.departments ?? [],
    }),
    [filtersQuery.data],
  );

  return (
    <Box>
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h5">Employees</Typography>
        <Button component={Link} to="/employees/new" variant="contained" startIcon={<AddIcon />}>
          Add employee
        </Button>
      </Stack>

      <Stack direction={{ xs: "column", md: "row" }} spacing={2} mb={2}>
        <TextField
          label="Search name or email"
          size="small"
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          sx={{ minWidth: 220 }}
          inputProps={{ "aria-label": "Search employees by name or email" }}
        />
        <TextField
          select
          label="Country"
          size="small"
          value={country}
          onChange={(e) => {
            setCountry(e.target.value);
            setPage(0);
          }}
          sx={{ minWidth: 120 }}
        >
          <MenuItem value="">All</MenuItem>
          {filterOptions.countries.map((c) => (
            <MenuItem key={c} value={c}>
              {c}
            </MenuItem>
          ))}
        </TextField>
        <TextField
          select
          label="Job title"
          size="small"
          value={jobTitle}
          onChange={(e) => {
            setJobTitle(e.target.value);
            setPage(0);
          }}
          sx={{ minWidth: 180 }}
        >
          <MenuItem value="">All</MenuItem>
          {filterOptions.jobTitles.map((t) => (
            <MenuItem key={t} value={t}>
              {t}
            </MenuItem>
          ))}
        </TextField>
        <TextField
          select
          label="Department"
          size="small"
          value={department}
          onChange={(e) => {
            setDepartment(e.target.value);
            setPage(0);
          }}
          sx={{ minWidth: 160 }}
        >
          <MenuItem value="">All</MenuItem>
          {filterOptions.departments.map((d) => (
            <MenuItem key={d} value={d}>
              {d}
            </MenuItem>
          ))}
        </TextField>
      </Stack>

      {filtersQuery.isError && (
        <QueryErrorAlert
          message={`Filters unavailable: ${(filtersQuery.error as Error).message}`}
          onRetry={() => filtersQuery.refetch()}
        />
      )}

      {listQuery.isError && (
        <QueryErrorAlert
          message={(listQuery.error as Error).message}
          onRetry={() => listQuery.refetch()}
        />
      )}

      {deleteMutation.isError && (
        <Alert severity="error" role="alert" sx={{ mb: 2 }}>
          Delete failed: {(deleteMutation.error as Error).message}
        </Alert>
      )}

      <TableContainer component={Paper}>
        {listQuery.isLoading ? (
          <Box p={4} display="flex" justifyContent="center" role="status">
            <CircularProgress aria-label="Loading employees" />
          </Box>
        ) : rows.length === 0 ? (
          <EmptyState message="No employees match your filters." />
        ) : (
          <Table size="small">
            <TableHead>
              <TableRow>
                {SORT_COLUMNS.map((col) => (
                  <TableCell key={col.id}>
                    <TableSortLabel
                      active={sortBy === col.id}
                      direction={sortBy === col.id ? order : "asc"}
                      onClick={() => handleSort(col.id)}
                    >
                      {col.label}
                    </TableSortLabel>
                  </TableCell>
                ))}
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.map((row) => (
                <TableRow key={row.id} hover>
                  <TableCell>
                    {row.first_name} {row.last_name}
                  </TableCell>
                  <TableCell>{row.employee_code}</TableCell>
                  <TableCell>{row.email}</TableCell>
                  <TableCell>{row.job_title}</TableCell>
                  <TableCell>{row.department}</TableCell>
                  <TableCell>{row.country_code}</TableCell>
                  <TableCell>{formatLocalSalary(row.annual_salary, row.currency)}</TableCell>
                  <TableCell>{row.hire_date}</TableCell>
                  <TableCell align="right">
                    <IconButton component={Link} to={`/employees/${row.id}/edit`} aria-label="Edit">
                      <EditIcon fontSize="small" />
                    </IconButton>
                    <IconButton aria-label="Delete" onClick={() => setDeleteId(row.id)}>
                      <DeleteOutlineIcon fontSize="small" />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </TableContainer>

      <TablePagination
        component="div"
        count={total}
        page={page}
        onPageChange={(_, p) => setPage(p)}
        rowsPerPage={rowsPerPage}
        rowsPerPageOptions={[25]}
      />

      <ConfirmDialog
        open={deleteId !== null}
        title="Delete employee?"
        message="This cannot be undone."
        onCancel={() => setDeleteId(null)}
        onConfirm={() => deleteId !== null && deleteMutation.mutate(deleteId)}
      />
    </Box>
  );
}
