import Alert from "@mui/material/Alert";
import Typography from "@mui/material/Typography";

/** Phase 7 — insights charts and stat cards */
export default function InsightsPage() {
  return (
    <>
      <Typography variant="h5" gutterBottom>
        Insights
      </Typography>
      <Alert severity="info">
        Pay analytics (summary, by country, by job title, distribution) ship in Phase 7.
      </Alert>
    </>
  );
}
