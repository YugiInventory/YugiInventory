import {
  Button,
  Text,
  TextInput,
  StyleSheet,
  View,
  Pressable,
} from "react-native"
import { Link } from "expo-router"
import CreateUser from "./CreateUser"

export default function Login({ navigation }) {
  return (
    <View>
      <TextInput placeholder="Username" />
      <TextInput placeholder="Password" />
      <Button title="Login">Login</Button>
      {/* <Link href="/CreateUser" asChild>
        <Pressable>
          <Text>Create User</Text>
        </Pressable>
      </Link> */}
      {/* <Text style={styles.container}>Login</Text> */}
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
})
