import BASE_URL_ from "./services/AuthFunctions";
import * as SecureStore from "expo-secure-store";

const storeAccessToken = async (accessToken) => {
  await SecureStore.setItemAsync("accessToken", accessToken);
};

export const cardSearch = async (params) => {
  try {
    const response = await fetch(
      `${BASE_URL_}/cards/getAllCards?name=${params}`
    );
    const data = response.json();
    return data;
  } catch (error) {
    console.error("Could not retrieve card info:", error);
  }
};

export const inventoryCardSearch = async (params) => {
  try {
    const token = await SecureStore.getItemAsync("accessToken");
    const response = await fetch(
      `${BASE_URL_}/inventory/getUserInventory?name_partial=${params}`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    const data = response.json();
    return data;
  } catch (error) {
    console.error("Could not retrieve card info:", error);
  }
};
