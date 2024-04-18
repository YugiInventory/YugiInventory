import React from "react";
import { Text, TextInput, StyleSheet, View, Button } from "react-native";
import { BASE_URL } from "../index";

export default function Login({ navigation }) {
  const handleLogin = () => {
    navigation.navigate("Home");
  };

  const handleCreateUserScreen = () => {
    navigation.navigate("CreateUser");
  };

  return (
    <View>
      <Text>Placeholder for Logo</Text>
      <View style={styles.container}>
        <TextInput placeholder="Username" />
        <TextInput placeholder="Password" />
        <View style={styles.buttonSuite}>
          <Button title="Login" onPress={handleLogin} />
          <Button title="Create User" onPress={handleCreateUserScreen} />
        </View>
      </View>
    </View>
  );
}

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
