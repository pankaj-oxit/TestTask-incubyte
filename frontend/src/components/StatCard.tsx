import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";

type Props = {
  label: string;
  value: string;
};

export function StatCard({ label, value }: Props) {
  return (
    <Card variant="outlined" sx={{ height: "100%" }}>
      <CardContent>
        <Typography color="text.secondary" variant="body2" gutterBottom>
          {label}
        </Typography>
        <Typography variant="h5" component="p">
          {value}
        </Typography>
      </CardContent>
    </Card>
  );
}
