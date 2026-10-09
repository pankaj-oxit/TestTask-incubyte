import Alert from "@mui/material/Alert";
import Button from "@mui/material/Button";

type Props = {
  message: string;
  onRetry: () => void;
};

export function QueryErrorAlert({ message, onRetry }: Props) {
  return (
    <Alert
      severity="error"
      role="alert"
      action={
        <Button color="inherit" size="small" onClick={onRetry}>
          Retry
        </Button>
      }
    >
      {message}
    </Alert>
  );
}
