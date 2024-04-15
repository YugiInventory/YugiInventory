import { Button, Text, TextInput, StyleSheet, View } from "react-native";

export default function CreateUser() {
  return (
    <View>
      <TextInput placeholder="Enter Username" />
      <TextInput placeholder="Enter Password" />
      <TextInput placeholder="Confirm Password" />
      <Button title="Create User" />
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
