import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import CircularProgress from "@mui/material/CircularProgress";
import Grid from "@mui/material/Grid2";
import MenuItem from "@mui/material/MenuItem";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { useMemo, useState } from "react";

import {
  fetchInsightsByCountry,
  fetchInsightsByJobTitle,
  fetchInsightsDistribution,
  fetchInsightsSummary,
} from "../api/insights";
import { fetchMetaFilters } from "../api/employees";
import { COUNTRY_CURRENCY_MAP } from "../constants/countries";
import { EmptyState } from "../components/EmptyState";
import { InsightsAsyncSection } from "../components/InsightsAsyncSection";
import { QueryErrorAlert } from "../components/QueryErrorAlert";
import { SimpleBarChart } from "../components/SimpleBarChart";
import { StatCard } from "../components/StatCard";
import { formatLocalSalary } from "../utils/formatSalary";
import { formatUsd } from "../utils/formatUsd";

const FX_AS_OF = "2024-01-01";

export default function InsightsPage() {
  const [jobTitleCountry, setJobTitleCountry] = useState("");
  const [distCountry, setDistCountry] = useState("");
  const [distJobTitle, setDistJobTitle] = useState("");

  const filtersQuery = useQuery({
    queryKey: ["meta-filters"],
    queryFn: fetchMetaFilters,
  });

  const summaryQuery = useQuery({
    queryKey: ["insights-summary"],
    queryFn: fetchInsightsSummary,
  });

  const byCountryQuery = useQuery({
    queryKey: ["insights-by-country"],
    queryFn: () => fetchInsightsByCountry(),
  });

  const byJobTitleQuery = useQuery({
    queryKey: ["insights-by-job-title", jobTitleCountry],
    queryFn: () =>
      fetchInsightsByJobTitle({
        country: jobTitleCountry || undefined,
      }),
    placeholderData: keepPreviousData,
  });

  const distributionQuery = useQuery({
    queryKey: ["insights-distribution", distCountry, distJobTitle],
    queryFn: () =>
      fetchInsightsDistribution({
        country: distCountry || undefined,
        job_title: distJobTitle || undefined,
      }),
    placeholderData: keepPreviousData,
  });

  const countryChartData = useMemo(
    () =>
      (byCountryQuery.data ?? []).map((r) => ({
        label: r.country_code,
        value: r.average_salary_usd,
      })),
    [byCountryQuery.data],
  );

  const jobTitleChartData = useMemo(
    () =>
      (byJobTitleQuery.data ?? []).slice(0, 15).map((r) => ({
        label: r.job_title.length > 18 ? `${r.job_title.slice(0, 16)}…` : r.job_title,
        value: r.average_salary_usd,
      })),
    [byJobTitleQuery.data],
  );

  const distributionChartData = useMemo(
    () =>
      (distributionQuery.data?.buckets ?? []).map((b) => ({
        label: b.range,
        value: b.count,
      })),
    [distributionQuery.data],
  );

  const bootstrapping =
    (summaryQuery.isPending && !summaryQuery.data) ||
    (byCountryQuery.isPending && !byCountryQuery.data);

  const bootstrapError = summaryQuery.error ?? byCountryQuery.error;

  const refetchBootstrap = () => {
    void summaryQuery.refetch();
    void byCountryQuery.refetch();
    void distributionQuery.refetch();
    void filtersQuery.refetch();
  };

  if (bootstrapping) {
    return (
      <Box display="flex" justifyContent="center" p={4} role="status">
        <CircularProgress aria-label="Loading insights" />
      </Box>
    );
  }

  if (bootstrapError) {
    return (
      <Stack spacing={2} p={2}>
        <Typography variant="h5">Insights</Typography>
        <QueryErrorAlert message={(bootstrapError as Error).message} onRetry={refetchBootstrap} />
      </Stack>
    );
  }

  const summary = summaryQuery.data!;

  return (
    <Stack spacing={3}>
      <Typography variant="h5">Insights</Typography>

      {filtersQuery.isError && (
        <QueryErrorAlert
          message={`Filters unavailable: ${(filtersQuery.error as Error).message}`}
          onRetry={() => filtersQuery.refetch()}
        />
      )}

      {summary.headcount === 0 && (
        <Alert severity="warning" role="status">
          No employee records yet. Seed the database or add employees to see insights.
        </Alert>
      )}

      <Grid container spacing={2}>
        <Grid size={{ xs: 12, md: 4 }}>
          <StatCard label="Headcount" value={String(summary.headcount)} />
        </Grid>
        <Grid size={{ xs: 12, md: 4 }}>
          <StatCard label="Average salary (USD)" value={formatUsd(summary.average_salary_usd)} />
        </Grid>
        <Grid size={{ xs: 12, md: 4 }}>
          <StatCard label="Median salary (USD)" value={formatUsd(summary.median_salary_usd)} />
        </Grid>
      </Grid>

      <Alert severity="info" variant="outlined">
        All org-wide figures are converted to USD using fixed rates (as of {FX_AS_OF}). Salary insights
        are shown by country and job title. Department breakdown is on the roadmap.
      </Alert>

      <Paper sx={{ p: 2 }}>
        <Grid container spacing={3}>
          <Grid size={{ xs: 12, lg: 6 }}>
            <SimpleBarChart
              title="Average pay by country (USD)"
              data={countryChartData}
              valueFormatter={formatUsd}
            />
          </Grid>
          <Grid size={{ xs: 12, lg: 6 }}>
            <Typography variant="subtitle1" gutterBottom>
              By country (detail)
            </Typography>
            <TableContainer sx={{ maxHeight: 320 }}>
              <Table size="small" stickyHeader>
                <TableHead>
                  <TableRow>
                    <TableCell>Country</TableCell>
                    <TableCell align="right">Count</TableCell>
                    <TableCell align="right">Avg (local)</TableCell>
                    <TableCell align="right">Avg (USD)</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {(byCountryQuery.data ?? []).length === 0 && (
                    <TableRow>
                      <TableCell colSpan={4}>
                        <EmptyState message="No country breakdown available." />
                      </TableCell>
                    </TableRow>
                  )}
                  {(byCountryQuery.data ?? []).map((row) => (
                    <TableRow key={row.country_code}>
                      <TableCell>{row.country_code}</TableCell>
                      <TableCell align="right">{row.headcount}</TableCell>
                      <TableCell align="right">
                        {formatLocalSalary(
                          Math.round(row.average_salary_local),
                          COUNTRY_CURRENCY_MAP[row.country_code] ?? "USD",
                        )}
                      </TableCell>
                      <TableCell align="right">{formatUsd(row.average_salary_usd)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Grid>
        </Grid>
      </Paper>

      <Paper sx={{ p: 2 }}>
        <Stack direction={{ xs: "column", sm: "row" }} spacing={2} mb={2}>
          <TextField
            select
            label="Country filter (job title)"
            size="small"
            value={jobTitleCountry}
            onChange={(e) => setJobTitleCountry(e.target.value)}
            sx={{ minWidth: 200 }}
          >
            <MenuItem value="">All countries</MenuItem>
            {(filtersQuery.data?.countries ?? []).map((c) => (
              <MenuItem key={c} value={c}>
                {c}
              </MenuItem>
            ))}
          </TextField>
        </Stack>
        <InsightsAsyncSection
          isPending={byJobTitleQuery.isPending}
          isFetching={byJobTitleQuery.isFetching}
          isError={byJobTitleQuery.isError}
          error={(byJobTitleQuery.error as Error) ?? null}
          onRetry={() => byJobTitleQuery.refetch()}
          busyLabel="Updating job title insights"
        >
          <Grid container spacing={3}>
            <Grid size={{ xs: 12, lg: 6 }}>
              <SimpleBarChart
                title="Average pay by job title (USD, top 15)"
                data={jobTitleChartData}
                valueFormatter={formatUsd}
              />
            </Grid>
            <Grid size={{ xs: 12, lg: 6 }}>
              <Typography variant="subtitle1" gutterBottom>
                By job title (detail)
              </Typography>
              <TableContainer sx={{ maxHeight: 320 }}>
                <Table size="small" stickyHeader>
                  <TableHead>
                    <TableRow>
                      <TableCell>Job title</TableCell>
                      <TableCell align="right">Count</TableCell>
                      <TableCell align="right">Avg (USD)</TableCell>
                      <TableCell align="right">Median (USD)</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {(byJobTitleQuery.data ?? []).length === 0 && !byJobTitleQuery.isFetching && (
                      <TableRow>
                        <TableCell colSpan={4}>
                          <EmptyState message="No job titles match this filter." />
                        </TableCell>
                      </TableRow>
                    )}
                    {(byJobTitleQuery.data ?? []).map((row) => (
                      <TableRow key={row.job_title}>
                        <TableCell>{row.job_title}</TableCell>
                        <TableCell align="right">{row.headcount}</TableCell>
                        <TableCell align="right">{formatUsd(row.average_salary_usd)}</TableCell>
                        <TableCell align="right">{formatUsd(row.median_salary_usd)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Grid>
          </Grid>
        </InsightsAsyncSection>
      </Paper>

      <Paper sx={{ p: 2 }}>
        <Typography variant="subtitle1" gutterBottom>
          Salary distribution (USD buckets)
        </Typography>
        <Stack direction={{ xs: "column", sm: "row" }} spacing={2} mb={2}>
          <TextField
            select
            label="Country"
            size="small"
            value={distCountry}
            onChange={(e) => setDistCountry(e.target.value)}
            sx={{ minWidth: 140 }}
          >
            <MenuItem value="">All</MenuItem>
            {(filtersQuery.data?.countries ?? []).map((c) => (
              <MenuItem key={c} value={c}>
                {c}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            label="Job title"
            size="small"
            value={distJobTitle}
            onChange={(e) => setDistJobTitle(e.target.value)}
            sx={{ minWidth: 220 }}
          >
            <MenuItem value="">All</MenuItem>
            {(filtersQuery.data?.job_titles ?? []).map((t) => (
              <MenuItem key={t} value={t}>
                {t}
              </MenuItem>
            ))}
          </TextField>
        </Stack>
        <InsightsAsyncSection
          isPending={distributionQuery.isPending}
          isFetching={distributionQuery.isFetching}
          isError={distributionQuery.isError}
          error={(distributionQuery.error as Error) ?? null}
          onRetry={() => distributionQuery.refetch()}
          busyLabel="Updating salary distribution"
        >
          <SimpleBarChart
            title={`Headcount by bucket (${distributionQuery.data?.headcount ?? 0} employees)`}
            data={distributionChartData}
            valueFormatter={(n) => String(n)}
          />
        </InsightsAsyncSection>
      </Paper>
    </Stack>
  );
}
