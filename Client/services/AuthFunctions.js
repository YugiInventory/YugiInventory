import * as SecureStore from "expo-secure-store";
import { jwtDecode } from "jwt-decode";

export const BASE_URL_ =
  "http://ec2-3-135-192-227.us-east-2.compute.amazonaws.com:8000/";
export const BASE_URL = "http://localhost:5555/"; //http://localhost:5555/user/createUser or 127.0.0.1

const storeTokens = async (accessToken, refreshToken) => {
  try {
    await SecureStore.setItemAsync("accessToken", accessToken);
    await SecureStore.setItemAsync("refreshToken", refreshToken);
  } catch (e) {
    console.error("Error Storing tokens", e);
  }
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
  console.log(BASE_URL_);
  try {
    const response = await fetch(`${BASE_URL_}/auth/Login`, {
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

const loginWithToken = async () => {
  const refreshToken = await SecureStore.getItemAsync("refreshToken");
  if (refreshToken) {
    try {
      const response = await fetch(`${BASE_URL}/auth/Login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ refreshToken }),
      });
      if (!response.ok) {
        console.log("Login Failed");
        throw new Error("Login failed");
      } else {
        const data = await response.json();
      }
    } catch (e) {}
  }
};

const logout = async () => {
  //get user_id
  //Send Req to server
  //Delete Tokens
  try {
    user_id = await getUserId();
    await clearTokens();
    const response = await fetch(`${BASE_URL_}/auth/Logout`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ user_id }),
    });
    if (response.ok) {
      console.log("Deleted");
    } else {
      console.log("oh brother this guy stinks");
    }
  } catch (error) {
    console.log(error);
  }

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

const isTokenExpired = async () => {
  let storedToken = await SecureStore.getItemAsync("accessToken");
  if (storedToken) {
    const decoded = jwtDecode(storedToken);
    console.log("Decoded Token:", decoded);
    const currentTime = Date.now() / 1000; //Date.now returns milliseconds after epoch
    return decoded.exp < currentTime;
  } else {
    console.log("no token");
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
