import { Button, Text, TextInput, StyleSheet, View } from "react-native";
import { useState } from "react";
import { BASE_URL_ } from "../services/AuthFunctions";

const CardInfo = () => {
  const generateCard = async () => {
    try {
      const response = await fetch(`${BASE_URL}/cards/getSingleCard/10`)
        .then((response) => response.json())
        .then((data) => console.log(data.card_attribute));
    } catch (err) {
      console.error(err.message);
    }
  };
  return (
    <View>
      <Button title="Get Information" onPress={() => generateCard()} />
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
