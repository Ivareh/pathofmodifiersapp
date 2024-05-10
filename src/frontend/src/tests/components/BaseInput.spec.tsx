import { render, screen } from "@testing-library/react";
import { BaseInput } from "../../components/Input/ItemBaseTypeInputComp/BaseInput";

describe("BaseInput", () => {
  test("renders BaseInput component", () => {
    render(<BaseInput />);
    const baseInput = screen.getByText("Base Type");
    expect(baseInput).toHaveLength(9);
  });
});
