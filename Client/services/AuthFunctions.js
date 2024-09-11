import * as SecureStore from "expo-secure-store";
import jwtDecode from "jwt-decode";

export const BASE_URL_ =
  "http://ec2-3-135-192-227.us-east-2.compute.amazonaws.com:8000/";
export const BASE_URL = "http://127.0.0.1:5555/";

const storeTokens = async (accessToken, refreshToken) => {
  try {
    await SecureStore.setItemAsync("accessToken", accessToken);
    await SecureStore.setItemAsync("refreshToken", refreshToken);
  } catch (e) {
    console.error("Error Storing tokens", e);
  }

  // console.log('zzzz')
  // let result = await SecureStore.getItemAsync('accessToken');
  // if (result) {
  //     console.log(`Access_Token is ${result}`)
  // }

  // let refresht = await SecureStore.getItemAsync('refreshToken');
  // if (refresht) {
  //     console.log(`Refresh_Token is ${refresht}`)
  // }
  // console.log('post zzzz')
};

const clearTokens = async () => {
  try {
    await SecureStore.deleteItemAsync("accessToken");
    await SecureStore.deleteItemAsync("refreshToken");
  } catch (e) {
    console.log("Error deleting tokens", e);
  }
};

const loginInit = async (username, password) => {
  console.log(JSON.stringify({ username, password }));
  console.log(BASE_URL);
  try {
    const response = await fetch(`${BASE_URL_}/Login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      console.log("Login Failed");
      throw new Error("Login failed");
    }

    const data = await response.json();
    const { accessToken, refreshToken } = data;
    await storeTokens(accessToken, refreshToken);
  } catch (e) {
    console.log("Error Logging in", e);
    throw e;
  }
};

const logout = async () => {
  await clearTokens();

  console.log("zzzz");
  let result = await SecureStore.getItemAsync("accessToken");
  if (result) {
    console.log(`Access_Token is ${result}`);
  } else {
    console.log("Access token_cleared");
  }

  let refresht = await SecureStore.getItemAsync("refreshToken");
  if (refresht) {
    console.log(`Refresh_Token is ${refresht}`);
  } else {
    console.log("refresh token cleared");
  }
  console.log("post zzzz");

  //Send request to server to delete refresh token as well
};

const getUserId = async () => {
  try {
    const accessToken = await SecureStore.getItemAsync("accessToken");
    if (accessToken) {
      const decoded = jwtDecode(accessToken);
      return decoded.user_id;
    }
    return null;
  } catch (e) {
    console.log("Error decoding token", e);
    return null;
  }
};

const isTokenExpired = () => {
  let storedToken = SecureStore.getItem("accessToken");
  if (storedToken) {
    const decoded = jwtDecode(storedToken);
    const currentTime = Date.now() / 1000; //Date.now returns milliseconds after epoch
    return decoded.expiration < currentTime;
  }
  return false;
};

export {
  loginInit,
  logout,
  clearTokens,
  storeTokens,
  getUserId,
  isTokenExpired,
};
