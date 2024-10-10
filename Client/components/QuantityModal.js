import { View, Text, StyleSheet, Button } from "react-native";
import {
  BASE_URL_,
  getUserId,
  isTokenExpired,
} from "../services/AuthFunctions";
import * as SecureStore from "expo-secure-store";

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
