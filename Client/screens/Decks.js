import { Text, StyleSheet } from "react-native";

const Decks = () => {
  return <Text style={styles.container}>Decks</Text>;
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
    textAlign: "center",
  },
});

export default Decks;
