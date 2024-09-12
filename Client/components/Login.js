import React, { useState } from "react";
import * as SecureStore from "expo-secure-store";
import { Text, TextInput, StyleSheet, View, Button } from "react-native";
import { useForm, Controller } from "react-hook-form";
import CardInfo from "./CardInfo";
import {
  storeTokens,
  clearTokens,
  loginInit,
  getUserId,
  BASE_URL_,
  BASE_URL,
} from "../services/AuthFunctions";
import PaginationBar from "../services/Pagination";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [createusername, setcreateusername] = useState("");
  const [createpassword, setcreatepassword] = useState("");
  const [createEmail, setcreateEmail] = useState("");

  const BASE = BASE_URL_;
  const BASE2 = BASE_URL;

  const handleLogin = () => {
    //Login Have the user submit the login credentials.
    //Get a return back from the server and if it is good then we will also have a refreshToken and an accessToken
    //Store these values in securestore.
    console.log("Username:", username);
    console.log("Password:", password);
    loginInit(username, password);
  };

  const handleLogout = async () => {
    console.log("logout");

    //Get the user_id

    try {
      const userid = await getUserId();
      if (!userid) {
        console.log("No id found in token");
        throw new Error("Token has issue");
      }
      const response = await fetch(`${BASE_URL_}/Logout`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_id: userid }),
      });
      if (!response.ok) {
        console.log("Logout failed");
        throw new Error("Logout failed");
      }
      await clearTokens();
      return true;
    } catch (e) {
      console.log("Error logging out", e);
    }
  };

  const handleCreateAccount = async () => {
    console.log(createusername);
    console.log(createpassword);
    console.log(createEmail);
    console.log(BASE_URL);

    //Send post request with the information

    const data = {
      username: createusername,
      password: createpassword,
      email: createEmail,
    };

    try {
      const response = await fetch(`${BASE_URL_}/user`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("???");
      } else {
        console.log("succ");
      }
    } catch (e) {
      console.log(e.message);
    }
  };

  return (
    <View>
      <TextInput placeholder="username" onChangeText={setUsername} />
      <TextInput
        secureTextEntry={true}
        placeholder="password"
        onChangeText={setPassword}
      />

      <View style={styles.buttonSuite}>
        <Button title="Login" onPress={handleLogin} />
        <Button title="Logout" onPress={handleLogout} />
      </View>

      <View>
        <TextInput
          placeholder="Create Username"
          onChangeText={setcreateusername}
        />
        <TextInput
          placeholder="Create Strong Password"
          onChangeText={setcreatepassword}
        />
        <TextInput placeholder="enter email" onChangeText={setcreateEmail} />
        <Button title="Create Account" onPress={handleCreateAccount} />
        <PaginationBar currentPage={1}></PaginationBar>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#fff",
  },
  buttonSuite: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },
  buttons: {
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 12,
    paddingHorizontal: 32,
    borderRadius: 4,
    elevation: 3,
    backgroundColor: "#2196f3",
    color: "white",
  },
});

export default Login;
