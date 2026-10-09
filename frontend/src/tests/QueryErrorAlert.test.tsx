import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { QueryErrorAlert } from "../components/QueryErrorAlert";

describe("QueryErrorAlert", () => {
  it("shows message and calls onRetry when retry is clicked", async () => {
    const onRetry = vi.fn();
    render(<QueryErrorAlert message="Network failed" onRetry={onRetry} />);

    expect(screen.getByRole("alert")).toHaveTextContent("Network failed");
    await userEvent.click(screen.getByRole("button", { name: /retry/i }));
    expect(onRetry).toHaveBeenCalledOnce();
  });
});
