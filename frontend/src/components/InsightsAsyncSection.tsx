import Box from "@mui/material/Box";
import CircularProgress from "@mui/material/CircularProgress";
import type { ReactNode } from "react";

import { QueryErrorAlert } from "./QueryErrorAlert";

type Props = {
  isPending: boolean;
  isFetching: boolean;
  isError: boolean;
  error: Error | null;
  onRetry: () => void;
  busyLabel: string;
  children: ReactNode;
};

export function InsightsAsyncSection({
  isPending,
  isFetching,
  isError,
  error,
  onRetry,
  busyLabel,
  children,
}: Props) {
  if (isError && error) {
    return <QueryErrorAlert message={error.message} onRetry={onRetry} />;
  }

  const showOverlay = isPending || isFetching;

  return (
    <Box position="relative">
      {children}
      {showOverlay && (
        <Box
          aria-busy="true"
          aria-label={busyLabel}
          role="status"
          sx={{
            position: "absolute",
            inset: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            bgcolor: "rgba(255, 255, 255, 0.65)",
            zIndex: 1,
            borderRadius: 1,
          }}
        >
          <CircularProgress size={32} />
        </Box>
      )}
    </Box>
  );
}
