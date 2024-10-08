import BASE_URL from "./config";

const storeAccessToken = async (accessToken) => {
  await SecureStore.setItemAsync("accessToken", accessToken);
};

export const cardSearch = async (params) => {
  try {
    const response = await fetch(
      `${BASE_URL}/cards/getAllCards?name=${params}`
    );
    const data = response.json();
    return data;
  } catch (error) {
    console.error("Could not retrieve card info:", error);
  }
};
