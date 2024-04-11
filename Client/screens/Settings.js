import { Text, StyleSheet } from "react-native"

export default function Settings() {
  return <Text style={styles.container}>Settings</Text>
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
    textAlign: "center",
  },
})
