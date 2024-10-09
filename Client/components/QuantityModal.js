import { View, Text, StyleSheet, Button } from "react-native";

const QuantityModal = ({ item }) => {
  return (
    <View>
      <Button title="+" />
      <Text style={styles.quantityCount}>{item.quantity}</Text>
      <Button title="-" />
    </View>
  );
};

const styles = StyleSheet.create({
  quantityCount: {
    textAlign: "center",
  },
});

export default QuantityModal;
