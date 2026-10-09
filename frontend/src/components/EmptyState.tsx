import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

type Props = {
  message: string;
};

export function EmptyState({ message }: Props) {
  return (
    <Box p={4} role="status">
      <Typography color="text.secondary">{message}</Typography>
    </Box>
  );
}
