import { Button, Text, TextInput, StyleSheet, View } from "react-native";
import { useState } from "react";
import { BASE_URL } from "../index";

export default function CreateUser({ navigation }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = () => {
    navigation.navigate("Login");
  };

  return (
    <View>
      <TextInput placeholder="Enter Username" />
      <TextInput placeholder="Enter Password" />
      <TextInput placeholder="Confirm Password" />
      <Button title="Create User" onPress={handleSubmit} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
    textAlign: "center",
  },
});
