import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { EmployeeForm } from "../components/EmployeeForm";

describe("EmployeeForm", () => {
  it("shows API validation error from server response", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn().mockRejectedValue(new Error("Currency 'EUR' does not match country 'US'"));

    render(
      <EmployeeForm
        title="Add employee"
        initialValues={null}
        onSubmit={onSubmit}
        onCancel={() => {}}
      />,
    );

    await user.type(screen.getByLabelText(/employee code/i), "EMP-T-01");
    await user.type(screen.getByLabelText(/first name/i), "Test");
    await user.type(screen.getByLabelText(/last name/i), "User");
    await user.type(screen.getByLabelText(/email/i), "t@acme.example");
    await user.type(screen.getByLabelText(/job title/i), "Engineer");
    await user.type(screen.getByLabelText(/department/i), "Engineering");
    await user.type(screen.getByLabelText(/annual salary/i), "80000");
    await user.click(screen.getByRole("button", { name: /save/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/currency/i);
    expect(onSubmit).toHaveBeenCalled();
  });
});
