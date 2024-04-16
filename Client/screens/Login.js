import { Text, TextInput, StyleSheet, View } from "react-native";
import { Link } from "@react-navigation/native";

export default function Login() {
  return (
    <View>
      <Text>Placeholder for Logo</Text>
      <View style={styles.container}>
        <TextInput placeholder="Username" />
        <TextInput placeholder="Password" />
        <View style={styles.buttonSuite}>
          <Link to={{ screen: "Home" }} style={styles.buttons}>
            Login
          </Link>
          <Link to={{ screen: "CreateUser" }} style={styles.buttons}>
            Create User
          </Link>
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
