import { Text, StyleSheet } from "react-native"

export default function Inventory() {
  return <Text style={styles.container}>Inventory</Text>
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
