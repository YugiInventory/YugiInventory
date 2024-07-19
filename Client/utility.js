import BASE_URL from "./config";

const storeAccessToken = async (accessToken) => {
  await SecureStore.setItemAsync("accessToken", accessToken);
};

export const cardSearch = async (params) => {
  try {
    const response =
      typeof params === "string"
        ? await fetch(`${BASE_URL}/cards?name=${params}`)
        : await fetch(`${BASE_URL}/card/${params}`);

    const data = response.json();
  } catch (error) {
    console.error("Could not retrieve card info:", error);
  }
};
