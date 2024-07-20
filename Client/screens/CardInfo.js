import { Button, Text, TextInput, StyleSheet, View } from "react-native";
import { useState } from "react";
import BASE_URL from "../config";

const CardInfo = () => {
  const randomCard = async () => {
    try {
      const response = await fetch(`${BASE_URL}/card/10`)
        .then((response) => response.json())
        .then((data) => console.log(data.card_attribute));
    } catch (err) {
      console.error(err.message);
    }
  };
  return (
    <View>
      <Button title="Get Information" onPress={() => randomCard(123)}>
        Get Information
      </Button>
    </View>
  );
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

export default CardInfo;
