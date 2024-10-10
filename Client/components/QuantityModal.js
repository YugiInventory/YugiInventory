import { View, Text, StyleSheet, Button } from "react-native";
import {
  BASE_URL_,
  getUserId,
  isTokenExpired,
} from "../services/AuthFunctions";
import * as SecureStore from "expo-secure-store";

const QuantityModal = ({ item }) => {
  const increase = (item) => {
    console.log("increase", item.quantity);
  };
  const decrease = (item) => {
    console.log("decrease", item.quantity);
  };

  return (
    <View>
      <Button title="+" onPress={increase} item={item} />
      <Text style={styles.quantityCount}>{item.quantity}</Text>
      <Button title="-" onPress={decrease} item={item} />
    </View>
  );
};

const styles = StyleSheet.create({
  quantityCount: {
    textAlign: "center",
  },
});

export default QuantityModal;
