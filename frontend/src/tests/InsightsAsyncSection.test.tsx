import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { InsightsAsyncSection } from "../components/InsightsAsyncSection";

describe("InsightsAsyncSection", () => {
  it("shows busy overlay while fetching without unmounting children", () => {
    render(
      <InsightsAsyncSection
        isPending={false}
        isFetching
        isError={false}
        error={null}
        onRetry={vi.fn()}
        busyLabel="Updating job title insights"
      >
        <p>Section content</p>
      </InsightsAsyncSection>,
    );

    expect(screen.getByText("Section content")).toBeInTheDocument();
    expect(screen.getByLabelText("Updating job title insights")).toBeInTheDocument();
  });
});
