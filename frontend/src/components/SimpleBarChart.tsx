import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export type BarChartRow = {
  label: string;
  value: number;
};

type Props = {
  title: string;
  data: BarChartRow[];
  valueFormatter?: (n: number) => string;
  emptyMessage?: string;
};

export function SimpleBarChart({ title, data, valueFormatter, emptyMessage }: Props) {
  if (data.length === 0) {
    return (
      <Box>
        <Typography variant="subtitle1" gutterBottom>
          {title}
        </Typography>
        <Typography color="text.secondary">{emptyMessage ?? "No data"}</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="subtitle1" gutterBottom>
        {title}
      </Typography>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data} margin={{ top: 8, right: 8, left: 0, bottom: 48 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="label" angle={-35} textAnchor="end" interval={0} height={70} tick={{ fontSize: 11 }} />
          <YAxis tickFormatter={valueFormatter} width={72} tick={{ fontSize: 11 }} />
          <Tooltip formatter={(v: number) => (valueFormatter ? valueFormatter(v) : v)} />
          <Bar dataKey="value" fill="#1565c0" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </Box>
  );
}
