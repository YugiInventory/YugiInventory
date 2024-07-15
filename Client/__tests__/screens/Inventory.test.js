import React from "react";
import { render, waitFor, act } from "@testing-library/react-native";
import Inventory from "../../screens/Inventory";
import BASE_URL from "../../config";

// Mock the fetch function
global.fetch = jest.fn();

describe("Inventory Component", () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  it("renders loading indicator initially", () => {
    const { getByTestId } = render(<Inventory />);
    expect(getByTestId("loading-indicator")).toBeTruthy();
  });

  it("renders the list of cards after fetching", async () => {
    const mockCards = {
      cards: [
        {
          id: 1,
          name: "Test Card",
          card_image: "https://example.com/image.jpg",
          card_race: "Test Race",
          card_type: "Monster",
          attack: 1000,
          defense: 1000,
          description: "Test description",
        },
      ],
    };

    fetch.mockResolvedValueOnce({
      json: jest.fn().mockResolvedValue(mockCards),
    });

    const { getByText, queryByTestId } = render(<Inventory />);

    await waitFor(() => {
      expect(queryByTestId("loading-indicator")).toBeNull();
      expect(getByText("Test Card")).toBeTruthy();
      expect(getByText("Test Race Monster")).toBeTruthy();
      expect(getByText("ATK: 1000 DEF: 1000")).toBeTruthy();
      expect(getByText("Test description")).toBeTruthy();
    });

    expect(fetch).toHaveBeenCalledWith(`${BASE_URL}/cards`);
  });

  it("renders empty state when no cards are found", async () => {
    fetch.mockResolvedValueOnce({
      json: jest.fn().mockResolvedValue({ cards: [] }),
    });

    const { getByText, queryByTestId } = render(<Inventory />);

    await waitFor(() => {
      expect(queryByTestId("loading-indicator")).toBeNull();
      expect(getByText("No cards found")).toBeTruthy();
    });
  });

  it("handles fetch error", async () => {
    console.error = jest.fn(); // Mock console.error
    fetch.mockRejectedValueOnce(new Error("API Error"));

    const { queryByTestId } = render(<Inventory />);

    await waitFor(() => {
      expect(queryByTestId("loading-indicator")).toBeNull();
      expect(console.error).toHaveBeenCalledWith(
        "Error fetching cards:",
        expect.any(Error)
      );
    });
  });
});
